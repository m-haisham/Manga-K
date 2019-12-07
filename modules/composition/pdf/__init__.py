import os
import tempfile

import img2pdf
from PIL import Image

from modules.sorting import numerical_sort


def dir_to_pdf(path, save_path, verbose=False):
    # get all directory paths
    dirs = sorted(os.listdir(path), key=numerical_sort)

    file_path_list = []

    # all of the files tested and opened
    for directory in dirs:
        try:
            # open image using PIL library
            new_img = Image.open(os.path.join(path, directory))
        except Exception as ex:
            # if any error occurs skip the file
            print(
                f'[ERROR] [{type(ex).__name__.upper()}] Cant open {os.path.join(path, directory)} as image!')
        else:

            file_path = os.path.join(path, directory)

            # if image has transparency
            if 'transparency' in new_img.info:
                # convert to RGBA mode
                new_img = new_img.convert('RGBA')

            # if image mode is RGBA
            if new_img.mode == 'RGBA':
                # convert image to RGB
                if verbose:
                    print(f'[CONVERT] [{os.path.basename(os.path.normpath(directory)).upper()}] RGBA to RGB')

                # create RGB image with white background of same size
                rgb = Image.new('RGB', new_img.size, (255, 255, 255))

                try:
                    # paste using alpha as mask
                    rgb.paste(new_img, new_img.split()[3])
                except OSError as e:
                    print(f'\n{e}')
                    continue

                # get temporary path
                temp = tempfile.NamedTemporaryFile().name + '.jpg'

                # save image as temporary
                rgb.save(temp, 'JPEG')

                # overrite file_path
                file_path = temp

            file_path_list.append(file_path)

    # if no images exit
    if len(file_path_list) == 0:
        return

    try:
        # save as pdf using img2pdf
        with open(os.path.join(save_path, os.path.basename(os.path.normpath(path)) + '.pdf'), 'wb') as f:
            f.write(img2pdf.convert(file_path_list))
    except Exception as e:
        print(f'{type(e).__name__.upper()} - {path} - {e}')