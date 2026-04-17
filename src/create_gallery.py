from models import Gallery, Image
from os import listdir, path, makedirs
from json import dump
from datetime import date

if __name__ == '__main__':
    today = date.today()

    while not (name := input('Name: ')): ...
    escaped_name = name.replace(' ', '_').lower()
    default_folder = path.join('bin', 'images', name.lower())
    input_folder = input(f'Input folder ({default_folder}): ') or default_folder
    published_date = input(f'Published date ({today.isoformat()}): ') or today.isoformat()
    storage_folder = input(f'Storage folder ({name.lower()}): ') or name.lower()
    html_file = input(f'Html file ({escaped_name}.html)') or f"{escaped_name}.html"
    default_output = path.join("src", "pages", f"{today.year}{today.month:02d}")
    output_folder = input(f'Output folder ({default_output}): ') or default_output
    
    images = [Image(src=f'/images/{storage_folder}/{f}').model_dump() for f in sorted(listdir(input_folder))]
    gallery = Gallery(title = name, publish_date=published_date, file = html_file, images = images)

    makedirs(output_folder, exist_ok=True)
    group_max = int(max(listdir(output_folder) + ['0_']).split('_', 1)[0])
    with open(path.join(path.join(output_folder, f'{group_max + 1}_{escaped_name}.json')), 'w', encoding='utf-8') as f:
        dump(gallery.model_dump(), f, indent = 4)