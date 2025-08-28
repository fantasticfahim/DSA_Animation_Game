import pygame
import sys
import random
from collections import deque
import os

pygame.init()
WIDTH, HEIGHT = 500, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Deque Game")
FPS = 60

WHITE = (255, 255, 255)
PURPLE = (138, 43, 226)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

ITEM_WIDTH, ITEM_HEIGHT = 40, 40
MAX_SIZE = 10

class ItemDeque:
    def __init__(self):
        self.deque = deque()

    def add_front(self, color):
        if len(self.deque) < MAX_SIZE:
            self.deque.appendleft(color)
            return True
        return False

    def add_back(self, color):
        if len(self.deque) < MAX_SIZE:
            self.deque.append(color)
            return True
        return False

    def remove_front(self):
        if self.deque:
            self.deque.popleft()
            return True
        return False

    def remove_back(self):
        if self.deque:
            self.deque.pop()
            return True
        return False

def draw_window(deq, score):
    WIN.fill(WHITE)
    for i, color in enumerate(deq.deque):
        x = 50 + i * (ITEM_WIDTH + 10)
        y = HEIGHT // 2
        pygame.draw.rect(WIN, color, (x, y, ITEM_WIDTH, ITEM_HEIGHT))
    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Score: {score}", True, BLACK)
    WIN.blit(text, (20, 20))
    text2 = font.render("A:AddFront D:AddBack W:RemFront S:RemBack", True, RED)
    WIN.blit(text2, (10, 50))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    deq = ItemDeque()
    score = 0
    running = True

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                color = random.choice([PURPLE, ORANGE])
                if event.key == pygame.K_a:
                    if deq.add_front(color):
                        score += 1
                elif event.key == pygame.K_d:
                    if deq.add_back(color):
                        score += 1
                elif event.key == pygame.K_w:
                    if deq.remove_front():
                        score += 1
                elif event.key == pygame.K_s:
                    if deq.remove_back():
                        score += 1
        draw_window(deq, score)

    # Save high score
    SCORES_DIR = "scores"
    os.makedirs(SCORES_DIR, exist_ok=True)
    score_file = os.path.join(SCORES_DIR, "deque.txt")
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
