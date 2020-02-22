import pygame
import random

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue  = pygame.Color(0, 0, 255)

block_size = 10

class Snake:
    len_start = 1
    len_tot = 1
    head_pos = []
    body = []
    
    def __init__(self, x_min, x_max, y_min, y_max):
        self.set_random_coordinates(x_min, x_max, y_min, y_max)

    def set_random_coordinates(self, x_min, x_max, y_min, y_max):
        self.x = round(random.randint(x_min, x_max) / 10.0) * 10.0
        self.y = round(random.randint(y_min, y_max) / 10.0) * 10.0

    def draw(self, screen, coordinates):
        for i in coordinates:
            pygame.draw.rect(screen, white, [int(i[0]), int(i[1]), block_size, block_size])


class Apple:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.set_random_coordinates(x_min, x_max, y_min, y_max)

    def set_random_coordinates(self, x_min, x_max, y_min, y_max):
        self.x = round(random.randint(x_min, x_max) / 10.0) * 10.0 + block_size/2
        self.y = round(random.randint(y_min, y_max) / 10.0) * 10.0 + block_size/2

    def draw(self, screen):
        pygame.draw.circle(screen, green, (int(self.x),int(self.y)), int(block_size/2))

class App:
    _screen_width = 300
    _screen_height = 300

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Pygame Snake')
        self._running = True
        self._game_over = False
        self._screen_surface = pygame.display.set_mode((self._screen_width, self._screen_height))
        self.player = Snake(3*block_size, self._screen_width - 3*block_size, 3*block_size, self._screen_height - 3*block_size)
        self.apple = Apple(3*block_size, self._screen_width - 3*block_size, 3*block_size, self._screen_height - 3*block_size)
        self.score = 0
        self.player_x_change = 0
        self.player_y_change = 0

        self.execute_game()

    def execute_game(self):
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                        self._game_over = True
                    elif event.key == pygame.K_LEFT:
                        self.player_x_change = -block_size
                        self.player_y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        self.player_x_change = block_size
                        self.player_y_change = 0
                    elif event.key == pygame.K_UP:
                        self.player_y_change = -block_size
                        self.player_x_change = 0
                    elif event.key == pygame.K_DOWN:
                        self.player_y_change = block_size
                        self.player_x_change = 0

            self.update_player_head(self.player_x_change, self.player_y_change)

            self.player_teleport_if_wall_hit()

            self.update_player_body()

            if self.player_bites_itself():
                self._game_over = True
                self.game_over_and_quit()
                break

            self.update_player_movement()
            
            if self.player_eats_apple():
                self.player.len_tot += 1
                self.apple.set_random_coordinates(block_size, self._screen_width - block_size, block_size, self._screen_height - block_size)

            self.update_score()

            if self._game_over:
                self.game_over_and_quit()
                break

            self.drawing()

            pygame.time.delay(80)

    def drawing(self):
        self._screen_surface.fill(black)

        self.draw_score()
        self.apple.draw(self._screen_surface)
        self.player.draw(self._screen_surface, self.player.body)
        pygame.display.update()

    def player_teleport_if_wall_hit(self):
        if self.player.x >= self._screen_width:
            self.player.x = 0
        elif self.player.x < 0:
            self.player.x = self._screen_width - block_size
        elif self.player.y >= self._screen_height:
            self.player.y = 0
        elif self.player.y < 0:
            self.player.y = self._screen_height - block_size

    def player_bites_itself(self):
        if self.player.len_tot != self.player.len_start:
            for player_body in self.player.body[:-1]: 
                if player_body[0] == self.player.x and player_body[1] == self.player.y:
                    return True
        else:
            return False

    def player_eats_apple(self):
        if abs(self.player.x - self.apple.x + block_size/2) <= block_size/2 and \
            abs(self.player.y - self.apple.y + block_size/2) <= block_size/2:
            return True
        else:
            return False

    def update_player_head(self, x_change, y_change):
        self.player.x += x_change
        self.player.y += y_change

    def update_player_body(self):
        self.player.head_pos = []
        self.player.head_pos.append(self.player.x)
        self.player.head_pos.append(self.player.y)
        self.player.body.append(self.player.head_pos)

    def update_player_movement(self):
        if len(self.player.body) > self.player.len_tot:
            del self.player.body[0]

    def update_score(self):
        self.score = self.player.len_tot - 1

    def draw_score(self):
        font = pygame.font.Font('freesansbold.ttf', 16) 
        text = font.render('Score: {}'.format(self.score), True, white, black)
        textRect = text.get_rect()  
        textRect.center = (40, 16) 
        self._screen_surface.blit(text, textRect)

    def game_over_and_quit(self):
        self._screen_surface.fill(black)
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render('Game Over!', True, white, black)
        textRect = text.get_rect()  
        textRect.center = (self._screen_width/2, self._screen_height/3)
        self._screen_surface.blit(text, textRect)
        font = pygame.font.Font('freesansbold.ttf', 16) 
        text = font.render('Score: {}'.format(self.score), True, white, black)
        textRect = text.get_rect()  
        textRect.center = (self._screen_width/2, self._screen_height/2)
        self._screen_surface.blit(text, textRect)
        pygame.display.update()
        pygame.time.delay(4000)
        pygame.quit()


if __name__ == "__main__" :
    application = App()