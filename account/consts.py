import os
from typing import List, Tuple

from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from functools import reduce

from account.ssh import SFTP, SSH

delimiter = '|'


class Algorithms(models.TextChoices):
    VolumetricScatterFiltering = 'Volumetric Scatter Filtering', _('Фильтрации объёмного рассеяния')
    MedianFiltering = 'Median Filtering', _('Медианная фильтрация')
    DoubleFiltering = 'Double Filtering', _('Двойная фильтрация')
    LogarithmicFiltering = 'Logarithmic Filtering', _('Логарифмическая фильтрация')


def get_volumetric_scatter_filtering_dict(params):
    return {
        'height': params[0],
        'width': params[1],
        'start': params[2],
        'end': params[3],
    }


def data_to_png(data: List[int],
                filename: str,
                size: Tuple[int, int]) -> None:
    """ Convert list of int to monochrome colors """

    def _round(x: int) -> int:
        """ Round numbers in range(0:255) """
        if x > 255:
            return 255
        elif x < 0:
            return 0
        return x

    colors = bytes(map(_round, data))
    img = Image.frombytes('L', size, colors)
    img.save(filename)


def run_parser(jsf_path, output_path):
    os.system(f'C:\\Users\\ReF0iL\\Desktop\\HydroCloud\\static\\Parser.exe {jsf_path} {output_path}')


def start_algorithm(jsf_input_path: str, jsf_output_path: str, data_path: str, image_path: str, params: str):
    sftp = SFTP()
    ssh = SSH()
    params = params.replace('| ', '')

    run_parser(jsf_input_path, jsf_output_path)
    # PUT file
    file_name = os.path.split(jsf_output_path)[1]
    remote_path = f'/home/dsalushkin/mpi/{file_name}'
    sftp.put_file(jsf_output_path, remote_path)

    ssh.command(f'mpiexec -n 1 ./mpi/p {params}')

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

    data = tuple(open(data_path, 'r').readlines())
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
    img.save(image_path)

    # _data = []  # tmp array to save signal value
    # data = tuple(open(data_path, 'r').readlines())
    # for line in data:
    #     _data.extend((int(float(x)) for x in line.split()))  # convert every num to int
    # data_to_png(_data, image_path, (8680, 7384))
