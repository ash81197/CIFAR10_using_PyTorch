# Importing Essential Libraries
import time
import torch
import torchvision
import torch.nn as nn

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

print(device)

batch_size = 256

# Class
class LeNet(nn.Module):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv_model = nn.Sequential(nn.Conv2d(3, 6, 5).cuda(),
                                        nn.Tanh().cuda(),
                                        nn.AvgPool2d(2, stride = 2).cuda(),
                                        nn.Conv2d(6, 16, 5).cuda(),
                                        nn.Tanh().cuda(),
                                        nn.AvgPool2d(2, stride = 2).cuda())
        
        self.dense_model = nn.Sequential(nn.Linear(400, 120).cuda(),
                                         nn.Tanh().cuda(),
                                         nn.Linear(120, 84).cuda(),
                                         nn.Tanh().cuda(),
                                         nn.Linear(84, 10).cuda())
    def forward(self, x):
        #x = x.to(device)
        y = self.conv_model(x)
        # Flatten the result from conv model
        y = torch.flatten(y, 1)
        y = self.dense_model(y)
        return y

# Training set
trainset = torchvision.datasets.CIFAR10(root = './data',
                                        train = True,
                                        download = True,
                                        transform = torchvision.transforms.ToTensor())

trainloader = torch.utils.data.DataLoader(trainset, batch_size = batch_size, shuffle = True)

# Testing set
testset = torchvision.datasets.CIFAR10(root = './data',
                                       train = False,
                                       download = True,
                                       transform = torchvision.transforms.ToTensor())

testloader = torch.utils.data.DataLoader(testset, batch_size = batch_size, shuffle = False)

net = LeNet()
net = net.to(device)
loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters())

# Evaluating Model Performance
def model_evalutaion(dataloader):
    total = 0
    correct = 0
    for data in dataloader:
        #image_data, labels = data
        #image_data = data[0].to(device), data[1].to(device)
        image_data, labels = data
        image_data = image_data.to(device)
        labels = labels.to(device)
        out = net(image_data)
        max_values, pred_class = torch.max(out, dim = 1)
        total += labels.shape[0]
        correct += (pred_class == labels).sum().item()
        accuracy = (100 * correct) / total
    return accuracy

start = time.perf_counter()
total_epochs = 2
for i in range(total_epochs):
    for data in trainloader:
        image_data, labels = data
        image_data = image_data.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        out = net(image_data)
        loss = loss_func(out, labels)
        loss.backward()
        optimizer.step()
    train_acc = model_evalutaion(trainloader)
    test_acc = model_evalutaion(testloader)
    print("Epoch: ", i+1,"Train Accuracy: ", train_acc, "Test Accuracy: ", test_acc)
end = time.perf_counter()
print("Time taken to execute the program is: ", end-start)
