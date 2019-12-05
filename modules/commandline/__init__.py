import argparse


def parse():
    """
    :return: (skip_menu, args)
    """
    parser = argparse.ArgumentParser(description='Tool to download and read manga')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--view', help='skip menu and open viewer directly', action='store_true')
    args = parser.parse_args()

    # update as necessary
    skip_menu = args.view

    return skip_menu, args
