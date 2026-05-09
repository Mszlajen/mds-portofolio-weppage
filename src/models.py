from pydantic import BaseModel, Field
from os import listdir
import datetime
from email import utils
from functools import cached_property

class Gallery(BaseModel):
    title: str
    publish_date: str
    image_url: str = ""
    file: str | None = None
    group: str | None = None
    images: 'list[Image]'
    thumbnail: str = Field(default_factory=lambda data: data['images'][0].path)
    alt_text: str = ""
    hide: bool = False

    @cached_property
    def link(self):
        return f"/{self.group}/{self.file}"

    @cached_property
    def pub_date(self):
        nowdt = datetime.datetime.strptime(self.publish_date, '%Y-%m-%d')
        return utils.format_datetime(nowdt)


class Image(BaseModel):
    path: str
    thumbnail: str = Field(default_factory=lambda data: data['path'])
    thumbnail_alt_text: str = ""
    sub_html: str = ""