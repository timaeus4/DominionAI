import torch.nn as nn
import torch.nn.functional as F


class DQN(nn.Module):

    def __init__(self, w, h, n, outputs):
        super(DQN, self).__init__()

        self.conv1 = nn.Conv2d(2, 4, kernel_size=5, stride=1)
        self.bn1 = nn.BatchNorm2d(4)
        self.conv2 = nn.Conv2d(4, 8, kernel_size=5, stride=1)
        self.bn2 = nn.BatchNorm2d(8)
        self.conv3 = nn.Conv2d(8, 16, kernel_size=5, stride=1)
        self.bn3 = nn.BatchNorm2d(16)
        #self.conv4 = nn.Conv2d(32, 32, kernel_size=4, stride=1)
        #self.bn4 = nn.BatchNorm2d(32)
        
        def conv2d_size_out(size, kernel_size=5, stride=1):
            return (size - (kernel_size - 1) - 1) // stride + 1
        #convw = conv2d_size_out(conv2d_size_out(w))
        #convh = conv2d_size_out(conv2d_size_out(h))
        convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(w)))
        convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(h)))
        #convw = conv2d_size_out(conv2d_size_out(conv2d_size_out(conv2d_size_out(w))))
        #convh = conv2d_size_out(conv2d_size_out(conv2d_size_out(conv2d_size_out(h))))
        print(convw)
        print(convh)
        linear_input_size = convw * convh * n
        self.head = nn.Linear(linear_input_size, outputs)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        #x = F.relu(self.bn4(self.conv4(x)))
        return self.head(x.view(x.size()[0], -1))