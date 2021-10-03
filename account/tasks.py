from celery import shared_task
from PIL import Image
import os

from HydroCloud import settings
from account import consts
from account.models import Algorithm
from account.ssh import SFTP, SSH


@shared_task
def start_algorithm(jsf_input_path: str, jsf_output_path: str, data_path: str, image_path: str, params: str, slug: str):
    print('Start algorithm')
    os.system(f'C:\\Users\\ReF0iL\\Desktop\\HydroCloud\\static\\Parser.exe {jsf_input_path} {jsf_output_path}')  # Run parser
    print('Parsed..')

    sftp = SFTP()
    # PUT file
    file_name = os.path.split(jsf_output_path)[1]
    remote_path = f'/home/dsalushkin/mpi/{file_name}'
    sftp.put_file(jsf_output_path, remote_path)

    params_path = os.path.join(settings.BASE_DIR, 'media', 'params.txt')
    with open(params_path, 'r') as f:
        f.write(params)
    remote_path = '/home/dsalushkin/mpi/params.txt'
    sftp.put_file(params_path, remote_path)

    print('Start algorithm')
    ssh = SSH()
    ssh.command(f'mpiexec -n 1 ./mpi/p')
    print('End algorithm')
    # GET file
    remote_path = '/home/dsalushkin/mpi/output1.txt'
    sftp.get_file(data_path, remote_path)
    print('Read')

    sftp.client.close()
    ssh.client.close()

    def _round(x: int) -> int:
        """ Round numbers in range(0:255) """
        if x > 255:
            return 255
        elif x < 0:
            return 0
        return x

    print('Start generate image')
    with open(data_path, 'r') as file:
        data = tuple(file.readlines())
        img = Image.new('L', (7384, 8680))
        i = j = 0
        stop = False
        for line in data:
            for pixel in line.split():
                img.putpixel((i, j), _round(int(float(pixel))))
                j += 1
                if j == 8680:
                    if i == 7384:
                        stop = True
                        break
                    j = 0
                    i += 1
            if stop:
                break
        print('Save image')
        img.save(image_path)
    alg = Algorithm.objects.get(slug=slug)
    alg.image = image_path
    alg.status = consts.Statuses.Complete
    alg.save()
