from pathlib import Path

from modules.resource import RawResource
from modules.resource.raw import style


class ResourceManager:
    def __init__(self, resources):
        self.resources = resources

    def check_resources(self):
        for resource in self.resources:
            resource.make()


manager = ResourceManager([
    RawResource(style, Path('style.css'))
])