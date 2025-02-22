import pygame
import torch
from stable_baselines3 import PPO  # Use PPO instead of DQN
from flappy_env import FlappyBirdEnv

# Load the trained PPO model
model = PPO.load("../models/flappy_dqn")

# Initialize Flappy Bird Environment
env = FlappyBirdEnv()
obs = env.reset()
done = False
score = 0

while not done:
    action, _ = model.predict(obs)  # AI chooses an action
    obs, reward, done, _ = env.step(action)
    score += reward
    env.render()  # Show the game

env.close()
print(f"🤖 AI Score: {score}")
