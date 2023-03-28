import torch.nn as nn
import torchvision.models as models

class convResnet(nn.Module):
    def __init__(self):
        super(convResnet, self).__init__()
        self.resnet = models.resnet18(pretrained=True)
        self.resnet.fc = nn.Linear(512, 5)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        x = self.resnet(x)
        return x
