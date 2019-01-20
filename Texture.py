import os
import pygame

pygame.display.set_mode((600, 600))


def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        if color_key is not None:
            if color_key is -1:
                color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        return image
    except pygame.error as message:
        print('Cannot load image:', name, message)
