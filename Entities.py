from Tools import *
from math import sin, cos, radians


class BaseEntity(pygame.sprite.Sprite):
    RIGHT, UP, LEFT, DOWN = 0, 1, 2, 3  # Константы направления
    ANGLE = 90  # Угол поворота

    EntityImage = load_image("NoneTexture.png")  # Стандартная текстура

    def __init__(self, x, y, group, direction=UP):
        super().__init__(group)
        self.direction = direction  # Установка направления
        self.group = group

        self.image = pygame.transform.rotate(self.EntityImage, BaseEntity.ANGLE * self.direction)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.hp = 100  # Очки прочности
        self.speed = 0  # Максимальная скорость
        self.is_moving = False  # Движение танка
        self.forbidden = None

    def update(self, solid_blocks, entities):
        collision = pygame.sprite.spritecollideany(self, entities) not in (None, self) or \
                    pygame.sprite.spritecollideany(self, solid_blocks) is not None
        if collision:
            if self.forbidden is None:
                self.forbidden = self.direction
            if self.direction == self.forbidden:
                self.is_moving = False
        else:
            self.forbidden = None

        if self.is_moving and self.direction != self.forbidden:
            dx = cos(radians(BaseEntity.ANGLE * self.direction)) * self.speed  # Расчет проекции на Ox
            dy = - (sin(radians(BaseEntity.ANGLE * self.direction)) * self.speed)  # Расчет проекции на Oy
            self.rect = self.rect.move(dx, dy)

    def get_event(self, event):
        pass

    def set_direction(self, direction):  # Смена направления
        self.direction = direction
        self.image = pygame.transform.rotate(self.EntityImage, BaseEntity.ANGLE * self.direction)


class Player(BaseEntity):  # Игрок
    EntityImage = load_image("PlayerTank.png")

    def __init__(self, *args):
        super().__init__(*args)
        self.speed = 3

    def shoot(self):  # Стрельба
        Bullet(self, self.rect.x, self.rect.y)

    def get_event(self, event):  # Обработка событий
        self.is_moving = True
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            self.shoot()
        elif key[pygame.K_w]:
            self.set_direction(self.UP)
        elif key[pygame.K_s]:
            self.set_direction(self.DOWN)
        elif key[pygame.K_d]:
            self.set_direction(self.RIGHT)
        elif key[pygame.K_a]:
            self.set_direction(self.LEFT)
        else:
            self.is_moving = False


class Enemy(BaseEntity):  # Противник
    EntityImage = load_image("EnemyTank.png")


class Bullet(BaseEntity):  # Снаряд
    EntityImage = load_image("Bullet.png")

    def __init__(self, owner, x, y):
        super().__init__(x, y, owner.group, direction=owner.direction)
        self.owner = owner
        self.speed = 8
        self.is_moving = True

    def update(self, solid_blocks, entities):
        pass


class Fortifying(BaseEntity):  # Существо, описывающее базу (для победы надо уничтожить)
    EntityImage = load_image("Fortifying.png")
