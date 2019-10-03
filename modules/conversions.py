def create_py_list(path, destination, plist='style'):
    '''
    path (string): path of css file
    destination (string): path of file to save

    reads all lines from a file and makes a python file which has all of them in a list called style
    '''
    declaration = plist+' = []\n'
    lines = [line for line in open(path)]

    with open(destination, 'w') as f:
        f.write(declaration)
        for line in lines:
            f.write('''%s.append('%s')\n''' % (plist, line.strip()))


def list_to_file(_list, destination):
    '''
    _list (list): list with strings
    destination (string): path of file to save

    takes a list and writes each item into (destination)
    '''
    with open(destination, 'w') as f:
        for line in _list:
            f.write(line)


if __name__ == "__main__":
    create_py_list('keybinding.js', 'keybinding.py', 'keybinding')
