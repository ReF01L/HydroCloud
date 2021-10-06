from typing import List

import paramiko

from HydroCloud import settings


class SSH:
    client: paramiko.SSHClient = None

    def __new__(cls) -> 'SSH':
        if not hasattr(cls, 'instance'):
            cls.instance = super(SSH, cls).__new__(cls)
            cls.client = paramiko.SSHClient()
            cls.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cls.client.connect(username=settings.config['SSH']['LOGIN'],
                               password='ЙФЯ?ЦУЧ"!Лфеэлф"№;',
                               hostname='jupiter.febras.net',
                               port=2020)
        return cls.instance

    @classmethod
    def command(cls, command: str) -> List[str]:
        a = list(x.decode('utf-8') for x in cls.client.exec_command(command)[1].read().splitlines())
        return a


class SFTP:
    client: paramiko.SFTPClient = None

    def __new__(cls) -> 'SFTP':
        if not hasattr(cls, 'instance'):
            cls.instance = super(SFTP, cls).__new__(cls)
            transport = paramiko.Transport(('jupiter.febras.net', 2020))
            transport.connect(username=settings.config['SSH']['LOGIN'], password='ЙФЯ?ЦУЧ"!Лфеэлф"№;')
            cls.client = paramiko.SFTPClient.from_transport(transport)
        return cls.instance

    @classmethod
    def get_file(cls, local_path: str, remote_path: str) -> None:
        cls.client.get(remote_path, local_path)

    @classmethod
    def put_file(cls, local_path: str, remote_path: str) -> None:
        cls.client.put(local_path, remote_path)
