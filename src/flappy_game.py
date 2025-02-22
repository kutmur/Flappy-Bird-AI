import pygame
import random
from stable_baselines3 import PPO
from flappy_env import FlappyBirdEnv

# Initialize pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = 3
GROUND_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load assets
bird_img = pygame.image.load("assets/bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))
bg_img = pygame.image.load("assets/background.png")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
best_score = 0  # Track the highest score


class Bird:
    def __init__(self):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, 40, 30)

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

        if self.y <= 0:
            self.y = 0
        elif self.y >= SCREEN_HEIGHT - GROUND_HEIGHT:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT


class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - 200)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH,
                                       SCREEN_HEIGHT - self.height - PIPE_GAP)

    def move(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)


def game_loop():
    global best_score  # Access global best score variable
    bird = Bird()
    pipes = [Pipe(400)]
    running = True
    score = 0

    while running:
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()
        screen.blit(bird_img, (bird.x, bird.y))

        for pipe in pipes:
            pipe.move()
            pipe.draw(screen)

            if pipe.x < -PIPE_WIDTH:
                pipes.remove(pipe)
                pipes.append(Pipe(400))
                score += 1

            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                running = False

        # Update Best Score
        if score > best_score:
            best_score = score

        # Display Scoreboard
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}  Best: {best_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    return "menu"  # Return to main menu when player dies


def play_ai():
    env = FlappyBirdEnv()

    # Check if the AI model exists
    try:
        model = PPO.load("models/flappy_dqn", env=env)
        print("✅ AI model loaded successfully!")
    except:
        print("❌ No trained AI model found! Train AI first using: python src/train_ai.py")
        return "menu"

    obs = env.reset()
    done = False

    while not done:
        action, _ = model.predict(obs)
        obs, reward, done, _ = env.step(action)
        env.render()

    env.close()
    return "menu"


def main_menu():
    while True:
        screen.fill(BLUE)
        font = pygame.font.Font(None, 36)

        title_text = font.render("Flappy Bird", True, WHITE)
        start_text = font.render("1 - Play Manually", True, WHITE)
        ai_text = font.render("2 - Let AI Play", True, WHITE)
        quit_text = font.render("Q - Quit", True, WHITE)

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 200))
        screen.blit(ai_text, (SCREEN_WIDTH // 2 - ai_text.get_width() // 2, 250))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # User Mode
                    result = game_loop()
                    if result == "quit":
                        pygame.quit()
                        return
                elif event.key == pygame.K_2:  # AI Mode
                    result = play_ai()  # Call AI play function
                    if result == "quit":
                        pygame.quit()
                        return
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return


if __name__ == "__main__":
    main_menu()
