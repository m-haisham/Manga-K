import os
import tempfile
import traceback
import img2pdf

import numpy as np
from PIL import Image
from modules.manager import numericalSort

class VerticalStack:
    def stack(self, folder_path, save_path, end='.jpg', new_width=None):
        '''
        folder_path (string): relative or absolute path to images
        save_path (string): relative or absolute path to save composite
        end (string): extension of the composite image
        new_width (+int): if new width not specified will use most recurring width to resize images

        Images in (folder_path) must be named as integers
        This function stacks the images vertically and saves composite in save_path with name of the last folder to path and extenstion (end)
        '''
        images = os.listdir(folder_path)
        
        print('initializing . . .', end=' ')
        image_dictionary_list = self.disect(images, folder_path)
        print('done!')

        # select width
        if new_width is None:
            print('Getting most recurring width . . .', end=' ')
            new_width = self.get_width(image_dictionary_list)
            print(new_width, 'done!')
        else:
            new_width = abs(int(new_width))
            print('using given width of', new_width, 'for resizing')

        #resizing images
        print('resizing images . . .', end=' ')
        image_array_list = []
        for image in image_dictionary_list:
            i = Image.open(os.path.join(image['directory'], str(image['name'])) + image['extension'])
            width, height = i.size # get size

            #adjust width of images to be constant
            adjusted_image = i
            if width != new_width:
                new_height = self.get_new_height(width, height, new_width)
                adjusted_image = i.resize((new_width, new_height), Image.LANCZOS)
            
            adjusted_image = adjusted_image.convert('RGB')
            array = np.asarray(adjusted_image)
            image_array_list.append(array)
        print('done!')

        print('compositing images . . .', end=' ')
        composite_array = np.vstack(image_array_list)
        composite_image = Image.fromarray(composite_array)
        print('done!')

        composite_image.save(os.path.join(save_path, get_last_directory(folder_path)) + end)
        print('composite saved as', os.path.join(save_path, get_last_directory(folder_path)) + end)

    def disect(self, image_paths, directory, key='name'):
        '''
        image_paths (string): names of images
        directory (string): path of images
        
        Takes (image_paths) and disects and sorts them according to (key)

        returns list of dictionaries
        '''
        sorted_images = []
        for image_path in image_paths:
            fn, fext = os.path.splitext(image_path)
            number = int(fn)
            dictionary = {
                'name': number,
                'extension': fext,
                'directory': directory,
                'temp_path': None
            }
            sorted_images.append(dictionary)

        sorted_images.sort(key = lambda k: k['name'])
        return sorted_images

    def get_width(self, image_list):
        '''
        image_list (list): list populated with dictionaries

        Returns the most recurring width
        '''
        size_repeat_dictionary = {}
        for image in image_list:
            i = Image.open(os.path.join(image['directory'], str(image['name'])) + image['extension'])
            width = i.size[0]
            if str(width) in size_repeat_dictionary.keys():
                size_repeat_dictionary[str(width)] += 1
            else:
                size_repeat_dictionary[str(width)] = 1
        
        highest = 0
        new_width = 0
        for key in size_repeat_dictionary.keys():
            if size_repeat_dictionary[key] > highest:
                new_width = int(key)
                highest = size_repeat_dictionary[key]
        return new_width

    def get_new_height(self, width, height, new_width):
        '''
        width (int): current width of image
        height (int): current height of image
        new_width (int): new width of image

        returns (int): the new height keeping the aspect_ratio
        '''
        return int((height * new_width) / width)

def get_last_directory(full_dir):
    '''
    full_dir (string): relative of absolute path

    returns (string): last directory of (full_dir)
    '''
    full_dir = full_dir if full_dir[-1] != '/' else full_dir[:-1]
    if '/' in full_dir:
        dir_lst = full_dir.split('/')
    else:
        dir_lst = full_dir.split('\\')
    return dir_lst[len(dir_lst) - 1]

def dir_to_pdf(path, save_path):

    # get all directory paths
    dirs = sorted(os.listdir(path), key=numericalSort)

    file_path_list = []

    # all of the files tested and opened
    for directory in dirs:
        try:
            # open image using PIL library
            new_img = Image.open(os.path.join(path, directory))
        except Exception as ex:
            # if any error occurs skip the file
            print('[ERROR] [%s] Cant open %s as image!' % (type(ex).__name__.upper(), os.path.join(path, directory)))
        else:

            file_path = os.path.join(path, directory)

            # if image mode is RGBA
            if(new_img.mode == 'RGBA'):
                # convert image to RGB
                print('[CONVERT] [%s] RGBA to RGB' % os.path.basename(os.path.normpath(directory)).upper())

                # create RGB image with white background of same size
                rgb = Image.new('RGB', new_img.size, (255, 255, 255))

                # paste using alpha as mask
                rgb.paste(new_img, new_img.split()[3])

                # get temporary path
                temp = tempfile.NamedTemporaryFile().name + '.jpg'
                print(temp)
                # save image as temporary
                rgb.save(temp)

                # overrite file_path
                file_path = temp

            file_path_list.append(file_path)

    # if no images exit
    if len(file_path_list) == 0:
        return

    # save as pdf using img2pdf
    with open(os.path.join(save_path, get_last_directory(path) + '.pdf'), 'wb') as f:
        f.write(img2pdf.convert(file_path_list, dpi=300.0))
