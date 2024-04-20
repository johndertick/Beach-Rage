import pygame
import random
import button
from pygame import mixer
import math

pygame.init()

def main():
    clock = pygame.time.Clock()
    fps = 60

    #game window
    bottom_panel = 150
    screen_width = 800
    screen_height = 390 + bottom_panel

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Beach Rage')

    #game variables
    current_fighter = 1
    total_fighters = 3
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    potion = False
    potion_effect = 15
    clicked = False
    game_over = 0
    lose_sound_played = False

    #font
    custom_font = pygame.font.Font("fonts/Minecraft.ttf", 25)

    #colors
    red = (255, 0, 0)
    green = (0, 255, 0)
    yellow = (248, 255,0)
    light_blue = (173,216, 230)

    # Bg music
    mixer.music.load("audio/bg_music.mp3")

    # Adjust the loudness to 50% (0.5)
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

    lose_sfx = pygame.mixer.Sound("audio/lose_sfx.mp3")

    heal_sfx = pygame.mixer.Sound("audio/heal_sfx.mp3")
    heal_sfx.set_volume(0.4)

    victory_sfx = pygame.mixer.Sound("audio/victory_sfx.mp3")
    victory_sfx.set_volume(0.3)

    #load images
    #background image
    background_img = pygame.image.load('assets/bg.png').convert_alpha()
    bg_width = background_img.get_width()

    #panel image
    panel_img = pygame.image.load('assets/panel.png').convert_alpha()

    #potion image
    potion_img = pygame.image.load('assets/potion_bottle.png').convert_alpha()

    #load restart img
    restart_img = pygame.image.load('assets/restart_btn.png').convert_alpha()

    #load victory and defeat img
    victory_img = pygame.image.load('assets/victory.png').convert_alpha()

    defeat_img = pygame.image.load('assets/defeat.png').convert_alpha()

    #sword image
    sword_img = pygame.image.load('assets/sword.png').convert_alpha()

    sand_img = pygame.image.load('assets/sand.png').convert_alpha()

    #draw text
    def draw_text(text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))

    def draw_bg(scroll):
        for i in range(tiles):
            x = i * bg_width + scroll
            # Ensure that the background is drawn only within the visible screen area
            if x < screen_width:  # Draw only if the background is within the screen width
                screen.blit(background_img, (x, 0))

    #function for drawing panel
    def draw_panel():
        #draw panel rectangle
        screen.blit(panel_img, (0, screen_height - bottom_panel))
        #show character stats
        draw_text(f"{ninja.name} HP: {ninja.hp}", custom_font, light_blue, 100, screen_height - bottom_panel + 15)
        for count, i in enumerate(enemy_list):
            draw_text(f'{i.name} HP: {i.hp}', custom_font, light_blue, 520, (screen_height - bottom_panel + 15) + count * 60)

    def draw_sand():
        # Draw sand at a fixed position
        screen.blit(sand_img, (0, screen_height - bottom_panel - 120))

    #fighter class    
    class Fighter():

        def __init__(self, x, y, name, max_hp, strength, potion):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.start_potion = potion
            self.potion = potion
            self.alive = True
            self.animation_list = []
            self.frame_index = 0
            self.action = 0 #0 for idle, 1 for attack, 2 for hurt, 3 for death
            self.hurt_sfx = pygame.mixer.Sound("audio/hurt_sfx.mp3")
            self.hurt_sfx.set_volume(0.4)
            self.update_time = pygame.time.get_ticks()
            
            #load idle images
            temp_list = []
            for i in range(6):
                img = pygame.image.load(f"assets/{self.name}/Idle/{i}.png")
                img = pygame.transform.scale(img, (img.get_width() * 1.8, img.get_height() * 1.8))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
            #load attack images
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f"assets/{self.name}/Attack/{i}.png")
                img = pygame.transform.scale(img, (img.get_width() * 1.8, img.get_height() * 1.8))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
            #load hurt images
            temp_list = []
            for i in range(2):
                img = pygame.image.load(f"assets/{self.name}/Hurt/{i}.png")
                img = pygame.transform.scale(img, (img.get_width() * 1.8, img.get_height() * 1.8))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
            #load death images
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f"assets/{self.name}/Death/{i}.png")
                img = pygame.transform.scale(img, (img.get_width() * 1.8, img.get_height() * 1.8))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

        def update(self):
            animation_cooldown = 100
            #handle animation
            #update image
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if animation has run out reset back to the start
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.idle()

        def idle(self):
                #set animation to idle
                self.action = 0
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def attack(self, target):
                #deal damage
                rand = random.randint(-4, 5)    
                damage = self.strength + rand
                target.hp -= damage
                #run hurt animation
                target.hurt()

                #check if target is dead
                if target.hp < 1:
                    target.hp = 0
                    target.alive = False
                    target.death()
                damage_text = Damage_text(target.rect.centerx, target.rect.y, str(damage), red)
                damage_text_group.add(damage_text)

                #set variables to attack
                self.action = 1
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def hurt(self):
            #set animation to hurt
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
            # Play hurt sound
            self.hurt_sfx.play()

        def death(self):
                #set animation to death
                self.action = 3
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def reset(self):
            self.alive = True
            self.potion = self.start_potion
            self.hp = self.max_hp
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()
            mixer.music.play()

        def draw(self):
            screen.blit(self.image, self.rect)

    class HealthBar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp

        def draw(self, hp):
            #update with new health
            self.hp = hp
            #calculate health ratio
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

    class Damage_text(pygame.sprite.Sprite):
        def __init__(self, x, y, damage, color):
            pygame.font.init()  
            pygame.sprite.Sprite.__init__(self)
            self.font = pygame.font.Font("fonts/Minecraft.ttf", 30) 
            self.image = self.font.render(damage, True, color)  # Render text using custom font
            self.rect = self.image.get_rect()
            self.rect.center = (x, y + 70)
            self.counter = 0

        def update(self):
            # Move damage text up
            self.rect.y -= 1
            # Delete text after a few seconds
            self.counter += 1
            if self.counter > 50:
                self.kill()

    damage_text_group = pygame.sprite.Group()

    ninja = Fighter(180, 250, "Ninja", 30, 10, 3)
    enemy1 = Fighter(620, 250, "Enemy", 20, 5, 1)
    enemy2 = Fighter(520, 250, "Enemy", 20, 5, 1)

    enemy_list = []
    enemy_list.append(enemy1)
    enemy_list.append(enemy2)

    ninja_health_bar = HealthBar(100, screen_height - bottom_panel + 47, ninja.hp, ninja.max_hp)
    enemy1_health_bar = HealthBar(520, screen_height - bottom_panel + 47, enemy1.hp, enemy1.max_hp)
    enemy2_health_bar = HealthBar(520, screen_height - bottom_panel + 110, enemy2.hp, enemy2.max_hp)

    potion_button = button.Button(screen, 100, screen_height - bottom_panel + 75, potion_img, 64, 64)
    restart_button = button.Button(screen, 340, 120, restart_img, 140, 40)

    scroll = 0
    tiles = math.ceil(screen_width / bg_width) + 1

    run = True
    while run:

        clock.tick(fps)

        #draw background
        draw_bg(scroll)

        draw_sand()

        #draw panel
        draw_panel()

        # Update scrolling background
        if game_over == 0:  # Only update scrolling if the game is not over
            scroll -= 0.3
            if abs(scroll) > bg_width:
                scroll = 0

        #draw healthbar
        ninja_health_bar.draw(ninja.hp)
        enemy1_health_bar.draw(enemy1.hp)
        enemy2_health_bar.draw(enemy2.hp)

        #draw character
        ninja.update()
        ninja.draw()

        for enemy in enemy_list:
            enemy.update()
            enemy.draw()

        #draw dmg text
        damage_text_group.update()
        damage_text_group.draw(screen)

        #control player action
        #reset control variables
        attack = False
        potion = False
        target = None
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, enemy in enumerate(enemy_list):
            if enemy.rect.collidepoint(pos):
                #hide mouse
                pygame.mouse.set_visible(False)
                #show sword
                screen.blit(sword_img, pos)
                if clicked == True and enemy.alive == True:
                    attack = True
                    target = enemy_list[count]
        if potion_button.draw():
            potion = True
            #show number of potions remaining
        draw_text(str(ninja.potion), custom_font, yellow, 150, screen_height - bottom_panel + 120)

        if game_over == 0:    
            #player action   
            if ninja.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                        if attack == True and target != None:
                            ninja.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                            #potion
                        if potion == True:
                            if ninja.potion > 0:
                                #check if potion heals ninja beyond max hp
                                if ninja.max_hp - ninja.hp > potion_effect:
                                    heal_amount = potion_effect
                                else:
                                    heal_amount = ninja.max_hp - ninja.hp
                                ninja.hp += heal_amount
                                ninja.potion -= 1
                                heal_sfx.play()
                                damage_text = Damage_text(ninja.rect.centerx, ninja.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0

            else:
                    game_over = -1
                                    
                                    
                                
                            
                            
                            
            #enemy action                
            for count, enemy in enumerate(enemy_list):
                            if current_fighter == 2 + count:
                                if enemy.alive == True:
                                    action_cooldown += 1
                                    if action_cooldown >= action_wait_time:
                                        #check if enemy needs to heal first
                                        if (enemy.hp / enemy.max_hp) < 0.5 and enemy.potion > 0:
                                            #check if potion heals enemy beyond max hp
                                            if enemy.max_hp - enemy.hp > potion_effect:
                                                heal_amount = potion_effect                            
                                            else:
                                                heal_amount = enemy.max_hp - enemy.hp
                                            enemy.hp += heal_amount
                                            heal_sfx.play()
                                            enemy.potion -= 1
                                            damage_text = Damage_text(enemy.rect.centerx, enemy.rect.y, str(heal_amount), green)
                                            damage_text_group.add(damage_text)
                                            current_fighter += 1
                                            action_cooldown = 0
                                            
                                        #attack
                                        else:
                                            enemy.attack(ninja)
                                            current_fighter += 1
                                            action_cooldown = 0        
                                else:
                                    current_fighter += 1            
                            
            #if all fighters had a turn then reset
            if current_fighter > total_fighters:
                            current_fighter = 1
                        
        #check if enemies are dead
        alive_enemies = 0
        for enemy in enemy_list:
            if enemy.alive == True:
                alive_enemies += 1
        if alive_enemies == 0:
            game_over = 1
                
        # Handle game over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (290, 50))
                victory_sfx.play()
            elif game_over == -1:
                screen.blit(defeat_img, (290, 50))  
                if not lose_sound_played:
                    mixer.music.stop()
                    lose_sfx.play()
                    lose_sound_played = True
            if restart_button.draw():
                ninja.reset()
                for enemy in enemy_list:
                    enemy.reset()
                current_fighter = 1
                action_cooldown
                game_over = 0
                lose_sfx.stop()
                lose_sound_played = False
                        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False

        pygame.display.update()

    pygame.quit()