from modules.sorting.alphabetic import alphabetic_prompt_list
from modules.console.menu import Menu

from whaaaaat import Separator, prompt
from modules.ui import Loader


class UpdatesMenu:
    def __init__(self, updates: dict):
        self.updates = updates
        self.informative = {f'{key.title} ({len(self.updates[key])})': self.updates[key] for key in self.updates.keys()}

        mangas = list(self.informative.keys())

        manga_prompt_list = alphabetic_prompt_list([manga for manga in mangas])

        # exit options
        manga_prompt_list.extend([Separator(' '), 'Exit'])
        self._menu = Menu("Updates", manga_prompt_list)

    def prompt(self):
        # choose a manga
        manga_title = self._menu.prompt()

        if manga_title == 'Exit':
            return

        # construct new checbox menu for this
        checkbox_choices = [{'name': chapter.title} for chapter in self.informative[manga_title]]
        selected_names = prompt(dict(
            type='checkbox',
            name='updates',
            message=manga_title,
            choices=checkbox_choices
        ))['updates']

        # nothing selected
        if not selected_names:
            return

        selected = list(filter(lambda chapter: chapter.title in selected_names, self.informative[manga_title]))
        manga = list(filter(lambda key: self.updates[key] == self.informative[manga_title], self.updates.keys()))[0]

        with Loader("Parse Info"):
            manga, all_chapters = manga.parse()

        from modules.database.models.manga.download import selective_download
        selective_download(manga, all_chapters, selected, update=False)

