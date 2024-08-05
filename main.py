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
WIDTH, HEIGHT = 570, 700

pygame.display.set_caption("Tower of Cats")

class Scene(ABC):
    @abstractmethod
    def run(self, events):
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
        self.title = self.font.render("Tower of Cats", True, (0,0,0))
        
        self.buttons = [
            Button(self.game.screen, WIDTH / 2 - 300 / 2, 200 + 20, 300, 100, radius=50, text='Play', fontSize=64, onRelease=lambda: game.gamescene.set_scene(GameSelection(game))),
            Button(self.screen, WIDTH / 2 - 300 / 2, 300 + 30, 300, 100, radius=50, text="Leaderboard", fontSize=56, onRelease=lambda: game.gamescene.set_scene(Leaderboard(game))),
            Button(self.screen, WIDTH / 2 - 300 / 2, 400 + 40, 300, 100, radius=50, text="Options", fontSize=64, onRelease=lambda: game.gamescene.set_scene(Settings(game))),
            Button(self.screen, WIDTH / 2 - 300 / 2, 500 + 50, 300, 100, radius=50, onRelease=lambda: game.quit(), text="Quit", fontSize=64)
        ]
        
        self.mouse = pygame.mouse

        self.bg_image = pygame.image.load("images/game/backgrounds/menu_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

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
            "back": Button(self.screen, center - 200 / 2, HEIGHT - 125, 200, 100, text="Back", fontSize=64, onClick=self.back, radius=100 // 2)
        }
        
        fontLabel = pygame.font.Font(None, 64)
        title = pygame.font.Font(None, 96)

        self.bgm_label = fontLabel.render("Background Music", True, (0,0,0))
        self.sfx_label = fontLabel.render("Sound Effects", True, (0,0,0))
        self.settings_title = title.render("Settings", True, (0, 0, 0))

        self.font = pygame.font.Font(None, 40)

        self.open()
        
        self.bg_image = pygame.image.load("images/game/backgrounds/menu_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))
    
    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        
        self.screen.blit(self.bgm_label, (WIDTH / 2 - self.bgm_label.get_width() / 2, 280))
        self.screen.blit(self.sfx_label, (WIDTH / 2 - self.sfx_label.get_width() / 2, 400))
        self.screen.blit(self.settings_title, (WIDTH / 2 - self.settings_title.get_width() / 2, 100))

        # Draw slider values
        bgm_value_text = self.font.render(f"{self.widgets['bgm'].getValue()}", True, (0, 0, 0))
        sfx_value_text = self.font.render(f"{self.widgets['sfx'].getValue()}", True, (0, 0, 0))

        self.screen.blit(bgm_value_text, (WIDTH // 2 - 400 // 2 + 385, 345))
        self.screen.blit(sfx_value_text, (WIDTH // 2 - 400 // 2 + 385, 465))
        
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
        self.game.gamescene.set_scene(MainMenu(self.game))  # Change scene
    
    def destroy(self):
        for key, stat in self.widgets.items():
            pygame_widgets.WidgetHandler().removeWidget(stat)

class GameSelection(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        # Initialize fonts
        self.fontLabel = pygame.font.Font(None, 64)
        self.font = pygame.font.Font(None, 30)
        title = pygame.font.Font(None, 75)

        # Initialize texts
        self.slider_text = self.fontLabel.render("Number of Cats:", True, (0, 0, 0))
        self.toggle_text = self.fontLabel.render("Shuffle Mode", True, (0, 0, 0))
        self.gameselection_title = title.render("Game Setup", True, (0, 0, 0))

        # Initialize widgets
        center = WIDTH / 2
        self.widgets = {
            "slider": Slider(self.screen, WIDTH // 2 - 260 // 2, 250, 260, 63, min=3, max=9, handleRadius=30, initial=3, step=1),
            "toggle": Toggle(self.screen, WIDTH // 2 - 75 // 2, 410, 75, 50, handleRadius=25),
            "back": Button(self.screen, center / 2 - 260 / 2, 550, 260, 110, radius=50, text="Back", fontSize=64, onRelease=lambda: game.gamescene.set_scene(MainMenu(game))),
            "play": Button(self.screen, (center + center / 2) - 260 / 2, 550, 260, 110, radius=50, text="Play", fontSize=64, onRelease=self.switch_to_game)
        }

        # Create an initial text for slider value
        self.update_slider_value()

        self.bg_image = pygame.image.load("images/game/backgrounds/menu_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    def update_slider_value(self):
        value = int(self.widgets['slider'].getValue())
        self.slider_value_text = self.fontLabel.render(str(value), True, (0, 0, 0)) 

    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        
        self.screen.blit(self.gameselection_title, (WIDTH / 2 - self.gameselection_title.get_width() / 2, 60))
        self.screen.blit(self.slider_text, (WIDTH / 2 - self.slider_text.get_width() / 2 - 25, 200))
        self.screen.blit(self.toggle_text, (WIDTH / 2 - self.toggle_text.get_width() / 2, 360))

        # Update and draw slider value text
        self.update_slider_value()
        self.screen.blit(self.slider_value_text, (WIDTH / 2 + 260 // 2 - self.slider_value_text.get_width() + 52, 200))
        
        # Update the widgets
        for widget in self.widgets.values():
            widget.draw()
    
    def switch_to_game(self):
        self.game.gamescene.set_scene(TowerCats(self.game, rings=self.widgets['slider'].getValue(), shuffle=self.widgets['toggle'].getValue()))

    def destroy(self):
        for i, v in self.widgets.items():
            pygame_widgets.WidgetHandler().removeWidget(v)


class Leaderboard(Scene):
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(None, 41)
        self.title_font = pygame.font.Font(None, 72)  # Larger font for the title
        self.title = self.title_font.render("Leaderboard", True, (0, 0, 0))

        self.leaderboard_entries = self.load_leaderboard()[:10]  # Load only the top 10
        self.content_height = 50 * (len(self.leaderboard_entries) + 1)  # Include space for the header
        self.surface = pygame.Surface((WIDTH, self.content_height + 20), pygame.SRCALPHA)
        self.surface.fill((255, 255, 255, 128))  # Fill with semi-transparent white

        self.y_scroll = 0
        self.create_leaderboard()

        self.back_button_font = pygame.font.Font(None, 48)
        self.back_button = self.back_button_font.render("Back", True, (0, 0, 0))
        self.back_button_rect = self.back_button.get_rect(topleft=(10, 10))

        self.bg_image = pygame.image.load("images/game/backgrounds/leaderboard_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

    def load_leaderboard(self):
        if os.path.exists('leaderboard.json'):
            with open('leaderboard.json', 'r') as file:
                data = json.load(file)
                # Sort the data by score in descending order and return the top 10
                data.sort(key=lambda x: x['score'], reverse=True)
                return data[:10]
        return []

    def create_leaderboard(self):
        # Define columns and their positions
        columns = ["Rank", "Name", "Score"]
        column_positions = [10, 150, 400]  # Adjust these positions as needed for proper spacing

        # Render header
        for col, pos in zip(columns, column_positions):
            header = self.font.render(col, True, (0, 0, 0))
            self.surface.blit(header, (pos, 10))  # Adjust the y position of the header

        # Render leaderboard entries
        entry_y_spacing = 49  # Adjust this value to change spacing between entries
        for i, entry in enumerate(self.leaderboard_entries):
            rank_text = self.font.render(f"{i + 1}", True, (0, 0, 0))
            name_text = self.font.render(entry['name'], True, (0, 0, 0))
            score_text = self.font.render(str(entry['score']), True, (0, 0, 0))

            texts = [rank_text, name_text, score_text]
            for text, pos in zip(texts, column_positions):
                self.surface.blit(text, (pos, 60 + i * entry_y_spacing))  # Adjust the y position for entries

    def run(self, events):
        self.screen.blit(self.bg_image, self.bg_rect.topleft)
        self.screen.blit(self.title, (WIDTH / 2 - self.title.get_width() / 2, 80))
        self.screen.blit(self.back_button, self.back_button_rect.topleft)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button_rect.collidepoint(event.pos):
                    self.game.gamescene.set_scene(MainMenu(self.game))
            if event.type == pygame.MOUSEWHEEL:
                self.y_scroll -= event.y * 20
                self.y_scroll = max(0, min(self.y_scroll, self.content_height - (HEIGHT - 100)))  # Adjust for title height

        self.screen.blit(self.surface, (0, 160 - self.y_scroll))  # Adjust starting y position for scrolling

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
            "pause": Button(self.screen, 0, 0, 50, 50, text="||", onRelease=self.pause)
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
        min_move = self.hanoi.min_moves
        base = 1000
        super_base = rings * base
        score = super_base - ((moves - min_move) / min_move) + ((timer - 1.5 * min_move)/1.5 * min_move) * base

        print("Moves: ", moves)
        print("Timer: ", timer)
        print("Min Move: ", min_move)
        print("Rings: ", rings)
        print("Base: ", base)
        print("Score: ", score)

        return max(0, int(score)) 

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause()
    
    def pause(self):
        if not self.paused:
            self.hanoi.pause = True
            self.paused = True
            self.buttons = [
                Button(self.screen, WIDTH / 2 - 300 / 2, 200 + 20, 300, 100, radius=50, text="Resume", fontSize=64, onRelease=self.resume),
                Button(self.screen, WIDTH / 2 - 300 / 2, 300 + 30, 300, 100, radius=50, text="Quit", fontSize=64, onRelease=self.quit)
            ]
    
    def resume(self):
        self.hanoi.pause = False
        self.paused = False
        del self.buttons

    def quit(self):
        self.game.gamescene.set_scene(MainMenu(self.game))
        del self.buttons

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

        self.name_box = TextBox(self.screen, WIDTH / 2 - 150, 300, 300, 60, fontSize=40, borderThickness=1, radius=10)
        
        # Initialize buttons
        self.buttons = [
            Button(self.game.screen, WIDTH / 2 - 150, 400, 300, 100, radius=50, text='Save', fontSize=64, onRelease=self.save_name),
            Button(self.game.screen, WIDTH / 2 - 150, 520, 300, 100, radius=50, text='Main Menu', fontSize=64, onRelease=lambda: game.gamescene.set_scene(MainMenu(game)))
        ]

        self.bg_image = pygame.image.load("images/game/backgrounds/winner_bg.png")
        self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))

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

            # Append the new name with score
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
        self.gamescene = SceneManager(MainMenu(self))
        self.delta = 0
        self.run = False

        self.bgm = pygame.mixer.Sound('music/bgm.mp3')

        if not os.path.exists('settings.json'):
            with open('settings.json', 'w+') as file:
                file.write('{"bgm": 100, "sfx": 100}')
        
        with open('settings.json', 'r+') as file:
            data = json.load(file)

        self.bgm.set_volume(data['bgm'] / 100)
        self.bgm.play(-1)
    
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

game = Game()
game.mainloop()
