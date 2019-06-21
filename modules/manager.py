from yattag import Doc
import webbrowser
import os
import json

import re
from modules.static import Const
numbers = re.compile(r'(\d+)')

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

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



class MangaManager():
    def __init__(self):
        self.manga_path = Const.MangaSavePath
        self.tree = {}

    def generate_tree(self):

        # Get all manga directories
        dirs = self.get_dirs(self.manga_path)[0]


        for i in range(len(dirs)): 

            # get all downloaded chapter directories for the manga
            shallow_dirs = self.get_dirs(os.path.join(self.manga_path, dirs[i]))[0]
            self.remove_composite_dir(shallow_dirs)

            self.tree[dirs[i]] = {}

            for j in range(len(shallow_dirs)):

                # get all page files of the chapter
                deep_files = self.get_dirs(os.path.join(self.manga_path, dirs[i], shallow_dirs[j]))[1]

                self.tree[dirs[i]][shallow_dirs[j]] = sorted(deep_files, key=numericalSort)

        with open('tree.json', 'w') as f:
            json.dump(self.tree, f)

    def get_dirs(self, path):
        '''
        Seperates the files and folders of directory
        '''
        full_list = os.listdir(path)

        dir_list = []
        files_list = []
        for i in full_list:
            if os.path.isdir(os.path.join(path, i)):
                dir_list.append(i)
            else:
                files_list.append(i)

        return dir_list, files_list

    def remove_composite_dir(self, dirs):
        if 'Composites' in dirs:
            dirs.remove('Composites')

class HtmlManager:
    def __init__(self):
        self.manga_path = Const.MangaSavePath
        self.location = 'Web'
        self.main_menu = os.path.join(self.location, 'index.html')

    def generate_new_chapter(self, manga_title, chapter_title, page_list, destination, prefix='', previous = '#', next = '#'):
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        doc.asis('<html lang="en" dir="ltr">')
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<link rel="stylesheet" href="../../style.css">')
            with tag('title'):
                text(manga_title + ' - ' + chapter_title)
        with tag('body'):
            with tag('div', klass='container'):
                with tag('div', klass='title-container'):
                    doc.asis('<a class="title manga-title" href="' + os.path.join('..', manga_title + '.html') + '" >' + manga_title + '</a>')
                with tag('div', klass='chapter-bar'):
                    doc.asis('<a class="btn btn-left btn-1 btn-1d" href="' + previous + '">Previous</a>')
                    with tag('h3', klass='title chapter-title'):
                        text(chapter_title)
                    doc.asis('<a class="btn btn-right btn-1 btn-1d" href="' + next + '">Next</a>')

                for page in page_list:
                    doc.stag('img', src=self.verify_source(os.path.join(prefix, page)), klass='page')

                with tag('div', klass='chapter-bar'):
                    doc.asis('<a class="btn btn-left btn-1 btn-1d" href="' + previous + '">Previous</a>')
                    with tag('h3', klass='title chapter-title'):
                        text(chapter_title)
                    doc.asis('<a class="btn btn-right btn-1 btn-1d" href="' + next + '">Next</a>')
        doc.asis('</html>')

        with open(destination, 'w') as f:
            f.write(doc.getvalue())

    def generate_list(self, title, mlist, destination, is_manga_list = True):
        doc, tag, text = Doc().tagtext()

        doc.asis('<!DOCTYPE html>')
        doc.asis('<html lang="en" dir="ltr">')
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<link rel="stylesheet" href="../style.css">')
            with tag('title'):
                text(title if is_manga_list else title + '- Chapter list')
        with tag('body'):
            with tag('div', klass='container'):
                if not is_manga_list:
                    doc.asis('<a class="btn btn-left btn-1 btn-1d" href="index.html">Menu</a>')
                with tag('div', klass='title-container'):
                    with tag('h1', klass='title manga-title'):
                        text(title)
                with tag('ul'):
                    for item in mlist:
                        if is_manga_list:
                            link = item + '.html'
                        else:
                            link = os.path.join(title, item + '.html')
                        with tag('li', klass='manga'):
                            self.button(doc, link, item)

        doc.asis('</html>') 

        with open(destination, 'w') as f:
            f.write(doc.getvalue())

    def generate_web(self, dir_tree):
        
        # generate manga list
        all_manga_keys = list(dir_tree.keys())
        if not os.path.exists(self.location):
            os.mkdir(self.location)

        self.generate_list('Manga list', all_manga_keys, self.main_menu)
        
        for i in range(len(all_manga_keys)):
            manga_key = all_manga_keys[i]
            all_chapters_keys = list(dir_tree[manga_key].keys())

            self.generate_list(manga_key, all_chapters_keys, os.path.join(self.location, manga_key+'.html'), is_manga_list=False)

            
            save_location = os.path.join(self.location, manga_key)
            if not os.path.exists(save_location):
                os.mkdir(save_location)
            for i in range(len(all_chapters_keys)):
                chapter_key = all_chapters_keys[i]

                next_link = os.path.join(all_chapters_keys[(i + 1) % len(all_chapters_keys)] + '.html')
                previous_link = os.path.join(all_chapters_keys[(i - 1) % len(all_chapters_keys)] + '.html')

                self.generate_new_chapter(manga_key, chapter_key, dir_tree[manga_key][chapter_key],
                                        os.path.join(save_location, chapter_key + '.html'),
                                        os.path.join('..', '..', self.manga_path, manga_key, chapter_key),
                                        next=next_link, previous=previous_link)

    def open(self):
        webbrowser.open('file://'+os.path.realpath(self.main_menu))

    def button(self, doc, href, text):
        doc.asis('<a class="btn btn-1 btn-1d" href="' + href + '">' + text + '</a>')

    def verify_source(self, source):
        new = re.sub(r'[ ]', '%20', source)
        return new

if __name__ == '__main__':
    
    html = HtmlManager()

    manga = MangaManager()
    manga.generate_tree()

    mangas_list = list(manga.tree.keys())

    manga_title = mangas_list[2]
    chapter_dict = manga.tree[manga_title]
    chapter = list(chapter_dict.keys())[0]
    page_list = chapter_dict[chapter]
    
    html.generate_web(manga.tree)