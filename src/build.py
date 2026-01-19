from sys import argv
from os import path, makedirs
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


if __name__ == '__main__':
    input_file = argv.get(1, "pages.json")
    output_folder = argv.get(2, "bin")
    templates_folder = argv.get(3, "templates")

    env = Environment(loader=FileSystemLoader(templates_folder), autoescape=select_autoescape())

    with open(input_file) as f:
        all_galleries = load(f)
    
    all_galleries = sorted(((group, 
                             [Gallery.model_validate(gallery | {'group': group}) for gallery in galleries])
                            for group, galleries 
                            in all_galleries.items()), 
                           key=lambda t: t[0], 
                           reverse=True)
    
    flatten_galleries = reduce(lambda acc, v: acc.extend(v[1]) or acc, all_galleries, [])
    recent_galleries = flatten_galleries[:5]

    render_file(env, 'about.html', path.join(output_folder, 'about.html'), about_active=True, recent=recent_galleries)
    render_file(env, 'contact.html', path.join(output_folder, 'contact.html'), contact_active=True, recent=recent_galleries)
    render_file(env, 'newsletter.html', path.join(output_folder, 'newsletter.html'), newsletter_active=True, recent=recent_galleries)

    render_file(env, 'rss.xml', path.join(output_folder, 'rss.xml'), build_date=format_datetime(datetime.now()), galleries=flatten_galleries)
    
    render_file(env, 'index.html', path.join(output_folder, 'index.html'), galleries=flatten_galleries, recent=recent_galleries, home_active = True)

    for group, galleries in all_galleries:
        group_folder = path.join(output_folder, group)
        makedirs(group_folder, exist_ok=True)
        for gallery in galleries:
            render_file(env, 'gallery.html', path.join(group_folder, gallery.file), recent_active = gallery in recent_galleries, recent=recent_galleries, gallery = gallery, load_gallery = True)