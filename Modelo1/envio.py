import csv
import pywhatkit as kit
from datetime import datetime, timedelta
import os

def enviar_mensagem(numero_whatsapp, mensagem, caminho_imagem):
    try:
        kit.sendwhats_image(phone_num=numero_whatsapp,
                            img_path=caminho_imagem,
                            caption=mensagem,
                            wait_time=20)  # Aguarda 20 segundos antes de enviar a mensagem
        print(f'Mensagem com imagem enviada para {numero_whatsapp}: {mensagem}')
    except Exception as e:
        print(f'Ocorreu um erro ao enviar a mensagem com imagem para {numero_whatsapp}: {str(e)}')

def verificar_e_enviar_mensagens(agora, arquivo_csv):
    tolerancia_minutos = 5
    horario_inicio = agora - timedelta(minutes=tolerancia_minutos)
    horario_fim = agora + timedelta(minutes=tolerancia_minutos)

    with open(arquivo_csv, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            numero_whatsapp, mensagem, caminho_imagem, horario_envio = row

            # Verifica se o horário está dentro da tolerância
            horario_envio = datetime.strptime(horario_envio, '%H:%M')
            if horario_inicio.time() <= horario_envio <= horario_fim.time():
                enviar_mensagem(numero_whatsapp, mensagem, caminho_imagem)

if __name__ == "__main__":
    # Armazena a hora que foi iniciado
    agora = datetime.now()

    # Abre o arquivo CSV
    arquivo_csv = "agendamentos.csv"

    # Verifica e envia mensagens agendadas
    verificar_e_enviar_mensagens(agora, arquivo_csv)
