def create_py_list(path, destination):
    '''
    path (string): path of css file
    destination (string): path of file to save

    reads all lines from a file and makes a python file which has all of them in a list called style
    '''
    declaration = 'style = []\n'
    lines = [line.rstrip() for line in open(path)]

    with open(destination, 'w') as f:
        f.write(declaration)
        for line in lines:
            f.write('style.append("%s")\n' % line)

def list_to_file(_list, destination):
    '''
    _list (list): list with strings
    destination (string): path of file to save

    takes a list and writes each item into (destination)
    '''
    with open(destination, 'w') as f:
        for line in _list:
            f.write(line)