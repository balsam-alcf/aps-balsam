#!/usr/bin/env python
from balsam.launcher.dag import current_job
import glob
import os

def imgName(path):
    '''Strip name out of path'''
    return os.path.splitext(os.path.basename(path))[0]

# Create requisite directories in parent folder
images_dir = current_job.data['images_dir']
os.symlink(images_dir, 'images')
print(f"Created symlink images/ --> {images_dir}")

dirs = 'cmaps maps amaps grids aligned'.split()
for d in dirs:
    if not os.path.isdir(d): 
        os.makedirs(d)
        print(f"Created {d}")

# Identify folder with *.tif and collect images
image_paths = glob.glob('images/*.tif')
image_names = sorted([
    imgName(p) for p in image_paths
])

print(f'Detected {len(image_names)} .tif images')

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
