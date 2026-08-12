from typing import Literal
from sys import argv
from os import path, makedirs, walk
from json import load
from jinja2 import Environment, FileSystemLoader, select_autoescape
from models import Gallery
from functools import reduce
from datetime import datetime
from email.utils import format_datetime

argv = {i: value for i, value in enumerate(argv)}

def render_file(env: Environment, template: str, output: str, **kwargs):
    render = env.get_template(template).render(**kwargs)
    with open(output, "w") as f:
        f.write(render)

def bool_input(prompt: str, default: Literal['y', 'n']) -> bool:
    while True:
        answer = input(f"{prompt} ({default}): ").lower() or default
        if answer == 'y':
            return True
        elif answer == 'n':
            return False

def input_value(msg: str, default: str) -> str:
    return input(f'{msg} ({default}): ') or default

def json_load(file_path: str) -> dict:
    with open(file_path) as f:
        return load(f)

if __name__ == '__main__':
    update_rss = bool_input('Update RSS Feed', 'y')
    input_files = input_value('Configuration folder', path.join('src', 'pages'))
    output_folder = input_value('Output folder', 'bin')
    templates_folder = input_value('Template folder', path.join('src', 'templates'))
    main_url = input_value('Main url', 'https://matias-sz.work')
    title = input_value('Base title', 'Matias Szlajen')

    env = Environment(loader=FileSystemLoader(templates_folder), autoescape=select_autoescape())
    
    all_galleries = sorted(((folder.rsplit(path.sep, 1)[-1],
                             [Gallery.model_validate(json_load(path.join(folder, file)) | {'group': folder.rsplit(path.sep, 1)[-1]})])
                            for folder, _, files in list(walk(input_files)) for file in files),
                           key=lambda t: t[0], 
                           reverse=True)
    
    flatten_galleries = reduce(lambda acc, v: acc.extend(v[1]) or acc, all_galleries, [])
    recent_galleries = flatten_galleries[:5]

    render_file(env, 'about.html', path.join(output_folder, 'about.html'), about_active=True, recent=recent_galleries, title=title, main_url=main_url, file='about.html')
    render_file(env, 'contact.html', path.join(output_folder, 'contact.html'), contact_active=True, recent=recent_galleries, title=title, main_url=main_url, file='contact.html')
    render_file(env, 'newsletter.html', path.join(output_folder, 'newsletter.html'), newsletter_active=True, recent=recent_galleries, title=title, main_url=main_url, file='newsletter.html')

    render_file(env, 'custom.js', path.join(output_folder, 'js', 'custom.js'), recent=recent_galleries)

    if update_rss:
        render_file(env, 'rss.xml', path.join(output_folder, 'rss.xml'), build_date=format_datetime(datetime.now()), galleries=flatten_galleries)
    
    render_file(env, 'index.html', path.join(output_folder, 'index.html'), galleries=flatten_galleries, recent=recent_galleries, home_active = True, title=title, main_url=main_url, file='index.html')

    for group, galleries in all_galleries:
        group_folder = path.join(output_folder, group)
        makedirs(group_folder, exist_ok=True)
        for gallery in galleries:
            render_file(env, 'gallery.html', path.join(group_folder, gallery.file), recent_active = gallery in recent_galleries, gallery = gallery, load_gallery = True, title=f"{gallery.title} - {title}", main_url=main_url, file='/'.join((group, gallery.file)))