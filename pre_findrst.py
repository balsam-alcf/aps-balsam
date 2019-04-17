#!/usr/bin/env python
import glob
import os

def imgName(path):
    '''Strip name out of path'''
    return os.path.splitext(os.path.basename(path))[0]

# Create requisite directories in parent folder
dirs = 'cmaps maps amaps grids aligned'.split()
for d in dirs:
    if not os.path.isdir(d): 
        os.makedirs(d)
        print(f"Created {d}")

# Identify folder with *.tif and collect images
image_paths = glob.glob('*/*.tif')
images_dir = list(set([os.path.dirname(p) for p in image_paths]))[0]
image_names = [
    imgName(p) for p in image_paths
    if os.path.dirname(p) == images_dir
]

print(f'Detected {len(image_names)} .tif images in {images_dir}')

# Rename images folder as "./images"
src = os.path.abspath(images_dir)
dest = os.path.abspath('./images')
if src != dest: 
    os.rename(src, dest)
    print(f"Renamed {src} --> {dest}")

# Generate images.lst file
with open('images.lst', 'w') as fp:
    for image_name in image_names:
        fp.write(f'{image_name}\n')
print("Wrote images.lst")

# Generate pairs.lst file
with open('pairs.lst', 'w') as fp:
    for img1, img2 in zip(image_names[:-1], image_names[1:]):
        fp.write(f'{img1} {img2} {img1}_{img2}\n')
print("Wrote pairs.lst")
