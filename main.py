import random
# from django.shortcuts import render_doc
import pygame 
from sys import exit
from random import randint , choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.4)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):      
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]      

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha() 
            fly_2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            self.y_pos = 210
        else:
            snail_1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha() 
            snail_2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]    
            self.y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900,1100),self.y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state()    
        self.rect.x -= 6
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()    

pygame.init()

screen = pygame.display.set_mode((800 , 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
bg_music.set_volume(0.5)
test_font = pygame.font.Font('font/Pixeltype.ttf' , 50)

#groups
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()
player.add(Player())


Sky_surface = pygame.image.load('Graphics/Sky.png').convert()

groundImg = pygame.image.load('Graphics/ground.png').convert()

# text
game_title = test_font.render('Pixel Runner',False , (111,196,169))
game_rect = game_title.get_rect(center = (400,80))

restart_title = test_font.render('Press Space To Run' , False , (111,196,169))
restart_rect = restart_title.get_rect(center = (400 , 340))

#enemys
snail_frame_1 = pygame.image.load('Graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Graphics/snail/snail2.png').convert_alpha()
snail_frame = [snail_frame_1,snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frame[snail_frame_index]
snail_rect = snail_surface.get_rect(bottomright = (800 , 300))

fly_frame_1= pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Graphics/Fly/Fly2.png').convert_alpha()
fly_frame = [fly_frame_1,fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frame[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('Graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect= player_surf.get_rect(midbottom = (80 , 300))
snail_x_pos = 600

player_gravity = 0
game_active = True
start_time = 0
score = 0

player_stand = pygame.image.load('Graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)    
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]    
        return obstacle_list 
    else:
        return []       

def dispaly_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = test_font.render(f'Score :{current_time}' , False ,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision(player,obstacle):
    if obstacle:
        for obstacle_rect in obstacle:
            if player.colliderect(obstacle_rect):
                return False
    return True     

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True     

def player_animation():
    global player_surf , player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]    

#timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1400)   
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200) 
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:    
            
                   
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            if event.type == pygame.MOUSEBUTTONDOWN:
                player_gravity = -20        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
              
                start_time = int(pygame.time.get_ticks()/1000)
        if game_active:     
          
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail' , 'snail' ])))
                # if randint(0,2):

                #     obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100), 300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(bottomright= (randint(900,1100),210)))  
            if event.type == snail_animation_timer:    
                if snail_frame_index == 0:snail_frame_index = 1
                else:snail_frame_index = 0
                snail_surface = snail_frame[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:fly_frame_index = 1 
                else:fly_frame_index = 0
                fly_surf= fly_frame[fly_frame_index]         
                
 
    if game_active:        
        screen.blit(Sky_surface , (0,0))
        screen.blit(groundImg,(0,300))
        
        score =  dispaly_score()
    
        # snail_rect.x -=4
        # if snail_rect.right <= 0:snail_rect.left = 800
        # screen.blit(snail_surface ,snail_rect)

        #player
        # player_gravity += 1

        # player_rect.y += player_gravity
        # if player_rect.bottom >= 300:
        #     player_rect.bottom = 300
        # player_animation()    
        # screen.blit(player_surf,player_rect)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collision_sprite()
        #obstacle_movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        
        # game_active = collision(player_rect,obstacle_rect_list)   
    else:

        screen.fill((94 , 129 , 162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        score_message = test_font.render(f'Your score: {score}',False, (111,198,169))
        score_message_rect = score_message.get_rect(center = (400,310))
        screen.blit(game_title , game_rect)
        if score==0:

            screen.blit(restart_title,restart_rect)
        else:
            screen.blit(score_message,score_message_rect)    

    pygame.display.update()  
    clock.tick(60)