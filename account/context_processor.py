from HydroCloud import settings
from account.ssh import SSH


def ssh(request):
    return {'ssh': SSH(request, settings.config['SSH']['LOGIN'], settings.config['SSH']['PASSWORD'])}
