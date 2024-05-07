import pyautogui
import time
import datetime as dt
import pywhatkit as kit

arquivo_csv = "agendamentos.csv"

# Replace with the recipient's phone number
phone_num = "+5511978314783"

# Replace with the actual file path
file_path = "C:/Users/slpra/OneDrive/Imagens/Jurandir.png"

mensagem = "Olá, tudo bem? Estou enviando esta mensagem e imagem automaticamente!"
# Define the time you want to send the message (e.g., 15 minutes from now)
send_time = dt.datetime.now() + dt.timedelta(minutes=1)

# Send the message using pywhatkit
kit.sendwhats_image(phone_num, file_path,mensagem, send_time.hour, send_time.minute)
time.sleep(10) 
pyautogui.press('tab', presses=3)
pyautogui.press('enter')
time.sleep(1)           
