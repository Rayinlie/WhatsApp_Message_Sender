import csv
import pywhatkit as kit
from datetime import datetime, timedelta

def enviar_mensagem(numero_whatsapp, mensagem, caminho_imagem, send_time):
    try:
        kit.sendwhats_image(numero_whatsapp, caminho_imagem, mensagem, send_time.hour, send_time.minute)
        time.sleep(10)
        pyautogui.press('tab', presses=3)
        pyautogui.press('enter')
        time.sleep(1)
        print(f'Mensagem com imagem enviada para {numero_whatsapp}: {mensagem}')
    except Exception as e:
        print(f'Ocorreu um erro ao enviar a mensagem com imagem para {numero_whatsapp}: {str(e)}')

def verificar_e_enviar_mensagens(agora, arquivo_csv):
    tolerancia_minutos = 5
    horario_inicio = agora - timedelta(minutes=tolerancia_minutos)
    horario_fim = agora + timedelta(minutes=tolerancia_minutos)

    with open(arquivo_csv, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            numero_whatsapp, mensagem, caminho_imagem, horario_envio = row
            if horario_envio:
                horario_envio = datetime.strptime(horario_envio, '%H:%M')
                if horario_inicio.time() <= horario_envio.time() <= horario_fim.time():
                    enviar_mensagem(numero_whatsapp, mensagem, caminho_imagem, horario_envio)

if __name__ == "__main__":
    import pyautogui
    import time

    agora = datetime.now()
    arquivo_csv = "agendamentos.csv"
    verificar_e_enviar_mensagens(agora, arquivo_csv)
