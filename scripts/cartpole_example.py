import gym

env = gym.make('CartPole-v1')
observation = env.reset()

for _ in range(1000):
    env.render()  # Add render mode if needed: render_mode="rgb_array"
    action = env.action_space.sample()  # Take a random action
    observation, reward, done, truncated, info = env.step(action)
    if done or truncated:
        observation = env.reset()

env.close()
