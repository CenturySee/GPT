import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the fonts
FONT = pygame.font.SysFont(None, 48)

# Set up the ball
BALL_RADIUS = 10
ball_x = WINDOW_WIDTH // 2
ball_y = WINDOW_HEIGHT // 2
ball_dx = 5
ball_dy = 5

# Set up the player's paddle
PLAYER_PADDLE_WIDTH = 10
PLAYER_PADDLE_HEIGHT = 100
player_paddle_x = WINDOW_WIDTH - PLAYER_PADDLE_WIDTH - 10
player_paddle_y = WINDOW_HEIGHT // 2 - PLAYER_PADDLE_HEIGHT // 2
player_paddle_dy = 0

# Set up the computer's paddle
COMPUTER_PADDLE_WIDTH = 10
COMPUTER_PADDLE_HEIGHT = 100
computer_paddle_x = 10
computer_paddle_y = WINDOW_HEIGHT // 2 - COMPUTER_PADDLE_HEIGHT // 2
computer_paddle_dy = 5

# Set up the scores
player_score = 0
computer_score = 0
player_str = ""
computer_str = ""

# Set up the game state
game_state = "start"
space_state = "0"

# Set up the clock
clock = pygame.time.Clock()

# Set up the main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_paddle_dy = -5
            elif event.key == pygame.K_DOWN:
                player_paddle_dy = 5
            elif event.key == pygame.K_SPACE:
                if space_state == "0":
                    space_state = "1"
                    #print(f"DOWN, space_state: {space_state}, {game_state}, {computer_score}", flush=True)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_paddle_dy = 0
            elif event.key == pygame.K_SPACE:
                if space_state != "1": continue
                #print(f"  UP, space_state: {space_state}, {game_state}, {computer_score}", flush=True)
                space_state = "0"
                if game_state == "start":
                    game_state = "playing"
                    ball_dx = -ball_dx
                    ball_dy = -ball_dy
                    #ball_dx = random.choice([-5, 5])
                    #ball_dy = random.choice([-5, 5])
        #elif event.type == pygame.MOUSEBUTTONDOWN:
        #elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #    if game_state == "start":
        #        game_state = "playing"
        #        ball_dx = random.choice([-5, 5])
        #        ball_dy = random.choice([-5, 5])

    # Update the game state
    if game_state == "playing":
        # Move the ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Bounce the ball off the top or bottom of the window
        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= WINDOW_HEIGHT:
            ball_dy = -ball_dy

        # Bounce the ball off the player's paddle
        if ball_x + BALL_RADIUS >= player_paddle_x and ball_y >= player_paddle_y and ball_y <= player_paddle_y + PLAYER_PADDLE_HEIGHT:
            ball_dx = -ball_dx

        # Bounce the ball off the computer's paddle
        if ball_x - BALL_RADIUS <= computer_paddle_x + COMPUTER_PADDLE_WIDTH and ball_y >= computer_paddle_y and ball_y <= computer_paddle_y + COMPUTER_PADDLE_HEIGHT:
            ball_dx = -ball_dx

        # Check if the ball went out of bounds
        if ball_x - BALL_RADIUS <= 0:
            #computer_score += 1
            player_score += 1
            game_state = "start"
        elif ball_x + BALL_RADIUS >= WINDOW_WIDTH:
            #player_score += 1
            computer_score += 1
            game_state = "start"
        # 判断游戏是否结束
        if computer_score >= 5 or player_score >= 5:
            game_state = "game over"

        # Move the player's paddle
        player_paddle_y += player_paddle_dy
        if player_paddle_y <= 0:
            player_paddle_y = 0
        elif player_paddle_y + PLAYER_PADDLE_HEIGHT >= WINDOW_HEIGHT:
            player_paddle_y = WINDOW_HEIGHT - PLAYER_PADDLE_HEIGHT

        # Move the computer's paddle
        if ball_y < computer_paddle_y + COMPUTER_PADDLE_HEIGHT // 2:
            computer_paddle_dy = -5
        elif ball_y > computer_paddle_y + COMPUTER_PADDLE_HEIGHT // 2:
            computer_paddle_dy = 5
        else:
            computer_paddle_dy = 0
        computer_paddle_y += computer_paddle_dy
        if computer_paddle_y <= 0:
            computer_paddle_y = 0
        elif computer_paddle_y + COMPUTER_PADDLE_HEIGHT >= WINDOW_HEIGHT:
            computer_paddle_y = WINDOW_HEIGHT - COMPUTER_PADDLE_HEIGHT

    # Draw the game
    WINDOW.fill(BLACK)
    if game_state == "start":
        #start_text = FONT.render("Press the mouse button to start", True, WHITE)
        start_text = FONT.render("Press space key to start", True, WHITE)
        start_rect = start_text.get_rect()
        start_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        WINDOW.blit(start_text, start_rect)
    elif game_state == "playing":
        # Draw the ball
        pygame.draw.circle(WINDOW, WHITE, (ball_x, ball_y), BALL_RADIUS)

        # Draw the player's paddle
        pygame.draw.rect(WINDOW, WHITE, (player_paddle_x, player_paddle_y, PLAYER_PADDLE_WIDTH, PLAYER_PADDLE_HEIGHT))

        # Draw the computer's paddle
        pygame.draw.rect(WINDOW, WHITE, (computer_paddle_x, computer_paddle_y, COMPUTER_PADDLE_WIDTH, COMPUTER_PADDLE_HEIGHT))

        # Draw the scores
        player_score_text = FONT.render(str(player_score), True, WHITE)
        player_score_rect = player_score_text.get_rect()
        player_score_rect.center = (WINDOW_WIDTH - 50, 50)
        WINDOW.blit(player_score_text, player_score_rect)

        computer_score_text = FONT.render(str(computer_score), True, WHITE)
        computer_score_rect = computer_score_text.get_rect()
        computer_score_rect.center = (50, 50)
        WINDOW.blit(computer_score_text, computer_score_rect)

    elif game_state == "game over":
        # Draw the game over text
        game_over_text = FONT.render("Game Over", True, WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50)
        WINDOW.blit(game_over_text, game_over_rect)

        # Draw the final scores
        #print(player_score, computer_score, flush=True)
        if not player_str:
            player_str = f"Player Score: {player_score}" 
            computer_str = f"Computer Score: {computer_score}"
        
        player_final_score_text = FONT.render(player_str, True, WHITE)
        player_final_score_rect = player_final_score_text.get_rect()
        player_final_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        WINDOW.blit(player_final_score_text, player_final_score_rect)

        computer_final_score_text = FONT.render(computer_str, True, WHITE)
        computer_final_score_rect = computer_final_score_text.get_rect()
        computer_final_score_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)
        WINDOW.blit(computer_final_score_text, computer_final_score_rect)

        # Reset the scores and game state
        player_score = 0
        computer_score = 0
        game_state = "game over"

    # Update the window
    pygame.display.update()

    # Tick the clock
    clock.tick(60)

pygame.quit()