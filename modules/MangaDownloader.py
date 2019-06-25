import os
import shutil
import json
import sys
from io import BytesIO
import re

import requests
from bs4 import BeautifulSoup
from PIL import Image

from modules.static import Const
from modules.ImageStacking import VerticalStack, dir_to_pdf

def make_valid(path):
    return re.sub(r'[/\\:*"<>|]', '', path)

class MangaDownloader:
    def __init__(self):
        self.image_stacker = VerticalStack()
        self.settings_path = 'config.json'
        if self.settings_exists():
            self.load_settings()

    def download_init(self):
        while(True):
            manga_url = input('Input full url to manga from mangakakalot.com|manganel.com\nURl: ')

            self.print_info(manga_url)

            print("\nLeave following field empty to start from beginning chapter")
            manga_start = input('Start index: ')
            if manga_start == '':
                manga_start = 1

            ch_lst = None
            print("\nLeave following field empty to download till last chapter")
            manga_end = input('End index: ')
            if manga_end == '':
                ch_lst = self.get_chapter_list(manga_url)
                manga_end = len(ch_lst)

            if manga_url[-1] == '/':
                manga_url = manga_url[0:-1]
            
            while True:
                make_settings = input("Change Settings (Y/N): ")
                if make_settings.lower() == 'y':
                    make_settings = True
                    break
                elif make_settings.lower() == 'n':
                    make_settings = False
                    break
                else:
                    print('pick a valid choice')

            if os.path.exists(self.settings_path) and not make_settings:
                with open(self.settings_path, 'r') as f:
                    self.settings = json.load(f)
            else:        
                while True:
                    make_composites = input("\nMake Composites (Y/N): ")
                    if make_composites.lower() == 'y':
                        make_composites = True
                        while True:
                            keep_originals = input("Delete originals (Y/N): ")
                            if keep_originals.lower() == 'y':
                                keep_originals = False
                                break
                            elif keep_originals.lower() == 'n':
                                keep_originals = True
                                break
                            else:
                                print('pick a valid choice')
                        break
                    elif make_composites.lower() == 'n':
                        make_composites = False
                        keep_originals = True
                        break
                    else:
                        print('pick a valid choice')
                self.settings = {
                    'make_composite': make_composites,
                    "keep_originals": keep_originals
                }
                with open(self.settings_path, 'w') as f:
                    json.dump(self.settings, f)
            
            try:
                int_start = int(manga_start)
                int_end = int(manga_end) + 1
                break
            except ValueError:
                print('Start or end chapter numbers not numerical')

        self.download_manga(manga_url, int_start, int_end, ch_lst)

    def save_image(self, url, directory):
        """
        url (String): online image file path
        directory (String): Image file save path

        returns: None

        This function downloads [url] and prints the progress of the download to the console and save the file to [directory]
        """
        filename = url.split('/')[-1]
        print('Downloading ' + url)
        with open(directory + '/' + filename, 'wb') as f:
            response = requests.get(url, stream=True)

            total_length = response.headers.get('content-length')
            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                length_kb = round(total_length / 1024, 2)
                chunksize = int(total_length / 50)
                for data in response.iter_content(chunk_size=chunksize):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s] %.2f/%.2f kb" % ('=' * done, ' ' * (50 - done), round(dl / 1024, 2), length_kb))
                    sys.stdout.flush()

        print(' Done.')
        print('to path -> ' + os.getcwd() + "\\" + directory + '\\' + filename)
        print()

    def get_manga_name(self, manga_path):
        """
        manga_path (string): manga path from mangakakalot.com

        return (string): manga title
        """
        r = requests.get(manga_path)
        soup = BeautifulSoup(r.content, "html.parser")
        titlebox = soup.find(class_="manga-info-text")
        return titlebox.find("h1").text

    def get_chapter_list(self, manga_path):
        """
        manga_path (string): manga path from mangakakalot.com

        return (list): chapters of the manga
        """
        r = requests.get(manga_path)
        soup = BeautifulSoup(r.content, "html.parser")
        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")
        chapters = []
        for i in range(len(rows) - 1, -1, -1):
            chapters.append(rows[i].find('a', href=True)['href'])
        return chapters

    def get_page_list(self, chapter_path):
        """
        chapter_path (string): path of the chapter 

        returns (list): pages of the chapter
        """
        r = requests.get(chapter_path)
        soup = BeautifulSoup(r.content, "html.parser")
        pagebox = soup.find(id="vungdoc")
        rows = pagebox.find_all('img')
        pages = []
        for row in rows:
            pages.append(row['src'])
        return pages

    def download_manga(self, url, starting_chapter, ending_chapter, chapter_list = None):
        """
        url (string): manga path from mangakakalot.com
        starting_chapter (int): download start (inclusive)
        ending_chapter (int): download end (exclusive)
        chapter_list (list): optional

        returns None
        """
        
        manga_dir = os.path.join(Const.MangaSavePath, make_valid(self.get_manga_name(url)))
        composite_save_dir = os.path.join(manga_dir, 'Composites')

        # Create directories
        if not os.path.exists(Const.MangaSavePath):
            os.mkdir(Const.MangaSavePath)
        if not os.path.exists(manga_dir):
            os.mkdir(manga_dir)
        if self.settings['make_composite']:
            if not os.path.exists(composite_save_dir):
                os.mkdir(composite_save_dir)

        if chapter_list is None:
            chapter_list = self.get_chapter_list(url)
        print('\nChapter list loaded.')

        if starting_chapter - 1 < 0 or ending_chapter > len(chapter_list):
            print(starting_chapter)
            print(ending_chapter)
            print("Out of range.")

        for i in range(starting_chapter - 1, ending_chapter - 1, 1): # loop through every chapter in range
            chapter_name = chapter_list[i].split('/')[-1]
            chapter_directory = os.path.join(manga_dir, chapter_name)
            print("\nDownloading " + chapter_name)
            if not os.path.exists(chapter_directory):
                os.mkdir(chapter_directory) # create chapter_directory
            for j in self.get_page_list(chapter_list[i]):
                self.save_image(j, chapter_directory) # save image

            if self.settings['make_composite']:
                print('Attempting composition of %s ... ' % chapter_directory)
                if self.settings['composition_type'] == 'pdf':
                    dir_to_pdf(chapter_directory, composite_save_dir)
                elif self.settings['composition_type'] == 'image':
                    self.image_stacker.stack(chapter_directory, composite_save_dir)
                print("Composition done!")
                if not self.settings['keep_originals']:
                    shutil.rmtree(chapter_directory) # remove chapter
                    print(chapter_directory, 'removed')

    def print_info(self, manga_path):
        """
        manga_path (string): url of manga from mangakakalot.com
        returns None

        prints the information of manga
        """
        r = requests.get(manga_path)
        soup = BeautifulSoup(r.content, "html.parser")
        print("\n-- %s --\n" % self.get_manga_name(manga_path))
        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")
        for i in range(len(rows) - 1, -1, -1):
            iter_number = len(rows) - i
            print("{0}) {1}".format(iter_number, rows[i].find("a", href=True).text))

    def save_settings(self, make_composites, keep_originals, composition_type):
        '''
        saves the current settings
        '''
        self.settings = {
            'make_composite': make_composites,
            'keep_originals': keep_originals,
            'composition_type': composition_type
        }
        with open(self.settings_path, 'w') as f:
            json.dump(self.settings, f)
    
    def load_settings(self):
        '''
        load the settings from file
        '''
        with open(self.settings_path, 'r') as f:
            self.settings = json.load(f)

    def settings_exists(self):
        '''
        checks if save file exists
        '''
        return os.path.exists(self.settings_path)

    def verify_settings(self):
        '''
        check validity of loaded settings

        returns True if valid
        '''
        keys = self.settings.keys()
        if len(keys) != 3:
            return False
        for key in keys:
            if key == None:
                return False
        return True