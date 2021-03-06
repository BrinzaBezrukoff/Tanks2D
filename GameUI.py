from Tools import *


class BaseForm (pygame.sprite.Group):
    background_image = None

    def __init__(self, x, y, w, h, bg_color=pygame.Color("Gray")):
        super(BaseForm, self).__init__()
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.bg_color = bg_color
        self.image = self.background_image

    def add(self, *sprites):
        super(BaseForm, self).add(*sprites)
        for element in sprites:
            element.rect.x = self.x + element.x
            element.rect.y = self.y + element.y

    def draw(self, surface):
        if not self.image:
            pygame.draw.rect(surface, self.bg_color, (self.x, self.y, self.w, self.h))
        else:
            surface.blit(self.image, (0, 0))
        super(BaseForm, self).draw(surface)

    def get_event(self, event):
        for element in self.sprites():
            element.get_event(event)


class BaseElement (pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        super(BaseElement, self).__init__()
        self.w, self.h = w, h
        self.x, self.y = x, y
        self.color = color

        self.image = pygame.Surface((self.w, self.h))
        if color:
            pygame.draw.rect(self.image, self.color, (0, 0, self.w, self.h))
        self.rect = self.image.get_rect()

    def get_event(self, event):
        pass


class Label(BaseElement):
    def __init__(self, *args, **kwargs):
        super(Label, self).__init__(*args, **kwargs)
        self.image = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect((self.x, self.y, self.w, self.h))


class MessageBox (BaseForm):
    def __init__(self, message, *args, **kwargs):
        super(MessageBox, self).__init__(*args, **kwargs)
        self.message = message

    def draw(self, surface):
        super(MessageBox, self).draw(surface)
        text_x = self.w // 2 - self.message.get_width() // 2
        surface.blit(self.message, (self.x + text_x, self.y))
        for button in self.sprites():
            surface.blit(button.image, (button.rect.x, button.rect.y))


class Button (BaseElement):
    def __init__(self, name, button_text, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)

        text_x = self.w // 2 - button_text.get_width() // 2
        text_y = self.h // 2 - button_text.get_height() // 2

        self.image.blit(button_text, (text_x, text_y))
        self.rect.x = self.x
        self.rect.y = self.y
        self.name = name

    def on_click(self):
        return self.name


class MapButton (Button):
    pattern = "{} MAP"

    def __init__(self, map_id, x, y, w, h, color):
        button_text = text(MapButton.pattern.format(map_id), pygame.Color("Black"))
        super(MapButton, self).__init__(x=x, y=y, w=w, h=h, name=map_id, button_text=button_text, color=color)


class Menu (BaseForm):
    background_image = load_background("MenuBackground.jpg")

    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        self.selected = None

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for element in self.sprites():
                if element.rect.collidepoint(event.pos) and isinstance(element, Button):
                    return element.on_click()


class MainMenu (Menu):
    def __init__(self, *args, **kwargs):
        super(MainMenu, self).__init__(*args, **kwargs)
        start_game = Button("start_game", text("Начать игру", pygame.Color("Black")),
                            200, 100, 200, 100, pygame.Color("Gray"))
        instruction = Button("instructions", text("Инструкции", pygame.Color("Black")),
                             200, 300, 200, 100, pygame.Color("Gray"))
        self.add(start_game)
        self.add(instruction)


class LevelMenu(Menu):
    def __init__(self, *args, **kwargs):
        super(LevelMenu, self).__init__(*args, **kwargs)
        size = (89, 89)
        counter = 0
        for y in range(50, 468, 139):
            for x in range(50, 468, 139):
                counter += 1
                self.add(MapButton(counter, x, y, *size, pygame.Color("Gray")))


class InstructionsMenu (Menu):
    def __init__(self, *args, **kwargs):
        super(InstructionsMenu, self).__init__(*args, **kwargs)
        red_text = ["Красный игрок:", "^ - Вперед", "< - Влево",
                    "v - Вниз", "> - Вправо", "Enter - Выстрел", "Escape - Меню"]
        green_text = ["Зеленый игрок: ", "W - Вперед", "A - Влево",
                      "S - Вниз", "D - Вправо", "Пробел - Выстрел", "Escape - Меню"]
        red_instructions = Label(100, 150, 200, 400, None)
        green_instructions = Label(358, 150, 200, 400, None)
        self.add(red_instructions)
        self.add(green_instructions)

        y = 0
        for num in range(len(red_text)):
            red_instructions.image.blit(text(red_text[num], pygame.Color("Red")), (0, y))
            green_instructions.image.blit(text(green_text[num], pygame.Color("Green")), (0, y))
            y += 30
