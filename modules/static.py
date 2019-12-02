import os


class Const:
    MangaSavePath = 'Manga'
    StyleSaveFile = 'style.css'
    StructFile = 'tree.json'

    PdfDIr = 'pdf'
    JpgDir = 'jpd'

    @staticmethod
    def createCompositionDirs(manga_dir):
        if not os.path.exists(os.path.join(manga_dir, Const.PdfDIr)):
            os.mkdir(os.path.join(manga_dir, Const.PdfDIr))
        if not os.path.exists(os.path.join(manga_dir, Const.JpgDir)):
            os.mkdir(os.path.join(manga_dir, Const.JpgDir))
