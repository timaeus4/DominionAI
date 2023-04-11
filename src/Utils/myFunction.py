# オリジナル関数集

from PIL import Image
import numpy as np
import random
import math
import torch
import torchvision.transforms as T

# ε-greedy法
def eps_greedy(s, e, d, step):
    sample = random.random()
    eps_threshold = e + (s- e) * \
        math.exp(-1. * step / d)
    return sample > eps_threshold

# 1次元配列をone-hotの2次元配列に変換        
def expand_line2plane(line, y):
    plane = np.zeros((len(line), y))
    for i in range(len(line)):
        j = 0
        while (line[i] > 0 and j < y):
            plane[i,j] = 1
            j += 1
            line[i] -= 1
    return plane

# 3次元配列をTensor型に変換
def convert_to_tensor(cube, device):
    cube = np.ascontiguousarray(cube, dtype=np.float32) / 255
    cube = torch.from_numpy(cube)
    resize = T.Compose([T.ToPILImage(),
            T.Resize(40, interpolation=Image.CUBIC),
            T.ToTensor()])
    return resize(cube).unsqueeze(0).to(device)

# int型をTensor型に変換    
def int2tensor(i, device):
    return torch.tensor([i], device=device, dtype=torch.long)