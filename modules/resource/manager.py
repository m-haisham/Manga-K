from pathlib import Path

from .resources import RawResource
from .raw import style


class ResourceManager:
    def __init__(self, resources):
        self.resources = resources

    def check_resources(self):
        for resource in self.resources:
            resource.make()


manager = ResourceManager([
    RawResource(style, Path('style.css'))
])