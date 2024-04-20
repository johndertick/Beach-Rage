import pygame
import sys
import os
import math
from MAIN import main
from button import Button  # Import the Button class from button.py

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 540

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Load animation images
animation_folder = "assets/Animated_BG"
animation_images = [pygame.image.load(os.path.join(animation_folder, f)) for f in os.listdir(animation_folder) if f.endswith('.png')]
num_frames = len(animation_images)
current_frame = 0
background_frame_delay = 80 # Adjust frame delay for background animation

# Audio
menu_music = pygame.mixer.Sound("audio/waves_sfx.mp3")

# Load start image
start_img = pygame.image.load("assets/start_btn.png")
quit_img = pygame.image.load("assets/quit_btn.png")

# Font
font = pygame.font.Font("fonts/pixel_font.TTF", 50)

# Define floating text variables
text_floating_frequency = 900#Adjust text speed
background_animation_frequency = 500# Adjust the frequency of the background animation

def main_menu():
    global current_frame

    # Play menu music
    menu_music.play(-1)  # -1 plays the music on loop

    while True:
        # Draw background animation
        current_frame %= num_frames
        background = animation_images[current_frame]
        SCREEN.blit(background, ((SCREEN_WIDTH - background.get_width()) // 2, (SCREEN_HEIGHT - background.get_height()) // 2))
        current_frame += 1

        # Render text with custom color and apply floating effect
        text_floating_factor = pygame.time.get_ticks() / text_floating_frequency
        text_surface = font.render('Beach Rage!', True, (211, 211, 211))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 160 + 10 * math.sin(text_floating_factor)))

        # Display text on screen
        SCREEN.blit(text_surface, text_rect)

        # Create start button and apply floating effect
        button_floating_factor = pygame.time.get_ticks() / text_floating_frequency
        start_button = Button(SCREEN, (SCREEN_WIDTH - 200) // 2.5, (SCREEN_HEIGHT - 100) // 2 + 10 * math.sin(button_floating_factor), start_img, 300, 100)
        quit_button = Button(SCREEN, (SCREEN_WIDTH - 200) // 2.5, (SCREEN_HEIGHT - 100) // 2 + 120 + 10 * math.sin(button_floating_factor), quit_img, 300, 100)
        # Draw buttons
        start_button.draw()
        quit_button.draw()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if start button is clicked
                if start_button.rect.collidepoint(pygame.mouse.get_pos()):
                    # Stop menu music when start button is clicked
                    menu_music.stop()
                    main()
                elif quit_button.rect.collidepoint(pygame.mouse.get_pos()):
                    # Exit the game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        pygame.time.delay(background_frame_delay)  # Control frame rate for background animation


main_menu()