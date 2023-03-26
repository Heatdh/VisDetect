import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision.transforms as transforms

class BananaDetect_boundary_box(nn.Module):
    def __init__(self):
        super(BananaDetect_boundary_box, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 4)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
    def train(self, trainloader, testloader, epochs=2, lr=0.001, momentum=0.9):
        criterion = nn.MSELoss()
        optimizer = optim.SGD(self.parameters(), lr=lr, momentum=momentum)
        for epoch in range(epochs):
            running_loss = 0.0
            for i, data in enumerate(trainloader, 0):
                inputs, labels = data
                optimizer.zero_grad()
                outputs = self(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()
                if i % 2000 == 1999:
                    print('[%d, %5d] loss: %.3f' %
                          (epoch + 1, i + 1, running_loss / 2000))
                    running_loss = 0.0
        print('Finished Training')

    def test(self, testloader):
        dataiter = iter(testloader)
        images, labels = dataiter.next()
        outputs = self(images)
        print('GroundTruth: ', ' '.join('%5s' % labels[j] for j in range(4)))
        print('Predicted: ', ' '.join('%5s' % outputs[j] for j in range(4)))

    def save(self, path):
        torch.save(self.state_dict(), path)
        
      
