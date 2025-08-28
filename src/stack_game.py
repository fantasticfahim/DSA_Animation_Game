import pygame
import sys
import random
import os

# ----------------- Setup -----------------
pygame.init()
WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Stack Game - Plate Tower")
FPS = 60

WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
RED = (255, 69, 0)
BLACK = (0, 0, 0)

PLATE_WIDTH, PLATE_HEIGHT = 100, 20
MAX_HEIGHT = 10  # max plates

# ----------------- Stack Implementation -----------------
class PlateStack:
    def __init__(self):
        self.stack = []

    def push(self, plate_color):
        if len(self.stack) < MAX_HEIGHT:
            self.stack.append(plate_color)
            return True
        return False

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

# ----------------- Game Functions -----------------
def draw_window(stack, score):
    WIN.fill(WHITE)
    for i, color in enumerate(stack.stack):
        x = (WIDTH - PLATE_WIDTH) // 2
        y = HEIGHT - (i + 1) * PLATE_HEIGHT
        pygame.draw.rect(WIN, color, (x, y, PLATE_WIDTH, PLATE_HEIGHT))

    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Score: {score}", True, BLACK)
    WIN.blit(text, (20, 20))
    text2 = font.render("UP: Add | DOWN: Remove", True, RED)
    WIN.blit(text2, (20, 50))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    stack = PlateStack()
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if stack.push(random.choice([BLUE, RED])):
                        score += 1
                elif event.key == pygame.K_DOWN:
                    if stack.pop() is not None:
                        score += 1
        draw_window(stack, score)

    # ----------------- Save high score -----------------
    SCORES_DIR = "scores"
    os.makedirs(SCORES_DIR, exist_ok=True)
    score_file = os.path.join(SCORES_DIR, "stack.txt")
    try:
        with open(score_file, "r") as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0
    if score > high_score:
        with open(score_file, "w") as f:
            f.write(str(score))

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
