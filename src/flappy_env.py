import pygame
import gym
import numpy as np
import random
from gym import spaces

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = 3
GROUND_HEIGHT = 50

# Load Assets
pygame.init()
bird_img = pygame.image.load("assets/bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))
bg_img = pygame.image.load("assets/background.png")
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

class FlappyBirdEnv(gym.Env):
    def __init__(self):
        super(FlappyBirdEnv, self).__init__()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.score = 0
        self.best_score = 0  # Store best score

        # Bird properties
        self.bird_x = 100
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_velocity = 0
        self.bird_rect = pygame.Rect(self.bird_x, self.bird_y, 40, 30)

        # Pipe properties
        self.pipes = [self.create_pipe()]

        # Action space (0: do nothing, 1: flap)
        self.action_space = spaces.Discrete(2)

        # Observation space (bird position, velocity, pipe positions)
        self.observation_space = spaces.Box(
            low=np.array([0, -10, 0, 0]),
            high=np.array([SCREEN_HEIGHT, 10, SCREEN_WIDTH, SCREEN_HEIGHT]),
            dtype=np.float32
        )

    def create_pipe(self):
        height = random.randint(100, SCREEN_HEIGHT - 200)
        return {
            "x": SCREEN_WIDTH,
            "top": pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height),
            "bottom": pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP)
        }

    def reset(self):
        self.bird_y = SCREEN_HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = [self.create_pipe()]
        self.score = 0
        return np.array([self.bird_y, self.bird_velocity, self.pipes[0]["x"], self.pipes[0]["top"].height], dtype=np.float32)

    def step(self, action):
        self.bird_velocity += GRAVITY
        if action == 1:
            self.bird_velocity = FLAP_STRENGTH

        self.bird_y += self.bird_velocity
        self.bird_rect.y = self.bird_y

        for pipe in self.pipes:
            pipe["x"] -= PIPE_SPEED
            pipe["top"].x = pipe["x"]
            pipe["bottom"].x = pipe["x"]

        if self.pipes[0]["x"] < -PIPE_WIDTH:
            self.pipes.pop(0)
            self.pipes.append(self.create_pipe())
            self.score += 1
            if self.score > self.best_score:
                self.best_score = self.score

        done = False
        reward = 1  # Small reward for staying alive

        # **🆕 Reward for staying in the optimal flying zone (center)**
        if SCREEN_HEIGHT // 3 < self.bird_y < SCREEN_HEIGHT // 2:
            reward += 5  # Encourage staying in the best zone

        # **🆕 Extra reward for passing pipes perfectly**
        if self.pipes[0]["x"] == self.bird_x:
            reward += 10  # Reward precise timing

        # **🆕 Reward for smooth movement (no sudden jumps)**
        if abs(self.bird_velocity) < 3:
            reward += 3  # Encourage stable flight

        # **🆕 Small penalty for unnecessary flaps**
        if action == 1:
            reward -= 1  # Discourage excessive jumping

        # Collision detection
        if self.bird_y < 0 or self.bird_y > SCREEN_HEIGHT - GROUND_HEIGHT:
            done = True
            reward = -100  # Large penalty for hitting ground
        for pipe in self.pipes:
            if self.bird_rect.colliderect(pipe["top"]) or self.bird_rect.colliderect(pipe["bottom"]):
                done = True
                reward = -100  # Large penalty for hitting pipe

        return np.array([self.bird_y, self.bird_velocity, self.pipes[0]["x"], self.pipes[0]["top"].height], dtype=np.float32), reward, done, {}

    def render(self):
        self.screen.blit(bg_img, (0, 0))  # Draw background
        self.screen.blit(bird_img, (self.bird_x, self.bird_y))  # Draw bird

        for pipe in self.pipes:
            pygame.draw.rect(self.screen, (0, 255, 0), pipe["top"])  # Draw top pipe
            pygame.draw.rect(self.screen, (0, 255, 0), pipe["bottom"])  # Draw bottom pipe

        score_text = pygame.font.Font(None, 36).render(f"Score: {self.score}  Best: {self.best_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))  # Display score

        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        pygame.quit()
