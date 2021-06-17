from server import server

"""
Classe que implementa o server
e funciona como um intermediario entre o servidor e
o front-end.
"""
class app:
    def __init__(self):
        self.server = server()
        self.init = False

    def init_server(self):
        if self.init == False:
            self.server.listen_connections()
            self.init = True
            return True
        else:
            return False

    def show_clients(self):
        return self.server.clients

    def selected(self, id):
        return self.server.selected(id)

    def command_execute(self, command):
        return self.server.command(command)
