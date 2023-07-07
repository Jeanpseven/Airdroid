from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pyairmore.request import AirmoreSession
import subprocess

def install_package(package):
    subprocess.check_call(['pip', 'install', package])

# Verificar se a biblioteca pyairmore está instalada
try:
    import pyairmore
except ImportError:
    print("A biblioteca pyairmore não foi encontrada. Instalando...")
    install_package('pyairmore')
    import pyairmore

def select_file():
    Tk().withdraw()  # Esconde a janela principal do Tkinter
    file_path = askopenfilename()  # Abre uma janela de seleção de arquivo
    return file_path

def list_nearby_devices():
    session = AirmoreSession()
    devices = session.discover_devices()
    
    if devices:
        print("Dispositivos próximos encontrados:")
        for index, device in enumerate(devices, start=1):
            print(f"{index}. {device['name']} ({device['ip']})")
        
        device_number = int(input("Digite o número do dispositivo: "))
        
        if device_number >= 1 and device_number <= len(devices):
            selected_device = devices[device_number - 1]
            print(f"Dispositivo selecionado: {selected_device['name']} ({selected_device['ip']})")
            file_path = select_file()
            
            try:
                session = AirmoreSession(selected_device['ip'])
                session.is_server_running()  # Verifica se o AirDroid está em execução no dispositivo selecionado
                session.open_image(file_path)
                print("Arquivo compartilhado com sucesso!")
            except Exception as e:
                print(f"Ocorreu um erro ao compartilhar o arquivo: {str(e)}")
        else:
            print("Número de dispositivo inválido.")
    else:
        print("Nenhum dispositivo próximo encontrado.")

if __name__ == '__main__':
    list_nearby_devices()
