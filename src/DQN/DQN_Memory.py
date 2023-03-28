import random
from collections import deque


class DQN_Memory():

    def __init__(self, capacity, transition):
        self.memory = deque([], maxlen=capacity)
        self.Transition = transition
        
    def push_memory(self, *args):
        self.memory.append(self.Transition(*args))

    def pop_memory(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
        