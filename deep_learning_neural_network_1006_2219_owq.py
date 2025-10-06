# 代码生成时间: 2025-10-06 22:19:34
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# 定义一个简单的神经网络
class SimpleNeuralNetwork(nn.Module):
    def __init__(self):
        super(SimpleNeuralNetwork, self).__init__()
        # 定义网络层
        self.fc1 = nn.Linear(784, 128)  # 输入层到隐藏层
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(128, 10)   # 隐藏层到输出层

    def forward(self, x):
        # 前向传播
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# 数据加载和预处理
def load_data(batch_size):
    # 这里使用MNIST数据集作为示例
    from torchvision import datasets, transforms
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])
    # 下载并加载训练数据
    trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
    return trainloader

# 训练模型
def train_model(model, trainloader, epochs):
    criterion = nn.CrossEntropyLoss()  # 损失函数
    optimizer = optim.Adam(model.parameters(), lr=0.001)  # 优化器
    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in trainloader:
            # 将数据传递给网络
            outputs = model(images)
            # 计算损失
            loss = criterion(outputs, labels)
            # 反向传播和优化
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f'Epoch {epoch + 1}, Loss: {running_loss / len(trainloader)}')

# 主函数
def main():
    try:
        batch_size = 64
        epochs = 5
        # 实例化模型
        model = SimpleNeuralNetwork()
        trainloader = load_data(batch_size)
        # 训练模型
        train_model(model, trainloader, epochs)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
