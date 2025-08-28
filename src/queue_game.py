import pygame
import sys
import random
from collections import deque
import os

pygame.init()
WIDTH, HEIGHT = 500, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Queue Game")
FPS = 60

WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

CUSTOMER_WIDTH, CUSTOMER_HEIGHT = 40, 40
MAX_QUEUE = 10

class CustomerQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, color):
        if len(self.queue) < MAX_QUEUE:
            self.queue.append(color)
            return True
        return False

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

def draw_window(queue, score):
    WIN.fill(WHITE)
    for i, color in enumerate(queue.queue):
        x = 50 + i * (CUSTOMER_WIDTH + 10)
        y = HEIGHT // 2
        pygame.draw.rect(WIN, color, (x, y, CUSTOMER_WIDTH, CUSTOMER_HEIGHT))
    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Score: {score}", True, BLACK)
    WIN.blit(text, (20, 20))
    text2 = font.render("RIGHT: Add | LEFT: Serve", True, RED)
    WIN.blit(text2, (20, 50))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    queue = CustomerQueue()
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if queue.enqueue(random.choice([GREEN, BLACK])):
                        score += 1
                elif event.key == pygame.K_LEFT:
                    if queue.dequeue() is not None:
                        score += 1
        draw_window(queue, score)

    # Save high score
    SCORES_DIR = "scores"
    os.makedirs(SCORES_DIR, exist_ok=True)
    score_file = os.path.join(SCORES_DIR, "queue.txt")
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
