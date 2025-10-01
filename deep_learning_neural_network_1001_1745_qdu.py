# 代码生成时间: 2025-10-01 17:45:35
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

# Define a simple neural network model
class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        # Define the layers of the neural network
        self.fc1 = nn.Linear(in_features=784, out_features=128)  # Input layer (784) to hidden layer (128)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(in_features=128, out_features=10)  # Hidden layer (128) to output layer (10)
    
    def forward(self, x):
        # Define the forward pass
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x

# Parameters
input_size = 784  # 28x28 images
output_size = 10  # 10 classes (digits 0-9)
batch_size = 64
learning_rate = 0.001
num_epochs = 5

# Generate dummy data for demonstration purposes
# In a real-world scenario, this would be replaced with actual image data
X = torch.randn(batch_size, input_size)
y = torch.randint(0, output_size, (batch_size,))

# Create a dataset and data loader
dataset = TensorDataset(X, y)
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Initialize the model, loss function, and optimizer
model = NeuralNetwork()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for batch_idx, (data, target) in enumerate(data_loader):
        # Zero the gradients
        optimizer.zero_grad()
        
        # Forward pass
        output = model(data)
        loss = criterion(output, target)
        
        # Backward pass and optimize
        loss.backward()
        optimizer.step()
        
        if batch_idx % 10 == 0:
            print(f"Epoch [{epoch+1}/{num_epochs}], Batch [{batch_idx+1}/{len(data_loader)}], Loss: {loss.item():.4f}")

# Save the model
torch.save(model.state_dict(), 'neural_network_model.pth')

# Function to load the model
def load_model():
    model = NeuralNetwork()
    model.load_state_dict(torch.load('neural_network_model.pth'))
    return model

# Function to predict using the model
def predict(model, data):
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        output = model(data)
        _, predicted = torch.max(output, 1)
    return predicted

# Example usage:
# model = load_model()
# prediction = predict(model, X)
