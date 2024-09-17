import gym

# Specify the render mode when creating the environment
env = gym.make('CartPole-v1', render_mode='human')  # or 'rgb_array' for pixel-based rendering

observation = env.reset()

for _ in range(1000):  # Corrected syntax here
    env.render()  # This will now use the specified render mode
    action = env.action_space.sample()  # Take a random action
    observation, reward, done, truncated, info = env.step(action)
    if done or truncated:
        observation = env.reset()

env.close()
