from pathlib import Path

from .raw import style, script
from .resources import RawResource


class ResourceManager:
    def __init__(self, resources):
        self.resources = resources

    def check_resources(self):
        for resource in self.resources:
            resource.make()


manager = ResourceManager([
    RawResource(style, Path('Web') / Path('style.css')),
    RawResource(script, Path('Web') / Path('script.js'))
])