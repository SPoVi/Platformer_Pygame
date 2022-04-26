from os import walk
import pygame

'''walk(top, topdown = True, onerror=None, followLinks=False
    >> 3-tuple: (dirpath, dirnames, filenames)
    dirnames: subfolders. Folders inside dirpath'''

def import_folder(path):
    surface_list = []

    for dirpath,dirnames,filenames in walk(path):
        # This logic will import everything, so make sure you only have images in the folder
        for image in filenames:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


