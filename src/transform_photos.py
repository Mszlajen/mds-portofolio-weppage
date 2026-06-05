import os
import subprocess

if __name__ == '__main__':
    input_folder = input("Input Folder: ")
    output_folder = input(f"Output Folder ({input_folder}): ") or input_folder
    quality = int(input("Quality (30): ") or "30")
    thumbnail_scale = int(input("Thumbnail Scale (20): ") or "20")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(os.path.join(output_folder, "thumbnails")):
        os.makedirs(os.path.join(output_folder, "thumbnails"))

    for folder, _, files in list(os.walk(input_folder)):
        for filename in files:
            new_name = filename.replace('\r', '').replace('\n', '').rsplit('.', 1)[0]
            new_name = f"{folder_part}_{new_name}" if (folder_part := folder[len(input_folder) + 1:]) else new_name
            #subprocess.run(["gm", "convert", os.path.join(folder, filename), "-auto-orient", "-quality", str(quality), os.path.join(output_folder, f"{new_name}.webp")])
            subprocess.run(["gm", "convert", os.path.join(folder, filename), "-scale", f"{thumbnail_scale}x{thumbnail_scale}%", os.path.join(output_folder, "thumbnails", f"{new_name}.webp")])