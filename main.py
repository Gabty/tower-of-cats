import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button, ButtonArray
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox

from hanoi import Hanoi, Tower
from stack import Stack

import json

import os

import time
from abc import ABC, abstractmethod

pygame.init()
WIDTH, HEIGHT = 570,700

pygame.display.set_caption("Tower of Cats")

class Scene(ABC):
    @abstractmethod
    def run(self):
        pass
    
    @abstractmethod
    def destroy(self):
        pass

class SceneManager:
    def __init__(self, scene):
        self.__scene = scene
    
    def get_scene(self):
        return self.__scene
    
    def set_scene(self, scene):
        print("---")
        if self.__scene:
            self.__scene.destroy()
        self.__scene = scene
        for i in pygame_widgets.WidgetHandler()._widgets:
            print(i)
    
    def update(self, events):
        self.__scene.run(events)

class MainMenu(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 78)
        self.title = self.font.render("Tower of Cats", True, (100,155,240))
        
        self.buttons = [
            Button(self.game.screen, WIDTH/2 - 300/2, 200,300,100,radius=50, text='Play',fontSize=64, onRelease=lambda: game.gamescene.set_scene(GameSelection(game))),
            Button(self.screen, WIDTH/2 - 300/2, 300,300,100,radius=50,text="Options",fontSize=64, onRelease=lambda: game.gamescene.set_scene(Settings(game))),
            Button(self.screen, WIDTH/2 - 300/2, 400,300,100,radius=50,text="Leaderboard",fontSize=56, onRelease=lambda: game.gamescene.set_scene(Leaderboard(game))),
            Button(self.screen, WIDTH/2 - 300/2, 500,300,100,radius=50, onRelease=lambda: game.quit(),text="Quit",fontSize=64)
        ]
        
        #self.button_arrays = ButtonArray(self.screen, WIDTH/2 - 300/2, 250, 300,400, (1,4),colour=(255,255,255), separationThickness=8, texts=("Play", "Options","Leaderboard","Quit"), fontSizes=(64,64,52,64))

        self.mouse = pygame.mouse

    
    def run(self, events):
        self.screen.blit(self.title, (WIDTH/2 - self.title.get_width()/2,100))

    def destroy(self):
        for i in self.buttons:
            pygame_widgets.WidgetHandler().removeWidget(i)
    
