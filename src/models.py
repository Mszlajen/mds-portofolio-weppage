from pydantic import BaseModel, Field
from os import listdir, path
from functools import cached_property

class Gallery(BaseModel):
    title: str
    file: str | None = None
    group: str | None = None
    images_folder: str = ""
    images_path: str = ""
    images: 'list[Image]' = Field(default_factory=lambda data: [Image(src = f"{data['images_path']}/{filename}") for filename in listdir(data["images_folder"])])
    thumbnail: str = Field(default_factory=lambda data: data['images'][0].src)
    alt_text: str = ""

    @cached_property
    def link(self):
        return f"{self.group}/{self.file}"

class Image(BaseModel):
    src: str
    thumbnail: str = Field(default_factory=lambda data: data['src'])
    thumbnail_alt_text: str = ""
    sub_html: str = ""