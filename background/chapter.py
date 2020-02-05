from pathlib import Path

import requests


class ChapterDownload:
    def __init__(self, m_download, pause, exit):
        self.model = m_download
        self.path = Path(self.model.thumbnail_path)

        self.pause = pause
        self.exit = exit

        self.path.mkdir(parents=True, exist_ok=True)

    def start(self):
        responses = []
        total_length = 0

        model_pages = []

        # full length
        for page in self.model.pages:
            url = page.url
            response = requests.head(url)

            try:
                total_length += int(response.headers.get('content-length'))
            except TypeError:
                continue
            else:
                responses.append(response)
                model_pages.append(page)

        self.model.max = total_length
        self.model.value = 0

        # download stream
        for i, page in enumerate(model_pages):
            path = self.path / Path(f'{i + 1}.jpg')

            response = requests.get(page.url, stream=True)
            with path.open('wb') as f:
                chunksize = int(total_length / 100)
                for data in response.iter_content(chunk_size=chunksize):
                    self.model.value += len(data)
                    f.write(data)

                    print(self.model.value / self.model.max)

                    while self.pause.value:
                        if self.exit.value:
                            return

                    if self.exit.value:
                        return
