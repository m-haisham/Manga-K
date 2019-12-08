import re

import requests
from bs4 import BeautifulSoup


class MKCodec:
    def __init__(self):
        ''' 
        initialize the object
        '''
        self.search_prefix = 'https://mangakakalot.com/search/'
        self.search_postfix = '?page='

        self.keyword = ''
        self.search_result = []
        self.page_prefix = ''
        self.current_page = 0
        self.max_page = -1

    def previous_page_exists(self):
        return self.current_page != 1

    def next_page_exists(self):
        return self.max_page != -1 and self.current_page + 1 <= self.max_page

    def get_page(self, page: int):
        return f'{self.search_prefix}{self.keyword}{self.search_postfix}{page}'

    def search(self, keyword: str):
        '''
        keyword (string): word or phrase no less than three characters

        returns none

        Searches for the (keyword) on mangakakalot database and updates the variables
        Search result can be accessed as MKCodec.search_result (list)
        '''
        if len(keyword) < len(self.search_prefix) + 3:
            return

        keyword = re.sub(' ', '_', keyword.lower())

        self.keyword = keyword[len(self.search_prefix):]

        r = requests.get(keyword)
        soup = BeautifulSoup(r.content, 'html.parser')

        if '=' in keyword:
            url_fragments = keyword.split('=')
            self.current_page = int(url_fragments[-1])
        else:
            self.current_page = 1
        self._populate(soup)

    def _populate(self, dish):
        '''
        dish (BeautifulSoup): Beautiful soup object

        Parses the data (dish) and extracts information and updates object
        '''
        result_list = dish.find('div', {'class': 'panel_story_list'}).find_all(
            'div', {'class': 'story_item'})
        self.search_result = []
        for result in result_list:
            self.search_result.append({
                'name': result.find('h3', {'class': 'story_name'}).text.strip(' \n'),
                'href': result.find('a')['href']
            })

        try:
            page_list = dish.find('div', {'class': 'group_page'}).find_all('a')
        except AttributeError:
            self.page_prefix = ''
            self.max_page = -1
            return

        self.page_prefix = page_list[0]['href'][:-1]
        self.max_page = int(page_list[-1].text[-2:-1])
