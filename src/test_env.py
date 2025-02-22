from flappy_env import FlappyBirdEnv

# Initialize environment
env = FlappyBirdEnv()

# Reset environment to get the initial state
obs = env.reset()
done = False

# Run the environment with random actions
while not done:
    action = env.action_space.sample()  # Random actions (0 or 1)
    obs, reward, done, _ = env.step(action)
    env.render()  # Show the game

env.close()  # Close pygame when done
