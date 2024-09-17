import gym
from gym import spaces
import numpy as np

class CustomTradingEnv(gym.Env):
    def __init__(self):
        super(CustomTradingEnv, self).__init__()
        self.action_space = spaces.Discrete(3)  # Example: Buy, Hold, Sell
        self.observation_space = spaces.Box(low=0, high=1, shape=(10,), dtype=np.float32)  # Example observation space

    def reset(self):
        return np.random.rand(10)  # Return an initial observation

    def step(self, action):
        next_state = np.random.rand(10)  # Simulate next state
        reward = np.random.rand(1)  # Simulate reward
        done = False  # Example logic for ending the episode
        return next_state, reward, done, {}

    def render(self, mode='human'):
        pass  # Visualization logic (optional)

    def close(self):
        pass  # Cleanup (optional)

if __name__ == "__main__":
    env = CustomTradingEnv()
    obs = env.reset()
    print("Initial Observation:", obs)

    for _ in range(10):
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        print(f"Action: {action}, Observation: {obs}, Reward: {reward}, Done: {done}")

    env.close()