class Settings(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        center = WIDTH/2
        #self.back_button = Button(self.screen, (center+center/2)-200/2,HEIGHT-125, 200,100, text="Back",fontSize=64, onClick=lambda: game.gamescene.set_scene(MainMenu(game)),radius=100//2)
        self.widgets ={
            "bgm": Slider(self.screen, WIDTH//2-400//2,340, 400, 10, min=0, max=100, initial=100, handleRadius=15),
            "sfx":Slider(self.screen, WIDTH//2-400//2,460, 400, 10, min=0, max=100, initial=100, handleRadius=15),
            "text":TextBox(self.screen, WIDTH//2 - 100//2, 380, 100, 30, fontSize=16),
            "back": Button(self.screen, center-200/2,HEIGHT-125, 200,100, text="Back",fontSize=64, onClick=self.back,radius=100//2)
        }
        
        fontLabel = pygame.font.Font(None, 64)
        title = pygame.font.Font(None, 96)



        self.bgm_label = fontLabel.render("Background Music", True, (220,200,255))
        self.sfx_label = fontLabel.render("Sound Effects", True, (220,200,255))
        self.settings_title = title.render("Settings", True, (0,0,0))

        self.open()
    
    def run(self, events):
        self.screen.blit(self.bgm_label, (WIDTH/2 - self.bgm_label.get_width()/2,280))
        self.screen.blit(self.sfx_label, (WIDTH/2 - self.sfx_label.get_width()/2,400))
        self.screen.blit(self.settings_title, (WIDTH/2 - self.settings_title.get_width()/2,100))

        self.widgets['text'].setText(str(self.widgets['bgm'].getValue()))
    
    def open(self):
        if not os.path.exists('settings.json'):
            with open('settings.json', 'w+') as file:
                file.write('{"bgm": 100, "sfx": 100}')
        with open('settings.json', 'r+') as file:
            data = json.load(file)
        print(data)
        self.widgets['bgm'].setValue(data['bgm'])
        self.widgets['sfx'].setValue(data['sfx'])
    
    def back(self):
        data = {"bgm": self.widgets['bgm'].getValue(), "sfx": self.widgets['sfx'].getValue()}
        with open('settings.json', 'w+') as file:
            json.dump(data, file)
        

        self.game.bgm.set_volume(data['bgm']/100) # change volume
        
        self.game.gamescene.set_scene(MainMenu(self.game)) # change scene
    
    def destroy(self):
        for key, stat in self.widgets.items():
            pygame_widgets.WidgetHandler().removeWidget(stat)

class GameSelection(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        center = WIDTH/2
        self.widgets = {
            "slider":Slider(self.screen, WIDTH//2-260//2,300, 260,75, min=1, max=9, handleRadius= 30, initial=0,step=1),
            "slider2":Slider(self.screen, WIDTH//2-260//2,400, 260,75, min=0, max=5, handleRadius= 30, initial=0, step=0.1),
            "toggle":Toggle(self.screen, WIDTH//2 - 75//2, 500, 75,50, handleRadius=25),
            "button":Button(self.screen, center/2-260/2, 600,260,100, onRelease=lambda: game.gamescene.set_scene(MainMenu(game))),
            "button2":Button(self.screen, (center + center/2) - 260/2, 600,260,100, onRelease=self.switch_to_game)
        }
    
    def run(self, events):
        pass
    
    def switch_to_game(self):
        self.game.gamescene.set_scene(TowerCats(game, rings=self.widgets['slider'].getValue(), shuffle=self.widgets['toggle'].getValue()))

    def destroy(self):
        for i,v in self.widgets.items():
            pygame_widgets.WidgetHandler().removeWidget(v)

class Leaderboard(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.content_height = 2000
        self.surface = pygame.Surface((WIDTH, self.content_height))
        self.surface.fill((255,255,255))
        self.widgets = []
        self.y_scroll = 0
        for i in range(50):
            x = i
            self.widgets.append(Button(self.surface, 10,i*50+10, 100,40, text=str(i), onRelease=print, onReleaseParams=([i])))
    
    def run(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.y_scroll -= event.y * 20
                self.y_scroll = max(0,min(self.y_scroll, self.content_height - HEIGHT))
        self.screen.blit(self.surface, (0, -self.y_scroll))
    def destroy(self):
        pass

class TowerCats(Scene):
    def __init__(self, game, rings, shuffle=False):
        self.game = game
        self.screen = game.screen
        # Initialize Towers VERY COMPLICATED do not touch :) or else

        # many useless variables
        lefterTower = Tower(self.game.screen,Stack())
        midTower = Tower(self.game.screen,Stack())
        righterTower = Tower(self.game.screen,Stack())
        modidier = 50
        center = WIDTH//2
        left = center/2 - modidier
        right = center + center/2 + modidier
        lefterTower.image_rect.center = (left-lefterTower.image_rect.width//2, HEIGHT-lefterTower.image_rect.height)
        midTower.image_rect.center = (center-lefterTower.image_rect.width//2, HEIGHT-lefterTower.image_rect.height)
        righterTower.image_rect.center = (right-lefterTower.image_rect.width//2, HEIGHT-lefterTower.image_rect.height)

        lefterTower.image_rect.x, lefterTower.image_rect.y = left-lefterTower.image_rect.width//2, HEIGHT-lefterTower.image_rect.height
        midTower.image_rect.x, midTower.image_rect.y = center-midTower.image_rect.width//2,HEIGHT-midTower.image_rect.height
        righterTower.image_rect.x, righterTower.image_rect.y = right-righterTower.image_rect.width//2,HEIGHT-righterTower.image_rect.height
        

        self.widget = {
            "timer": TextBox(self.screen, WIDTH//2- 200//2,0, 200,50),
            "moves": TextBox(self.screen, WIDTH//2- 200//2,50, 200,50),
            "pause": Button(self.screen, 0,0,50,50,text="||", onRelease=self.pause)
        }

        towers = Stack()
        towers.insert(lefterTower)
        towers.insert(midTower)
        towers.insert(righterTower)

        for i in towers:
            i.hitbox_rect.x, i.hitbox_rect.y = i.image_rect.x - (i.hitbox_rect.width//2 - i.image_rect.width//2), i.image_rect.y
        # end useless variable
        self.hanoi = Hanoi(self.game, towers, rings, shuffled=shuffle)

    def run(self, events):
        self.widget['timer'].setText("Time: "+str(int(self.hanoi.time)))
        self.widget['moves'].setText("Moves:" +str(self.hanoi.moves))
        self.hanoi.update(events)
    
    def pause(self):
        self.hanoi.pause = True
        self.widget['pause'].disable()
        self.widget['array'] = ButtonArray(self.screen, WIDTH//2-200//2,300,200,400,(1,2), texts=["resume","quit"], onReleases=[self.resume, self.quit])

    def quit(self):
        self.game.gamescene.set_scene(MainMenu(self.game))
    
    def resume(self):
        self.hanoi.pause = False
        self.widget['pause'].enable()
        pygame_widgets.WidgetHandler().removeWidget(self.widget['array'])
    def destroy(self):
        for i,v in self.widget.items():
            pygame_widgets.WidgetHandler().removeWidget(v)


class Game:

    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.gamescene = SceneManager(MainMenu(self))
        self.delta = 0
        
        self.run = False

        self.bgm = pygame.mixer.Sound('music/bgm.mp3')

        if not os.path.exists('settings.json'):
            with open('settings.json', 'w+') as file:
                file.write('{"bgm": 100, "sfx": 100}')
        
        with open('settings.json', 'r+') as file:
            data = json.load(file)

        self.bgm.set_volume(data['bgm']/100)
        self.bgm.play(-1)
    
    def quit(self):
        self.run = False

    def mainloop(self):
        self.run = True
        while self.run:
            self.screen.fill((255,255,255))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

            self.gamescene.update(events)
            self.delta = pygame.time.Clock().tick(30) / 1000
            pygame_widgets.update(events)
            pygame.display.update()


game = Game()
game.mainloop()