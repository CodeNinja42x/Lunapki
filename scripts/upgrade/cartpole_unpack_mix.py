import gym

env = gym.make('CartPole-v1')
observation = env.reset()

for _ in range(1000):  # Corrected syntax here
    env.render()
    action = env.action_space.sample()  # Take a random action
    observation, reward, done, truncated, info = env.step(action)
    if done or truncated:
        observation = env.reset()

env.close()
