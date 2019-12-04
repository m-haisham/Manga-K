import json
import os
import re
import shutil

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from modules.ImageStacking import VerticalStack, dir_to_pdf
from modules.static import Const


def make_valid(path):
    return re.sub('[^A-Za-z0-9 -.]+', '', path)

class MangaDownloader:
    def __init__(self):
        self.image_stacker = VerticalStack()
        self.settings_path = 'config.json'
        if self.settings_exists():
            self.load_settings()

    def save_image(self, url, directory):
        """
        url (String): online image file path
        directory (String): Image file save path

        returns: None

        This function downloads [url] and prints the progress of the download to the console and save the file to [directory]
        """
        filename = url.split('/')[-1]
        with open(directory + '/' + filename, 'wb') as f:
            response = requests.get(url, stream=True)

            total_length = response.headers.get('content-length')
            if total_length is None:  # no content length header
                f.write(response.content)
            else:
                total_length = int(total_length)
                length_kb = round(total_length / 1024, 2)
                chunksize = int(total_length / 50)

                with tqdm(desc=f'{filename:<8}',
                          total=total_length,
                          unit='b',
                          unit_scale=True) as pbar:

                    for data in response.iter_content(chunk_size=chunksize):
                        pbar.update(len(data))
                        f.write(data)

    def get_manga_name(self, manga_path):
        """
        manga_path (string): manga path from mangakakalot.com

        return (string): manga title
        """
        r = requests.get(manga_path)
        soup = BeautifulSoup(r.content, "html.parser")
        titlebox = soup.find(class_="manga-info-text")
        return make_valid(titlebox.find("h1").text)

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

    def download_manga(self, url, chapters):
        """
        url (string): manga path from mangakakalot.com
        starting_chapter (int): download start (inclusive)
        ending_chapter (int): download end (exclusive)
        chapter_list (list): optional

        returns None
        """

        manga_dir = os.path.join(
            Const.MangaSavePath, self.get_manga_name(url))

        # Create directories
        if not os.path.exists(Const.MangaSavePath):
            os.mkdir(Const.MangaSavePath)
        if not os.path.exists(manga_dir):
            os.mkdir(manga_dir)
        if self.settings['make_composite']:
            if not os.path.exists(os.path.join(manga_dir, Const.PdfDIr)):
                os.mkdir(os.path.join(manga_dir, Const.PdfDIr))
            if not os.path.exists(os.path.join(manga_dir, Const.JpgDir)):
                os.mkdir(os.path.join(manga_dir, Const.JpgDir))

        for chapter in chapters:
            chapter_name = chapter['name']
            chapter_directory = os.path.join(
                manga_dir, make_valid(chapter_name))

            print(f'\n!{chapter_name}')
            if not os.path.exists(chapter_directory):
                os.mkdir(chapter_directory)  # create chapter_directory
            for page in self.get_page_list(chapter['href']):
                self.save_image(page, chapter_directory)  # save image

            if self.settings['make_composite']:
                print('Attempting composition of %s ... ' % chapter_directory)
                if self.settings['composition_type'] == 'pdf':
                    dir_to_pdf(chapter_directory, os.path.join(manga_dir, Const.PdfDIr))
                elif self.settings['composition_type'] == 'image':
                    self.image_stacker.stack(
                        chapter_directory, os.path.join(manga_dir, Const.JpgDir))
                print("Composition done!")
                if not self.settings['keep_originals']:
                    shutil.rmtree(chapter_directory)  # remove chapter
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
            print("{0}) {1}".format(iter_number,
                                    rows[i].find("a", href=True).text))

    def get_info(self, manga_path):
        """
        manga_path (string): url of manga from mangakakalot.com
        returns None

        prints the information of manga
        """

        info = {
            'name': '',
            'chapters': {}
        }

        r = requests.get(manga_path)
        soup = BeautifulSoup(r.content, "html.parser")
        chapterbox = soup.find_all(class_="chapter-list")
        rows = chapterbox[0].find_all(class_="row")

        info['name'] = self.get_manga_name(manga_path)
        for i in range(len(rows) - 1, -1, -1):
            iter_number = len(rows) - i
            info['chapters'][rows[i].find("a", href=True).text] = {
                'href': rows[i].find("a", href=True)['href']
            }

        return info

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
