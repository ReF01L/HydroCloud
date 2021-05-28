from typing import Tuple

import paramiko
from django.conf import settings


class SSH:
    def __init__(self, request, login: str, password: str) -> None:
        self.session = request.session
        ssh = self.session.get(settings.SSH_SESSION_CLIENT)
        if not ssh:
            ssh = self.session[settings.SSH_SESSION_CLIENT] = {}
        self.ssh = ssh
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect('jupiter.febras.net', 2020, login, password)
        self.ssh['client'] = self.client

    def command(self, command: str) -> None:
        self.ssh['content'] = list(x.decode('utf-8') for x in self.client.exec_command(command)[1].read().splitlines())
