import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Avoidance Game")

# Player character
player_width = 50
player_height = 50
player_x = window_width // 2 - player_width // 2
player_y = window_height - player_height - 10
player_speed = 5

# Enemy
enemy_width = 50
enemy_height = 50
enemy_x = random.randint(0, window_width - enemy_width)
enemy_y = 0
enemy_speed = 3

# Game state
GAME_RUNNING = 0
GAME_OVER = 1
game_state = GAME_RUNNING

# Fire animation variables
fire_radius = 100
fire_color = (255, 128, 0)
fire_animation_timer = 0
fire_animation_speed = 0.2  # Time between frame changes in seconds
fire_animation_radius = fire_radius

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)  # Limit the frame rate to 60 FPS

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == GAME_RUNNING:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < window_width - player_width:
            player_x += player_speed

        # Enemy movement
        enemy_y += enemy_speed
        if enemy_y > window_height:
            enemy_x = random.randint(0, window_width - enemy_width)
            enemy_y = 0

        # Collision detection
        if player_x < enemy_x + enemy_width and player_x + player_width > enemy_x \
                and player_y < enemy_y + enemy_height and player_y + player_height > enemy_y:
            game_state = GAME_OVER

    elif game_state == GAME_OVER:
        # Animate the burning fire
        fire_animation_timer += clock.get_time() / 1000  # Convert clock time to seconds
        if fire_animation_timer >= fire_animation_speed:
            fire_animation_radius += 10
            if fire_animation_radius > 2 * fire_radius:
                fire_animation_radius = fire_radius
            fire_animation_timer = 0

        # Handle game over logic

        # Check for "Start Again" option
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = GAME_RUNNING
            player_x = window_width // 2 - player_width // 2
            player_y = window_height - player_height - 10

    # Clear the screen
    window.fill((0, 0, 0))  # Fill with black color

    # Draw game objects
    pygame.draw.rect(window, (255, 0, 0), (player_x, player_y, player_width, player_height))  # Player character
    pygame.draw.rect(window, (0, 255, 0), (enemy_x, enemy_y, enemy_width, enemy_height))  # Enemy

    if game_state == GAME_OVER:
        # Draw the burning fire animation
        pygame.draw.circle(window, fire_color, (window_width // 2, window_height // 2), fire_animation_radius)

        # Display "Start Again" option
        font = pygame.font.Font(None, 36)
        start_again_text = font.render("Press SPACE to Start Again", True, (255, 255, 255))
        window.blit(start_again_text, (window_width // 2 - start_again_text.get_width() // 2,
                                        window_height // 2 + fire_radius // 2))

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
