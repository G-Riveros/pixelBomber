import pygame
from sys import exit
from random import randint
# player 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_walkRight_1 = pygame.image.load('pixelBomber/graphics/walk_1.png').convert_alpha()
        player_walkRight_2 = pygame.image.load('pixelBomber/graphics/walk_2.png').convert_alpha()
        player_walkRight_3 = pygame.image.load('pixelBomber/graphics/walk_3.png').convert_alpha()
        player_walkLeft_1 = pygame.image.load('pixelBomber/graphics/walk_1_Left.png').convert_alpha()
        player_walkLeft_2 = pygame.image.load('pixelBomber/graphics/walk_2_Left.png').convert_alpha()
        player_walkLeft_3 = pygame.image.load('pixelBomber/graphics/walk_3_Left.png').convert_alpha()
        self.player_walk = [player_walkRight_1, player_walkRight_2, player_walkRight_3]
        self.player_walk_left = [player_walkLeft_1,player_walkLeft_2, player_walkLeft_3]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,355))
        self.velocity = 3

    # player controls /animation
    def player_input(self):
        keys = pygame.key.get_pressed()

        # Left movment
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.velocity
            # animation when moving
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk_left[int(self.player_index)]

        # Right movment        
        if keys[pygame.K_RIGHT] and self.rect.x < 746:
            self.rect.x += self.velocity
            # animation when moving
            self.player_index += 0.1
            if self.player_index > len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()

# obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        missile = pygame.image.load('pixelBomber/graphics/missile.png').convert_alpha()
        missile = pygame.transform.rotozoom(missile,90,1)
        self.missile = missile
        
        self.image = self.missile
        self.rect = self.image.get_rect(midbottom = (randint(11,790), 10))

    def update(self):
        self.rect.y += 6
        self.destroy()

    # deleting off screen rectangles
    def destroy(self):
        if self.rect.y >= 500:
            self.kill()

# score 
def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score = font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score.get_rect(center = (400,50))
    screen.blit(score,score_rect)
    return current_time

# collison
def collison_sprite():
    if pygame.sprite.spritecollide(player1.sprite, obstacle_goup, False):
        obstacle_goup.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
game_active = False
font = pygame.font.Font('pixelBomber/font/Pixeltype.ttf', 50)
start_time = 0
score = 0

# calling classes
player1 = pygame.sprite.GroupSingle()
player1.add(Player())

obstacle_goup = pygame.sprite.Group()

# importing background
sky = pygame.image.load('pixelBomber/graphics/background.jpg').convert()
sky_rect = sky.get_rect(midbottom = (403, 400))

# title/gameover text
title = font.render('pixel runner 2',False, (111,196,169))
title_rect = title.get_rect(center = (400,80))

game_message = font.render('Press space to run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,360))

game_overText = font.render('Game Over', False, (111,196,169))
game_overText_rect = game_overText.get_rect(center = (400,80))

obstacle__rect_list = []

# intro screen image 
stand =  pygame.image.load('pixelBomber/graphics/walk_1.png').convert_alpha()
stand = pygame.transform.rotozoom(stand,0,2)
stand_rect = stand.get_rect(center = (400,200))


# game over screen importing image (tomb)
game_over =  pygame.image.load('pixelBomber/graphics/game_over.png').convert_alpha()
game_over = pygame.transform.rotozoom(game_over,0,2)
game_over_rect = game_over.get_rect(center = (400,200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 800)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # restart
        if game_active == False:
             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                 game_active = True
                 start_time = pygame.time.get_ticks()

        # calling class
        if event.type == obstacle_timer and game_active:
            obstacle_goup.add(Obstacle())
            
# game active
    if game_active:
            
    # backgroung display
        screen.blit(sky,sky_rect)
        score = display_score()
     
    # player/obstacle display
        player1.draw(screen)
        player1.update()

        obstacle_goup.draw(screen)
        obstacle_goup.update()
         
    # calling collition function
        game_active = collison_sprite()

    # intro/ game over screen
    else:
        screen.fill((94,129,162))
        obstacle__rect_list.clear()

        score_message = font.render(f'Your score: {score}',False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400, 315))
        screen.blit(game_message,game_message_rect)

        # into (title of game and player)
        if score == 0:
            screen.blit(title,title_rect)
            screen.blit(stand, stand_rect)
        # game over (game over text, score and game over image (tomb))
        else:
            screen.blit(game_overText,game_overText_rect)
            screen.blit(score_message,score_message_rect)
            screen.blit(game_over, game_over_rect)

    pygame.display.update()
    clock.tick(60)
    

