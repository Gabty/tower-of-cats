No need for this, as discussed that we will no longer use buttons



Just a bit of insight or like a template for changing the button widget into a button image (although you already know how)


    class MainMenu(Scene):
        def __init__(self, game):
            self.game = game
            self.screen = game.screen
            self.font = pygame.font.Font(None, 78)
            self.title = self.font.render("Tower of Cats", True, (0, 0, 0))
    
            # Load button images
            self.play_button_image = pygame.image.load("images/game/buttons/play_button.png")
            self.play_button_rect = self.play_button_image.get_rect()
            self.play_button_rect.topleft = (WIDTH / 2 - self.play_button_rect.width / 2, 200 + 20)
    
            self.leaderboard_button_image = pygame.image.load("images/game/buttons/play_button.png")
            self.leaderboard_button_rect = self.leaderboard_button_image.get_rect()
            self.leaderboard_button_rect.topleft = (WIDTH / 2 - self.leaderboard_button_rect.width / 2, 300 + 30)
    
            self.options_button_image = pygame.image.load("images/game/buttons/play_button.png")
            self.options_button_rect = self.options_button_image.get_rect()
            self.options_button_rect.topleft = (WIDTH / 2 - self.options_button_rect.width / 2, 400 + 40)
    
            self.quit_button_image = pygame.image.load("images/game/buttons/play_button.png")
            self.quit_button_rect = self.quit_button_image.get_rect()
            self.quit_button_rect.topleft = (WIDTH / 2 - self.quit_button_rect.width / 2, 500 + 50)
    
            self.mouse = pygame.mouse
    
            self.bg_image = pygame.image.load("images/game/backgrounds/menu_bg.png")
            self.bg_rect = self.bg_image.get_rect(topleft=(0, 0))
    
        def run(self, events):
            self.screen.blit(self.bg_image, self.bg_rect.topleft)
            self.screen.blit(self.title, (WIDTH / 2 - self.title.get_width() / 2, 100))
    
            # Draw the buttons
            self.screen.blit(self.play_button_image, self.play_button_rect.topleft)
            self.screen.blit(self.leaderboard_button_image, self.leaderboard_button_rect.topleft)
            self.screen.blit(self.options_button_image, self.options_button_rect.topleft)
            self.screen.blit(self.quit_button_image, self.quit_button_rect.topleft)
    
            # Check for mouse click on buttons
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button_rect.collidepoint(event.pos):
                        self.game.gamescene.set_scene(GameSelection(self.game))
                    elif self.leaderboard_button_rect.collidepoint(event.pos):
                        self.game.gamescene.set_scene(Leaderboard(self.game))
                    elif self.options_button_rect.collidepoint(event.pos):
                        self.game.gamescene.set_scene(Settings(self.game))
                    elif self.quit_button_rect.collidepoint(event.pos):
                        self.game.quit()
    
        def destroy(self):
            pass  # No need to remove widgets since we're not using pygame_widgets for these buttons
