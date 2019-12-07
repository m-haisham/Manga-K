import os

import numpy as np
from PIL import Image


class VerticalStack:
    def stack(self, folder_path, save_path, end='.jpg', new_width=None, verbose=False):
        """
        folder_path (string): relative or absolute path to images
        save_path (string): relative or absolute path to save composite
        end (string): extension of the composite image
        new_width (+int): if new width not specified will use most recurring width to resize images

        Images in (folder_path) must be named as integers
        This function stacks the images vertically and saves composite in save_path with name of the last folder to path and extenstion (end)
        """
        images = os.listdir(folder_path)

        if verbose:
            print('initializing . . .', end=' ')
        image_dictionary_list = self.disect(images, folder_path)
        if verbose:
            print('done!')

        # select width
        if new_width is None:
            if verbose:
                print('Getting most recurring width . . .', end=' ')
            new_width = self.get_width(image_dictionary_list)
            if verbose:
                print(new_width, 'done!')
        else:
            new_width = abs(int(new_width))
            if verbose:
                print('using given width of', new_width, 'for resizing')

        # resizing images
        if verbose:
            print('resizing images . . .', end=' ')
        image_array_list = []
        for image in image_dictionary_list:
            i = Image.open(os.path.join(image['directory'], str(
                image['name'])) + image['extension'])
            width, height = i.size  # get size

            # adjust width of images to be constant
            adjusted_image = i
            if width != new_width:
                new_height = self.get_new_height(width, height, new_width)
                adjusted_image = i.resize(
                    (new_width, new_height), Image.LANCZOS)

            adjusted_image = adjusted_image.convert('RGB')
            array = np.asarray(adjusted_image)
            image_array_list.append(array)
        if verbose:
            print('done!')

        if verbose:
            print('compositing images . . .', end=' ')
        composite_array = np.vstack(image_array_list)
        composite_image = Image.fromarray(composite_array)
        if verbose:
            print('done!')

        composite_image.save(os.path.join(save_path, folder_path.parts[-1] + end))
        if verbose:
            print('composite saved as', os.path.join(save_path, folder_path.parts[-1] + end))

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

        sorted_images.sort(key=lambda k: k['name'])
        return sorted_images

    def get_width(self, image_list):
        '''
        image_list (list): list populated with dictionaries

        Returns the most recurring width
        '''
        size_repeat_dictionary = {}
        for image in image_list:
            i = Image.open(os.path.join(image['directory'], str(
                image['name'])) + image['extension'])
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


def dir_to_jpg(path, save_path):
    VerticalStack().stack(path, save_path)