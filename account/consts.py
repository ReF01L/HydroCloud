import os
from typing import List, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from functools import reduce

from account.ssh import SFTP, SSH


class Algorithms(models.TextChoices):
    VolumetricScatterFiltering = 'Volumetric Scatter Filtering', _('Фильтрации объёмного рассеяния')
    MedianFiltering = 'Median Filtering', _('Медианная фильтрация')
    DoubleFiltering = 'Double Filtering', _('Двойная фильтрация')
    LogarithmicFiltering = 'Logarithmic Filtering', _('Логарифмическая фильтрация')


class Statuses(models.TextChoices):
    InProcess = 'In process', _('В процессе')
    Complete = 'Complete', _('Готов')


def get_volumetric_scatter_filtering_dict(params):
    return {
        'height': params[0],
        'width': params[1],
        'start': params[2],
        'end': params[3],
    }


def run_parser(jsf_path, output_path):
    os.system(f'C:\\Users\\ReF0iL\\Desktop\\HydroCloud\\static\\Parser.exe {jsf_path} {output_path}')


def start_algorithm(jsf_input_path: str, jsf_output_path: str, data_path: str, image_path: str, params: str):
    params = params.replace('| ', '')

    run_parser(jsf_input_path, jsf_output_path)
    print('Parsed..')

    sftp = SFTP()
    # PUT file
    file_name = os.path.split(jsf_output_path)[1]
    remote_path = f'/home/dsalushkin/mpi/{file_name}'
    sftp.put_file(jsf_output_path, remote_path)
    print('Start algorithm')
    ssh = SSH()
    ssh.command(f'mpiexec -n 1 ./mpi/p {params}')
    print('End algorithm')
    # GET file
    remote_path = '/home/dsalushkin/mpi/output1.txt'
    sftp.get_file(data_path, remote_path)
    print('Read')

    sftp.client.close()
    ssh.client.close()

    #
    # N = params.split(' ')[0]  # 8680
    # M = params.split(' ')[1]  # 7384

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
