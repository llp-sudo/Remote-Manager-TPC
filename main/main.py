import eel
from app import app

app = app()

"""Função para inicializar o servidor"""
@eel.expose
def init_server():
    status = app.init_server()
    return status


"""Função para listar os clientes"""
@eel.expose
def list_connections():
    print("executado")
    return app.show_clients()


"""Função para selecionar o cliente"""
@eel.expose
def cli_selected(id):
    print(f"ID = {id}")
    return app.selected(id)


"""Função para selecionar enviar o comando"""
@eel.expose
def send_command(command):
    output = app.command_execute(command)
    print(output)
    return output

"""Inicializa o eel"""
eel.init('template')
try:
    eel.start('index.html', size=(850, 400), port=0)   #python will select free ephemeral ports.
except (SystemExit, MemoryError, KeyboardInterrupt):
    print ("Program Exit, Save Logs if Needed")