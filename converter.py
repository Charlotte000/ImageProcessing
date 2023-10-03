import io
import os
from configparser import ConfigParser
from threading import Thread
from time import sleep

import requests
from PIL import Image, ImageEnhance, ImageOps, ImagePalette

config = ConfigParser()
config.read('config.ini')


class Converter:
    @staticmethod
    def load_images(count: int, folder: str) -> None:
        def worker(index: int):
            for _ in range(10):
                try:
                    headers = { 'X-Api-Key': config['DEFAULT']['RandomImageAPI'], 'Accept': 'image/jpg' }
                    response = requests.get(f'https://api.api-ninjas.com/v1/randomimage', headers=headers)
                    if response.status_code == requests.codes.ok:
                        with Image.open(io.BytesIO(response.content)) as img:
                            img.save(os.path.join(folder, f'img{index:05}.png'))
                        break
                except:
                    sleep(5)

        if not os.path.exists(folder):
            os.mkdir(folder)

        threads = [Thread(target=worker, args=(i,)) for i in range(count)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()

    @staticmethod
    def convert_images(sharpness_factor: float, resize_factor: float, input_folder: str, output_folder: str) -> None:
        def worker(file_name: str):
            with Image.open(os.path.join(input_folder, file_name)) as image:
                image = ImageOps.scale(image, resize_factor)
                image = ImageEnhance.Sharpness(image).enhance(sharpness_factor)
                with Image.new('P', image.size) as result:
                    result.putpalette(ImagePalette.sepia())
                    result.paste(image, (0, 0) + image.size)
                    result.save(os.path.join(output_folder, file_name))


        if not os.path.exists(output_folder):
            os.mkdir(output_folder)

        threads = [Thread(target=worker, args=(file_name,)) for file_name in os.listdir(input_folder)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
