import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)
        
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        # Prevent moving in opposite direction
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self):
        head = self.body[0]
        # Check wall collision
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
        # Check self collision
        if head in self.body[1:]:
            return True
        return False
    
    def eat_food(self, food_pos):
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_position(snake_body)
    
    def generate_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

def draw_grid(screen):
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

def draw_snake(screen, snake):
    for i, segment in enumerate(snake.body):
        x, y = segment
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2))

def draw_food(screen, food):
    x, y = food.position
    pygame.draw.rect(screen, RED, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2))

def draw_score(screen, score, font):
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen(screen, score, font):
    screen.fill(BLACK)
    game_over_text = font.render('GAME OVER!', True, RED)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    restart_text = font.render('Press SPACE to restart or ESC to quit', True, WHITE)
    
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 60))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 60))
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    while True:
        # Initialize game
        snake = Snake()
        food = Food(snake.body)
        score = 0
        game_active = True
        
        while game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
            
            # Move snake
            snake.move()
            
            # Check collisions
            if snake.check_collision():
                game_active = False
                continue
            
            # Check if food eaten
            if snake.eat_food(food.position):
                score += 1
                food = Food(snake.body)
            
            # Draw everything
            screen.fill(BLACK)
            draw_grid(screen)
            draw_snake(screen, snake)
            draw_food(screen, food)
            draw_score(screen, score, font)
            
            pygame.display.flip()
            clock.tick(10)  # Game speed
        
        # Game over screen
        game_over_screen(screen, score, font)
        
        # Wait for restart or quit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

if __name__ == '__main__':
    main()