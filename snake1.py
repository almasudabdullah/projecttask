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
YELLOW = (255, 255, 0)
DARK_GRAY = (20, 20, 20)
GRID_COLOR = (30, 30, 30)
SNAKE_HEAD = (50, 200, 50)
SNAKE_BODY = (34, 139, 34)
SNAKE_OUTLINE = (25, 100, 25)
FOOD_RED = (220, 20, 60)
FOOD_HIGHLIGHT = (255, 69, 96)

# Difficulty speeds
SPEEDS = {
    'slow': 7,
    'medium': 12,
    'fast': 18
}

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
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, WINDOW_HEIGHT), 1)
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WINDOW_WIDTH, y), 1)

def draw_snake(screen, snake):
    for i, segment in enumerate(snake.body):
        x, y = segment
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if i == 0:  # Head
            # Draw head with rounded corners and eyes
            pygame.draw.rect(screen, SNAKE_HEAD, rect, border_radius=8)
            pygame.draw.rect(screen, SNAKE_OUTLINE, rect, 2, border_radius=8)
            
            # Draw eyes based on direction
            eye_size = 4
            if snake.direction == RIGHT:
                eye1_pos = (x * GRID_SIZE + 14, y * GRID_SIZE + 6)
                eye2_pos = (x * GRID_SIZE + 14, y * GRID_SIZE + 14)
            elif snake.direction == LEFT:
                eye1_pos = (x * GRID_SIZE + 6, y * GRID_SIZE + 6)
                eye2_pos = (x * GRID_SIZE + 6, y * GRID_SIZE + 14)
            elif snake.direction == UP:
                eye1_pos = (x * GRID_SIZE + 6, y * GRID_SIZE + 6)
                eye2_pos = (x * GRID_SIZE + 14, y * GRID_SIZE + 6)
            else:  # DOWN
                eye1_pos = (x * GRID_SIZE + 6, y * GRID_SIZE + 14)
                eye2_pos = (x * GRID_SIZE + 14, y * GRID_SIZE + 14)
            
            pygame.draw.circle(screen, BLACK, eye1_pos, eye_size)
            pygame.draw.circle(screen, BLACK, eye2_pos, eye_size)
        else:  # Body
            # Draw body segments with gradient effect
            pygame.draw.rect(screen, SNAKE_BODY, rect, border_radius=6)
            pygame.draw.rect(screen, SNAKE_OUTLINE, rect, 2, border_radius=6)
            # Add highlight
            highlight_rect = pygame.Rect(x * GRID_SIZE + 2, y * GRID_SIZE + 2, GRID_SIZE - 4, GRID_SIZE // 2)
            pygame.draw.rect(screen, (60, 179, 60), highlight_rect, border_radius=4)

def draw_food(screen, food):
    x, y = food.position
    center_x = x * GRID_SIZE + GRID_SIZE // 2
    center_y = y * GRID_SIZE + GRID_SIZE // 2
    
    # Draw apple-like food
    # Main body
    pygame.draw.circle(screen, FOOD_RED, (center_x, center_y), GRID_SIZE // 2 - 2)
    
    # Highlight
    pygame.draw.circle(screen, FOOD_HIGHLIGHT, (center_x - 3, center_y - 3), 3)
    
    # Stem
    stem_points = [
        (center_x, center_y - GRID_SIZE // 2 + 2),
        (center_x + 2, center_y - GRID_SIZE // 2 - 2),
        (center_x + 3, center_y - GRID_SIZE // 2 - 1)
    ]
    pygame.draw.lines(screen, (101, 67, 33), False, stem_points, 2)
    
    # Leaf
    leaf_rect = pygame.Rect(center_x + 2, center_y - GRID_SIZE // 2 - 3, 4, 3)
    pygame.draw.ellipse(screen, (34, 139, 34), leaf_rect)

def draw_score(screen, score, font):
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

def difficulty_menu(screen, font):
    screen.fill(BLACK)
    title_text = font.render('SELECT DIFFICULTY', True, WHITE)
    slow_text = font.render('1 - SLOW', True, GREEN)
    medium_text = font.render('2 - MEDIUM', True, YELLOW)
    fast_text = font.render('3 - FAST', True, RED)
    
    screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 2 - 100))
    screen.blit(slow_text, (WINDOW_WIDTH // 2 - slow_text.get_width() // 2, WINDOW_HEIGHT // 2 - 30))
    screen.blit(medium_text, (WINDOW_WIDTH // 2 - medium_text.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
    screen.blit(fast_text, (WINDOW_WIDTH // 2 - fast_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'slow'
                elif event.key == pygame.K_2:
                    return 'medium'
                elif event.key == pygame.K_3:
                    return 'fast'
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_over_screen(screen, score, difficulty, font):
    screen.fill(BLACK)
    game_over_text = font.render('GAME OVER!', True, RED)
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    diff_text = font.render(f'Difficulty: {difficulty.upper()}', True, YELLOW)
    restart_text = font.render('Press SPACE to restart or ESC to quit', True, WHITE)
    
    screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 90))
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 30))
    screen.blit(diff_text, (WINDOW_WIDTH // 2 - diff_text.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 2 + 70))
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    while True:
        # Select difficulty
        difficulty = difficulty_menu(screen, font)
        speed = SPEEDS[difficulty]
        
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
            screen.fill(DARK_GRAY)
            draw_grid(screen)
            draw_snake(screen, snake)
            draw_food(screen, food)
            draw_score(screen, score, font)
            
            pygame.display.flip()
            clock.tick(speed)  # Use selected speed
        
        # Game over screen
        game_over_screen(screen, score, difficulty, font)
        
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