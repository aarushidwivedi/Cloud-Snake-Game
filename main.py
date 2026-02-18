import pygame
import random
from assets.aws_services import aws_services
from assets.azure_services import azure_services
from assets.gcp_services import gcp_services
CELL_SIZE = 20
all_services = aws_services + azure_services + gcp_services

# Pastel color palette
PASTEL_PINK = (255, 209, 220)
PASTEL_BLUE = (189, 224, 254)
PASTEL_GREEN = (186, 242, 198)
PASTEL_PURPLE = (221, 190, 237)
PASTEL_YELLOW = (255, 251, 194)
PASTEL_PEACH = (255, 218, 193)
BACKGROUND = (250, 245, 255) 
DARK_TEXT = (100, 80, 120) 

snake = [(10, 10), (9, 10), (8, 10)]
#for speed calculation purpose
starting_length = len(snake)

#start and set up screen
pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Cloud Snake Game")



running = True
game_over = False
service = None
clock = pygame.time.Clock()
direction = "RIGHT"

#random food generator
food_x = random.randint(0, 39)  
food_y = random.randint(0, 29) 
food = (food_x, food_y)

# font setting
font = pygame.font.Font(None, 48) 
small_font = pygame.font.Font(None, 32)
tiny_font = pygame.font.Font(None, 24)  

while running:
    screen.fill(BACKGROUND)
    if not game_over:
        # Draw food
        pygame.draw.rect(screen, PASTEL_PEACH, (food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), border_radius=8)

        # Get current head
        head_x, head_y = snake[0]

        # Calculate new head based on direction
        if direction == "UP":
            new_head = (head_x, head_y - 1)
        elif direction == "DOWN":
            new_head = (head_x, head_y + 1)  
        elif direction == "RIGHT":
            new_head = (head_x + 1, head_y)
        elif direction == "LEFT":
            new_head = (head_x - 1, head_y)
        
        # collision detection
        new_head_x, new_head_y = new_head
        if new_head_x < 0 or new_head_x >= 40:
            if not game_over: 
                game_over = True
                service = random.choice(all_services)
        elif new_head_y < 0 or new_head_y >= 30:
            if not game_over:
                game_over = True
                service = random.choice(all_services)

        # Add new head    
        snake.insert(0, new_head)
        if new_head in snake[1:]:
            if not game_over:
                game_over = True
                service = random.choice(all_services)
            
        # Check if food was eaten
        if new_head == food:
            food_x = random.randint(0, 39)
            food_y = random.randint(0, 29)
            food = (food_x, food_y)
        else:
            snake.pop() 

        # Handle keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if direction != "DOWN":
                        direction = "UP"
                if event.key == pygame.K_DOWN:
                    if direction != "UP":
                        direction = "DOWN"
                if event.key == pygame.K_LEFT:
                    if direction != "RIGHT":
                        direction = "LEFT"
                if event.key == pygame.K_RIGHT:
                    if direction != "LEFT":
                        direction = "RIGHT"
        
        # Draw snake
        for x,y in snake:
            pixel_x = x * CELL_SIZE
            pixel_y = y * CELL_SIZE
            pygame.draw.rect(screen, PASTEL_GREEN, (pixel_x+2, pixel_y+2, CELL_SIZE-4, CELL_SIZE-4), border_radius=5)
            

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over = False
                    # RESET THE GAME
                    snake = [(10, 10), (9, 10), (8, 10)]
                    direction = "RIGHT"
                    food_x = random.randint(0, 39)
                    food_y = random.randint(0, 29)
                    food = (food_x, food_y)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        # GAME OVER CARD 
        pygame.draw.rect(screen, (200, 200, 220), (255, 105, 310, 80), border_radius=15)
        pygame.draw.rect(screen, (255, 255, 255), (250, 100, 300, 75), border_radius=15)
        pygame.draw.rect(screen, PASTEL_PURPLE, (250, 100, 300, 75), width=3, border_radius=15)
        
        # Center "Game Over!"
        text = font.render("Game Over!", True, DARK_TEXT)
        text_rect = text.get_rect(center=(400, 137))  # 400 is half of 800 (screen width)
        screen.blit(text, text_rect)
        
        # SERVICE INFO CARD 
        pygame.draw.rect(screen, (200, 200, 220), (155, 205, 510, 260), border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), (150, 200, 500, 250), border_radius=20)
        pygame.draw.rect(screen, PASTEL_PURPLE, (150, 200, 500, 250), width=3, border_radius=20)
        
        # Center provider
        provider_text = small_font.render(service["provider"], True, PASTEL_BLUE)
        provider_rect = provider_text.get_rect(center=(400, 240))
        screen.blit(provider_text, provider_rect)
        
        # Center service name
        service_text = font.render(service["name"], True, DARK_TEXT)
        service_rect = service_text.get_rect(center=(400, 290))
        screen.blit(service_text, service_rect)
        
        # Center description
        desc_text = small_font.render(service["description"], True, (100, 100, 100))
        desc_rect = desc_text.get_rect(center=(400, 340))
        screen.blit(desc_text, desc_rect)
        
        # Center instructions
        instruction_text = tiny_font.render("Press SPACE to restart or ESC to quit", True, (180, 180, 180))
        instruction_rect = instruction_text.get_rect(center=(400, 410))
        screen.blit(instruction_text, instruction_rect)

    snake_length = len(snake)
    growth = snake_length - starting_length
    speed = 10 + (growth//3)
    pygame.display.flip()
    clock.tick(speed)

pygame.quit()