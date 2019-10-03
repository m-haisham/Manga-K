import os

from modules.conversions import create_py_list
from modules.static import Const

if __name__ == "__main__":
    if not os.path.exists(Const.StyleSaveFile):
        print('{0} does not exist, run while it exists'.format(
            Const.StyleSaveFile))
        print('Running main.py will regenerate {0} saved as style.py'.format(
            Const.StyleSaveFile))
        input('Press enter to exit')
    else:
        create_py_list(Const.StyleSaveFile,
                       os.path.join('modules', 'styles.py'))
        print('{0} regenerated'.format(Const.StyleSaveFile))
        input('Enter to continue . . .')
