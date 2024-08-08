import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.toggle import Toggle
from pygame_widgets.textbox import TextBox

from hanoi import Hanoi, Tower, scale
from stack import Stack

from tree import BinaryTree

import json
import os

from abc import ABC, abstractmethod

pygame.init()
WIDTH, HEIGHT = 570, 700
inactive = (255, 220, 220)
hover = (255, 190, 190)
click = (255, 160, 160)
border_inactive = (255, 200, 200)
border_hover = (255, 180, 180)
border_click = (255, 160, 160)

font_color_button = (235, 140, 140)
font_color = (255, 120, 120) # COLOR not on button

header_color = (255,90,90)

# dont touch
font_bold = "font/arcade_bold.ttf"
font_san = "font/arcade.ttf"

pygame.display.set_caption("Tower of Cats")

class Scene(ABC):
    @abstractmethod
    def run(self, events): # executes
        pass
    
    @abstractmethod
    def destroy(self): # destroy any widget
        pass

class SceneManager:
    def __init__(self, scene):
        self.__scene = scene
    
    def get_scene(self):
        return self.__scene
    
    def set_scene(self, scene):
        if self.__scene:
            self.__scene.destroy()
        self.__scene = scene
    
    def update(self, events):
        self.__scene.run(events)

class MainMenu(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(font_bold, 48)
        self.title = self.font.render("Tower of Cats", True, font_color)
        # colors

        self.buttons = [
            Button(self.game.screen, WIDTH / 2 - 300 / 2, 200 + 20, 300, 100,borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click,radius=50, text='Play', font=pygame.font.Font(font_bold, 64), onRelease=lambda:self.switch('play')),
            Button(self.screen, WIDTH / 2 - 300 / 2, 300 + 30, 300, 100,borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text="Leaderboard", font=pygame.font.Font(font_bold, 32), onRelease=lambda:self.switch('leaderboard')),
            Button(self.screen, WIDTH / 2 - 300 / 2, 400 + 40, 300, 100,borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text="Settings", font=pygame.font.Font(font_bold, 50), onRelease=lambda:self.switch('settings')),
            Button(self.screen, WIDTH / 2 - 300 / 2, 500 + 50, 300, 100,borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, onRelease=lambda:self.switch('quit'), font=pygame.font.Font(font_bold, 64), text="Quit")
        ]
        
        self.mouse = pygame.mouse

        self.bg_image = pygame.image.load("images/game/backgrounds/menu_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    def switch(self, scene):
        self.game.sfx['button'].play()
        if scene == 'play':
            self.game.gamescene.set_scene(GameSelection(game))
        elif scene == 'leaderboard':
            self.game.gamescene.set_scene(Leaderboard(game))
        elif scene == 'settings':
            self.game.gamescene.set_scene(Settings(game))
        elif scene == 'quit':
            self.game.quit()

    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        self.screen.blit(self.title, (WIDTH / 2 - self.title.get_width() / 2, 100))

    def destroy(self):
        for i in self.buttons:
            pygame_widgets.WidgetHandler().removeWidget(i)

class Settings(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        center = WIDTH / 2
        self.widgets = {
            "bgm": Slider(self.screen, WIDTH // 2 - 400 // 2 - 20, 340, 380, 33, min=0, max=100, initial=100, handleRadius=15),
            "sfx": Slider(self.screen, WIDTH // 2 - 400 // 2 - 20, 460, 380, 33, min=0, max=100, initial=100, handleRadius=15),
            "back": Button(self.screen, center - 200 / 2, HEIGHT - 150, 200, 100,font=pygame.font.Font(font_bold, 52),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, text="Back", fontSize=64, onClick=self.back, radius=100 // 2)
        }
        
        fontLabel = pygame.font.Font(font_bold, 32)
        title = pygame.font.Font(font_bold, 56)

        self.bgm_label = fontLabel.render("Background Music", True, font_color)
        self.sfx_label = fontLabel.render("Sound Effects", True, font_color)
        self.settings_title = title.render("Settings", True, font_color)

        self.font = pygame.font.Font(font_bold, 20)

        self.open()
        
        self.bg_image = pygame.image.load("images/game/backgrounds/menu_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))
    
    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        
        self.screen.blit(self.bgm_label, (WIDTH / 2 - self.bgm_label.get_width() / 2, 280))
        self.screen.blit(self.sfx_label, (WIDTH / 2 - self.sfx_label.get_width() / 2, 400))
        self.screen.blit(self.settings_title, (WIDTH / 2 - self.settings_title.get_width() / 2, 100))

        # Draw slider values
        bgm_value_text = self.font.render(f"{self.widgets['bgm'].getValue()}", True, font_color)
        sfx_value_text = self.font.render(f"{self.widgets['sfx'].getValue()}", True, font_color)

        self.screen.blit(bgm_value_text, (WIDTH // 2 - 400 // 2 + 395, 345))
        self.screen.blit(sfx_value_text, (WIDTH // 2 - 400 // 2 + 395, 465))
        
        # Update the widgets
        for widget in self.widgets.values():
            widget.draw()
    
    def open(self):
        if not os.path.exists('settings.json'):
            with open('settings.json', 'w+') as file:
                file.write('{"bgm": 100, "sfx": 100}')
        with open('settings.json', 'r+') as file:
            data = json.load(file)
        self.widgets['bgm'].setValue(data['bgm'])
        self.widgets['sfx'].setValue(data['sfx'])
    
    def back(self):
        data = {"bgm": self.widgets['bgm'].getValue(), "sfx": self.widgets['sfx'].getValue()}
        with open('settings.json', 'w+') as file:
            json.dump(data, file)
        
        self.game.bgm.set_volume(data['bgm'] / 100)  # Change volume
        for sound in self.game.sfx.values():
            sound.set_volume(data['sfx']/100)
        self.game.gamescene.set_scene(MainMenu(self.game))  # Change scene
    
    def destroy(self):
        for key, stat in self.widgets.items():
            pygame_widgets.WidgetHandler().removeWidget(stat)

class GameSelection(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        # Initialize fonts
        self.fontLabel = pygame.font.Font(font_bold, 32)
        self.font = pygame.font.Font(font_bold, 15)
        title = pygame.font.Font(font_bold, 52)

        # Initialize texts
        self.slider_text = self.fontLabel.render("Number of Cats:", True, font_color)
        self.toggle_text = self.fontLabel.render("Shuffle Mode", True, font_color)
        self.gameselection_title = title.render("Game Setup", True, font_color)

        # Initialize widgets
        center = WIDTH / 2
        self.widgets = {
            "slider": Slider(self.screen, WIDTH // 2 - 260 // 2, 280, 260, 15,colour=inactive,handleColour=click, min=3, max=9, handleRadius=30, initial=3, step=0.01),
            "toggle": Toggle(self.screen, WIDTH // 2 - 75 // 2, 410, 75, 50, handleRadius=25, handleOnColour=border_click,handleOffColour=border_inactive,onColour=inactive,offColour=click),
            "back": Button(self.screen, center / 2 - 260 / 2, 550, 260, 110,font=pygame.font.Font(font_bold, 52),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text="Back", fontSize=64, onRelease=lambda: self.switch('back')),
            "play": Button(self.screen, (center + center / 2) - 260 / 2, 550, 260, 110,font=pygame.font.Font(font_bold, 52),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text="Play", fontSize=64, onRelease=lambda: self.switch('play'))
        }

        # Create an initial text for slider value
        self.update_slider_value()

        self.bg_image = pygame.image.load("images/game/backgrounds/menu_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    def update_slider_value(self):
        value = round(self.widgets['slider'].getValue())
        self.slider_value_text = self.fontLabel.render(str(value), True, font_color) 

    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        
        self.screen.blit(self.gameselection_title, (WIDTH / 2 - self.gameselection_title.get_width() / 2, 60))
        self.screen.blit(self.slider_text, (WIDTH / 2 - self.slider_text.get_width() / 2 - 25, 200))
        self.screen.blit(self.toggle_text, (WIDTH / 2 - self.toggle_text.get_width() / 2, 360))

        # Update and draw slider value text
        self.update_slider_value()
        self.screen.blit(self.slider_value_text, (WIDTH / 2 + 260 // 2 - self.slider_value_text.get_width() + 52, 200))
        
    
    def switch(self, scene):
        self.game.sfx['button'].play()
        if scene == 'play':
            self.game.gamescene.set_scene(TowerCats(self.game, rings=round(self.widgets['slider'].getValue()), shuffle=self.widgets['toggle'].getValue()))
        elif scene == 'back':
            self.game.gamescene.set_scene(MainMenu(game))
    
    def destroy(self):
        for i, v in self.widgets.items():
            pygame_widgets.WidgetHandler().removeWidget(v)

class Leaderboard(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(font_bold, 20)
        self.title_font = pygame.font.Font(font_bold, 36)  # Larger font for the title
        self.title = self.title_font.render("Leaderboard", True, font_color)

        self.leaderboard_entries = self.load_leaderboard()
        self.content_height = 50 * (len(self.leaderboard_entries) + 1)  # Include space for the header
        self.surface = pygame.Surface((WIDTH, self.content_height + 20), pygame.SRCALPHA)
        self.surface.fill((255, 255, 255, 20))  # Fill with semi-transparent white

        self.y_scroll = 0
        self.create_leaderboard()

        self.widgets = {
            'back': Button(self.screen, 0,0,125,45,borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, text="Back")
        }

        self.bg_image = pygame.image.load("images/game/backgrounds/leaderboard_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    '''def load_leaderboard(self):
        if os.path.exists('leaderboard.json'):
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
                # Sort the data by score in descending order and return the top 10
                data.sort(key=lambda x: x['score'], reverse=True)
                return data[:10]
        return []'''
    
    def load_leaderboard(self):
        tree = BinaryTree().load_json()
        return tree

    def create_leaderboard(self):
        # Define columns and their positions
        columns = ["Rank", "Name", "Score"]
        column_positions = [10, 150, 400]  # Adjust these positions as needed for proper spacing

        # Render header
        for col, pos in zip(columns, column_positions):
            header = self.font.render(col, True, header_color)
            self.surface.blit(header, (pos, 10))  # Adjust the y position of the header

        # Render leaderboard entries
        entry_y_spacing = 49  # Adjust this value to change spacing between entries
        for i, entry in enumerate(self.leaderboard_entries.get_first_values(10)):
            rank_text = self.font.render(f"{i + 1}", True, font_color)
            name_text = self.font.render(entry['name'], True, font_color)
            score_text = self.font.render(str(entry['score']), True, font_color)

            texts = [rank_text, name_text, score_text]
            for text, pos in zip(texts, column_positions):
                self.surface.blit(text, (pos, 60 + i * entry_y_spacing))  # Adjust the y position for entries

    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        self.screen.blit(self.title, (WIDTH / 2 - self.title.get_width() / 2, 80))

        self.screen.blit(self.surface, (0, 160))
    

    def destroy(self):
        pass

class TowerCats(Scene):
    def __init__(self, game, rings, shuffle=False):
        self.game = game
        self.screen = game.screen
        self.paused = False

        
        lefterTower = Tower(self.game.screen, Stack())
        midTower = Tower(self.game.screen, Stack())
        righterTower = Tower(self.game.screen, Stack())
        modidier = 50
        center = WIDTH // 2
        left = center / 2 - modidier
        right = center + center / 2 + modidier
        lefterTower.image_rect.center = (left - lefterTower.image_rect.width // 2, HEIGHT - lefterTower.image_rect.height)
        midTower.image_rect.center = (center - lefterTower.image_rect.width // 2, HEIGHT - lefterTower.image_rect.height)
        righterTower.image_rect.center = (right - righterTower.image_rect.width // 2, HEIGHT - righterTower.image_rect.height)

        lefterTower.image_rect.x, lefterTower.image_rect.y = left - lefterTower.image_rect.width // 2, HEIGHT - lefterTower.image_rect.height
        midTower.image_rect.x, midTower.image_rect.y = center - midTower.image_rect.width // 2, HEIGHT - midTower.image_rect.height
        righterTower.image_rect.x, righterTower.image_rect.y = right - righterTower.image_rect.width // 2, HEIGHT - righterTower.image_rect.height

        self.widget = {
            "pause": Button(self.screen, 0, 0, 50, 50,font=pygame.font.Font(font_bold, 46),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, image=scale(pygame.image.load('images/game/pause.png'), (50,50)), onRelease=self.pause)
        }

        towers = Stack()
        towers.insert(lefterTower)
        towers.insert(midTower)
        towers.insert(righterTower)

        for i in towers:
            i.hitbox_rect.x, i.hitbox_rect.y = i.image_rect.x - (i.hitbox_rect.width // 2 - i.image_rect.width // 2), i.image_rect.y

        self.hanoi = Hanoi(self.game, towers, rings, shuffled=shuffle)

        self.timer_rect = pygame.Rect(WIDTH // 2 - 200 // 2, 25, 200, 60)
        self.moves_rect = pygame.Rect(WIDTH // 2 - 200 // 2, 75, 200, 70)
        self.text_color = (0,0,0)  

        self.bg_image = pygame.image.load("images/game/backgrounds/game_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        
        font = pygame.font.Font(None, 54)
        timer_text = font.render(f"Time: {int(self.hanoi.time)}", True, self.text_color)
        moves_text = font.render(f"Moves: {self.hanoi.moves}", True, self.text_color)
        
        self.screen.blit(timer_text, (self.timer_rect.x + 10, self.timer_rect.y + 10))
        self.screen.blit(moves_text, (self.moves_rect.x + 10, self.moves_rect.y + 10))
        
        # Check for ESC key press to pause
        for event in events:
            self.handle_event(event)
        
        if not self.paused:
            self.hanoi.update(events)
            self.check_winner()  

    def check_winner(self):
        righterTower = self.hanoi.towers.get_by_index(2) 
        if len(righterTower.stack) == self.hanoi.rings:
            score = self.calculate_score()
            self.game.gamescene.set_scene(Winner(self.game, score))

    def calculate_score(self):
        moves = self.hanoi.moves
        timer = self.hanoi.time
        rings = self.hanoi.rings
        base = 1000
        super_base = rings * base
        score = super_base - (((timer*moves) + (moves/2))**0.5)

        '''print("Moves: ", moves)
        print("Timer: ", timer)
        print("Min Move: ", min_move)
        print("Rings: ", rings)
        print("Base: ", base)
        print("Score: ", score)'''

        return max(0, int(score)) 

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause()
    
    def pause(self):
        self.game.sfx['button'].play()
        if not self.paused:
            self.hanoi.pause = True
            self.paused = True
            self.buttons = [
                Button(self.screen, WIDTH / 2 - 300 / 2, 200 + 20, 300, 100,font=pygame.font.Font(font_bold, 42),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text="Resume", fontSize=64, onRelease=self.resume),
                Button(self.screen, WIDTH / 2 - 300 / 2, 300 + 30, 300, 100,font=pygame.font.Font(font_bold, 52),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text="Quit", fontSize=64, onRelease=self.quit)
            ]
    
    def resume(self):
        self.game.sfx['button'].play()
        self.hanoi.pause = False
        self.paused = False
        for i in self.buttons:
            pygame_widgets.WidgetHandler().removeWidget(i)

    def quit(self):
        self.game.sfx['button'].play()
        for i in self.buttons:
            pygame_widgets.WidgetHandler().removeWidget(i)
        self.game.gamescene.set_scene(MainMenu(self.game))


    def destroy(self):
        for i, v in self.widget.items():
            pygame_widgets.WidgetHandler().removeWidget(v)

class Winner(Scene):
    def __init__(self, game, score):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 96)
        self.title = self.font.render("WINNER", True, (0, 0, 0))
        self.score = score

        self.name_box = TextBox(self.screen, WIDTH / 2 - 150, 300, 300, 60, fontSize=40, borderThickness=3, radius=10, borderColour=border_inactive, font=pygame.font.Font('font/arcade.TTF', 32), onSubmit=self.save_name)
        
        # Initialize buttons
        self.buttons = [
            Button(self.game.screen, WIDTH / 2 - 150, 400, 300, 100,font=pygame.font.Font(font_bold, 46),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text='Save', fontSize=64, onRelease=lambda: self.click('save')),
            Button(self.game.screen, WIDTH / 2 - 150, 520, 300, 100,font=pygame.font.Font(font_bold, 36),borderThickness=5, inactiveColour=inactive, hoverColour=hover,pressedColour=click, inactiveBorderColour=border_inactive,hoverBorderColour=border_hover,pressedBorderColour=border_click, radius=50, text='Main Menu', fontSize=64, onRelease=lambda: self.click('main'))
        ]

        self.bg_image = pygame.image.load("images/game/backgrounds/winner_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    def click(self, command):
        self.game.sfx['button'].play()
        if command == 'save':
            self.save_name()
        elif command == 'main':
            self.game.gamescene.set_scene(MainMenu(self.game))

    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        self.screen.blit(self.title, (WIDTH / 2 - self.title.get_width() / 2, 75))

        # Display the score
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, 200))
        
        # Update and draw TextBox
        self.name_box.draw()
        
        # Draw buttons
        for button in self.buttons:
            button.draw()

    def save_name(self):
        name = self.name_box.getText()
        if name:
            # Load existing names
            if os.path.exists('leaderboard.json'):
                with open('leaderboard.json', 'r') as file:
                    data = json.load(file)
            else:
                data = []

            found = False
            for i in data:
                if name == i['name']:
                    found = True
                    if self.score > i['score']:
                        i['score'] = self.score
                    break
            # Append the new name with score if not found
            if not found:
                data.append({"name": name, "score": self.score})

                # Save the updated list back to the file
            with open('leaderboard.json', 'w') as file:
                json.dump(data, file, indent=4)

            self.name_box.setText('')
        
        self.game.gamescene.set_scene(MainMenu(self.game))

    def destroy(self):
        pygame_widgets.WidgetHandler().removeWidget(self.name_box)
        for button in self.buttons:
            pygame_widgets.WidgetHandler().removeWidget(button)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.delta = 0
        self.run = False

        self.bgm = pygame.mixer.Sound('sounds/music/bgm.mp3')
        self.sfx = {}
        sfx_path = 'sounds/sfx'
        for file in os.listdir(sfx_path):
            name = file.removesuffix('.mp3')
            print(file)
            self.sfx[name] = pygame.mixer.Sound('sounds/sfx/'+file)


        if not os.path.exists('settings.json'):
            with open('settings.json', 'w+') as file:
                file.write('{"bgm": 100, "sfx": 100}')

        with open('settings.json', 'r+') as file:
            volume = json.load(file)
        self.volume = volume
        for i in self.sfx.values():
            i.set_volume(self.volume['sfx']/100)
        self.bgm.set_volume(self.volume['bgm'] / 100)
        self.bgm.play(-1)
        self.gamescene = SceneManager(MainMenu(self))
    def quit(self):
        self.run = False

    def mainloop(self):
        self.run = True
        while self.run:
            self.screen.fill((255, 255, 255))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.run = False

            self.gamescene.update(events)
            self.delta = pygame.time.Clock().tick(30) / 1000
            pygame_widgets.update(events)
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.mainloop()
