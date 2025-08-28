import pygame
import sys
import subprocess
import os

# ----------------- Setup -----------------
pygame.init()
WIDTH, HEIGHT = 400, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Animation Game - Main Menu")
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 149, 237)
RESET_COLOR = (220, 20, 60)
RESET_HOVER = (255, 69, 0)

# ----------------- Scores -----------------
SCORES_DIR = "scores"
os.makedirs(SCORES_DIR, exist_ok=True)

def read_score(key):
    file_path = os.path.join(SCORES_DIR, f"{key}.txt")
    try:
        with open(file_path, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

def reset_scores():
    for key in ["stack", "queue", "deque"]:
        file_path = os.path.join(SCORES_DIR, f"{key}.txt")
        with open(file_path, "w") as f:
            f.write("0")
    # Update local scores dictionary
    for key in scores:
        scores[key] = 0

scores = {
    "stack": read_score("stack"),
    "queue": read_score("queue"),
    "deque": read_score("deque")
}

# ----------------- Button Helper -----------------
class Button:
    def __init__(self, text, x, y, w, h, command, key=None, reset=False):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.command = command
        self.hovered = False
        self.key = key
        self.reset = reset

    def draw(self, surface):
        if self.reset:
            color = RESET_HOVER if self.hovered else RESET_COLOR
        else:
            color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect)
        font = pygame.font.SysFont(None, 28)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

        # Show high score if hovered
        if self.key and not self.reset and self.hovered:
            score_text = font.render(f"High Score: {scores[self.key]}", True, BLACK)
            surface.blit(score_text, (self.rect.x, self.rect.y - 30))

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def click(self):
        if self.command:
            self.command()

# ----------------- Commands to Run Games -----------------
PYTHON = sys.executable

def run_stack():
    proc = subprocess.Popen([PYTHON, "src/stack_game.py"])
    proc.wait()
    scores["stack"] = read_score("stack")

def run_queue():
    proc = subprocess.Popen([PYTHON, "src/queue_game.py"])
    proc.wait()
    scores["queue"] = read_score("queue")

def run_deque():
    proc = subprocess.Popen([PYTHON, "src/deque_game.py"])
    proc.wait()
    scores["deque"] = read_score("deque")

# ----------------- Main Loop -----------------
def main():
    clock = pygame.time.Clock()
    buttons = [
        Button("Stack Game", 100, 50, 200, 50, run_stack, "stack"),
        Button("Queue Game", 100, 130, 200, 50, run_queue, "queue"),
        Button("Deque Game", 100, 210, 200, 50, run_deque, "deque"),
        Button("Reset Scores", 100, 290, 200, 50, reset_scores, reset=True)
    ]

    running = True
    while running:
        clock.tick(FPS)
        WIN.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.click()

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(WIN)

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
