import csv
import pywhatkit as kit
from datetime import datetime
import time

def enviar_mensagem(numero_whatsapp, mensagem, caminho_imagem):
    try:
        kit.sendwhats_image(phone_num=numero_whatsapp,
                            img_path=caminho_imagem,
                            caption=mensagem,
                            wait_time=20)  # Aguarda 20 segundos antes de enviar a mensagem
        print(f'Mensagem com imagem enviada para {numero_whatsapp}: {mensagem}')
    except Exception as e:
        print(f'Ocorreu um erro ao enviar a mensagem com imagem para {numero_whatsapp}: {str(e)}')

def enviar_mensagens_automaticamente(arquivo_csv):
    while True:
        agora = datetime.now()
        with open(arquivo_csv, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                numero_whatsapp, mensagem, caminho_imagem, horario_envio = row

                # Verifica se o horário está vazio
                if not horario_envio:
                    continue

                horario_envio = datetime.strptime(horario_envio, '%H:%M')

                # Verifica se é hora de enviar a mensagem
                if agora.hour == horario_envio.hour and agora.minute == horario_envio.minute:
                    enviar_mensagem(numero_whatsapp, mensagem, caminho_imagem)

        # Espera 1 minuto antes de verificar novamente
        time.sleep(60)


if __name__ == "__main__":
    arquivo_csv = "agendamentos.csv"
    enviar_mensagens_automaticamente(arquivo_csv)
