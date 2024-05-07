import PySimpleGUI as sg
import datetime
import csv

class Agendamento:
    def __init__(self, numero_whatsapp, mensagem, caminho_imagem, horario_envio):
        self.numero_whatsapp = numero_whatsapp
        self.mensagem = mensagem
        self.caminho_imagem = caminho_imagem
        self.horario_envio = horario_envio

    def __repr__(self):
        return f"Agendamento({self.numero_whatsapp}, {self.mensagem}, {self.caminho_imagem}, {self.horario_envio})"

class AgendamentoController:
    def __init__(self, arquivo_csv):
        self.arquivo_csv = arquivo_csv

    def carregar_proximos_agendamentos(self):
        agora = datetime.datetime.now()
        proximos_agendamentos = []

        with open(self.arquivo_csv, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho

            for linha in reader:
                numero_whatsapp, mensagem, caminho_imagem, horario_envio = linha

                # Verifica se o horário de envio está vazio ou não
                if horario_envio:
                    horario_envio = datetime.datetime.strptime(horario_envio, '%H:%M').time()
                    data_envio = datetime.datetime.combine(agora.date(), horario_envio)

                    if data_envio > agora:
                        proximos_agendamentos.append(Agendamento(numero_whatsapp, mensagem, caminho_imagem, horario_envio))

        return proximos_agendamentos

    def agendar_mensagem(self, agendamento):
        with open(self.arquivo_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([agendamento.numero_whatsapp, agendamento.mensagem, agendamento.caminho_imagem, agendamento.horario_envio])

class InterfaceGrafica:
    def __init__(self, agendamento_controller):
        self.agendamento_controller = agendamento_controller
        self.proximos_agendamentos = []
        self.window = None

    def build(self):
        sg.theme('LightBlue2')

        layout = [
            [sg.Text('Agendamento de Mensagem e Imagem via WhatsApp', font=('Arial', 16), justification='center')],
            [sg.Text('Número do WhatsApp (com código do país):', font=('Arial', 12)), sg.InputText(key='-NUMERO-', size=(20, 1))],
            [sg.Text('Mensagem:', font=('Arial', 12)), sg.InputText(key='-MENSAGEM-', size=(100, 10))],
            [sg.Text('Caminho da Imagem:', font=('Arial', 12)), sg.InputText(key='-CAMINHO_IMAGEM-', size=(20, 1)), sg.FileBrowse()],
            [sg.Text('Horário de envio (HH:MM):', font=('Arial', 12)), sg.InputText(key='-HORARIO-', size=(20, 1))],
            [sg.Button('Agendar Envio', size=(15, 1)), sg.Button('Cancelar', size=(15, 1))],
            [sg.Text('Próximos Agendamentos:', font=('Arial', 12))],
            [sg.Listbox(values=[], size=(70, 5), key='-PROXIMOS_AGENDAMENTOS-')],
        ]

        self.window = sg.Window('Agendamento de Mensagem e Imagem', layout, size=(1280, 720))

    def run(self):
        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Cancelar':
                break
            elif event == 'Agendar Envio':
                numero_whatsapp = values['-NUMERO-']
                mensagem = values['-MENSAGEM-']
                caminho_imagem = values['-CAMINHO_IMAGEM-']
                horario_envio = values['-HORARIO-']

                agendamento = Agendamento(numero_whatsapp, mensagem, caminho_imagem, horario_envio)
                self.agendamento_controller.agendar_mensagem(agendamento)

        self.window.close()

if __name__ == '__main__':
    arquivo_csv = 'agendamentos.csv'
    agendamento_controller = AgendamentoController(arquivo_csv)
    interface = InterfaceGrafica(agendamento_controller)
    interface.build()
    interface.run()
    interface.update_proximos_agendamentos()
