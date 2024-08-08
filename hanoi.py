import pygame
from stack import Stack
from random import randint
import os

WIDTH, HEIGHT = 570, 700

class Hanoi:
    def __init__(self, game, towers, rings=3, shuffled=False):
        self.game = game
        self.screen = game.screen
        self.towers = towers
        self.rings = rings

        self.start = Stack()
        self.pause = False
        self.selected = None

        print(shuffled)
        if not shuffled:
            for val in range(rings, 0, -1):
                ring = Ring(self.screen, val, self.towers.index(0))
                self.start.insert(ring)
            self.towers.index(0).stack = self.start.copy()
        else:
            for val in range(rings, 0, -1):
                ring = Ring(self.screen, val, self.towers.index(0))
                self.start.insert(ring)

            for ring in self.start:
                tower = self.towers.index(randint(0, 2))
                ring.tower = tower
                tower.stack.insert(ring)
        print(self.towers.index(0).stack)
        self.moves = 0
        self.min_moves = (2 ** rings) - 1  # FORMULA
        self.time = 0  # round(self.min_moves * 1.5)

    def update(self, events):
        for i in self.towers:
            if i == self.selected:
                #Using surface for SRCALPHA instead of Rect, this is to manipulate the opacity
                hitbox_surface = pygame.Surface((i.hitbox_rect.width, i.hitbox_rect.height), pygame.SRCALPHA)
                # Fill the surface with a semi-transparent color
                hitbox_surface.fill((255, 255, 255, 128))
                # Blit the surface onto the screen at the position of the hitbox
                self.screen.blit(hitbox_surface, i.hitbox_rect.topleft)
            i.update()

        if not self.pause:
            self.time += self.game.delta
            for event in events:
                for tower in self.towers:
                    if event.type == pygame.MOUSEBUTTONUP and tower.hitbox_rect.collidepoint(
                            pygame.mouse.get_pos()) and self.selected is None and len(tower.stack) != 0:
                        self.selected = tower
                        self.game.sfx['select'].play()
                    elif event.type == pygame.MOUSEBUTTONUP and tower.hitbox_rect.collidepoint(
                            pygame.mouse.get_pos()) and self.selected is not None:
                        if len(tower.stack) == 0:
                            ring = self.selected.stack.get()
                            ring.tower = tower
                            tower.stack.insert(ring)
                            self.game.sfx['meow'].play()

                        elif tower.stack.getLast().value > self.selected.stack.getLast().value:
                            ring = self.selected.stack.get()
                            ring.tower = tower
                            tower.stack.insert(ring)
                            self.game.sfx['meow'].play()

                        else:
                            self.selected = None
                            self.game.sfx['wrong'].play()
                            continue

                        self.selected = None
                        self.moves += 1


class Tower:
    def __init__(self, screen, stack):
        self.screen = screen
        self.stack = stack
        self.image = pygame.image.load('images/game/tower.png')
        self.image_rect = self.image.get_rect()
        self.hitbox_rect = pygame.Rect(self.image_rect.x, self.image_rect.y, 175, self.image_rect.height)

    def update(self):
        self.screen.blit(self.image, pos(self.image_rect))
        for i in self.stack.inverse():
            i.update()


class Ring:
    def __init__(self, screen, value, tower):
        self.screen = screen
        self.tower = tower
        self.value = value
        image = pygame.image.load(f"images/game/cats/cat{self.value}.png")
        self.image = scale(image, (130, 60))
        self.image_rect = self.image.get_rect()

    def update(self):
        self.image_rect.x, self.image_rect.y = self.tower.image_rect.x - (self.image_rect.width // 2 - self.tower.image_rect.width // 2), HEIGHT - (
                    self.tower.stack.getIndex(self) * (self.image_rect.height - 10)) - 100

        self.screen.blit(self.image, pos(self.image_rect))


def pos(rect):
    return rect.x, rect.y


def scale(image, size):
    w, h = image.get_size()
    sc = min(size[0] / w, size[1] / h)

    new_w = int(w * sc)
    new_h = int(h * sc)

    new_image = pygame.transform.scale(image, (new_w, new_h))
    return new_image


if __name__ == '__main__':
    os.system('cls')
    os.system('py main.py')
