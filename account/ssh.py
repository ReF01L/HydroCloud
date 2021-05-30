from typing import List

import paramiko

from HydroCloud import settings


class SSH:
    def __new__(cls) -> 'SSH':
        if not hasattr(cls, 'instance'):
            cls.instance = super(SSH, cls).__new__(cls)
            cls.client = paramiko.SSHClient()
            cls.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cls.client.connect('jupiter.febras.net', 2020, settings.config['SSH']['LOGIN'], settings.config['SSH']['PASSWORD'])
        return cls.instance

    @classmethod
    def command(cls, command: str) -> List[str]:
        return list(x.decode('utf-8') for x in cls.client.exec_command(command)[1].read().splitlines())
