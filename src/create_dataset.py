import random

import numpy as np
import torch

from custom_env import make_env
from train_model import load_model

if __name__ == '__main__':
    play_iterations = 50_000
    num_data_points = 10_000
    seed = 0
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.backends.cudnn.deterministic = True

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    q_network = load_model("../runs/20230927-233906/models/model_9999999.pt").to(device)

    env = make_env(random.randint(1,100000), save_interval=play_iterations//num_data_points)
    obs, info = env.reset(seed=seed)
    for i in range(play_iterations):
        if i % 1000 == 0:
            print(i)
        # action by random
        if random.random() < 0.01:
            action = random.randint(0, 3)

        # action by model
        else:
            tensor_obs = torch.Tensor(np.array(obs)).to(device).unsqueeze(0)
            q_values = q_network(tensor_obs)
            action = q_values.argmax(dim=1).item()

        next_obs, reward, terminated, truncated, info = env.step(action)
        obs = next_obs
    
    env.reset()
    env.save_data()
    env.close()