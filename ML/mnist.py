'''
MNIST dataset
MAX: 
'''
# import packages
import time
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt


# init parameters
BATCH_SIZE = 128
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EPOCHES = 10


# define model
class Net(torch.nn.Module):

    def __init__(self):
        super().__init__()
        # Conv
        # padding = (kernel_size - 1) / 2
        self.conv_layers = torch.nn.Sequential(
            # 1 -> 16
            torch.nn.Conv2d(1, 16, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),  # 28 * 28 -> 14 * 14
            
            # 16 -> 32
            torch.nn.Conv2d(16, 32, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(2),  # 14 * 14 -> 7 * 7
            
            # 32 -> 64
            torch.nn.Conv2d(32, 64, kernel_size=3, padding=1),
            torch.nn.ReLU(),
            torch.nn.AdaptiveAvgPool2d((4, 4))  # 4 * 4
        )
        
        # Linear Connection
        self.fc_layers = torch.nn.Sequential(
            torch.nn.Linear(64 * 4 * 4, 128),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.3),
            torch.nn.Linear(128, 10)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return torch.nn.functional.log_softmax(x, dim=1)



# get data from MNIST
def get_data_loader(is_train):
    to_tensor = transforms.Compose([
        transforms.ToTensor(),
        # transforms.Normalize((0.1307,), (0.3081,))
    ])
    data_set = datasets.MNIST("", train=is_train, transform=to_tensor, download=True)
    data_loader = DataLoader(data_set, batch_size=BATCH_SIZE, shuffle=True)
    return data_loader


# train function
def train_epoch(train_data, net, optimizer, epoch):
    net.train()
    total_loss = 0.
    epoch_time = 0.
    batch_times = []
    for batch_index, (x, y) in enumerate(train_data):
        batch_start_time = time.time()
        x, y = x.to(DEVICE), y.to(DEVICE)
        optimizer.zero_grad()
        output = net(x)
        loss = torch.nn.functional.nll_loss(output, y)
        loss.backward()
        optimizer.step()
        
        # add total_loss
        total_loss += loss.item()
        
        # comput time
        batch_time = time.time() - batch_start_time
        batch_times.append(batch_time)
        epoch_time += batch_time
        
        # print the loss every batch
        if batch_index % 100 == 0:
            batch_time = sum(batch_times)
            print(f'Epoch {epoch:2d}: [{batch_index * len(x):5d}/{len(train_data.dataset)}\t'
                  f'({100. * batch_index / len(train_data):.0f}%)]\tLoss: {loss.item():.6f}\t'
                  f'Time: {batch_time:.2f}s')
            batch_times = []
            
    return total_loss/len(train_data), epoch_time


# evaluate function
def evaluate(test_data, net):
    net.eval()
    n_correct = 0
    n_total = 0
    with torch.no_grad():
        for (x, y) in test_data:
            x, y = x.to(DEVICE), y.to(DEVICE)
            output = net(x)
            predicted = output.max(1)[1]
            n_total += y.size(0)
            n_correct += (predicted == y).sum().item()
    net.train()
    return n_correct / n_total



def main():

    # get data
    train_data = get_data_loader(is_train=True)
    test_data = get_data_loader(is_train=False)
    
    # init 
    net = Net().to(DEVICE)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    print(f"Using device: {DEVICE}")
    print(f"Initial accuracy: {evaluate(test_data, net):.4f}")
    
    # start train
    print()
    print("Training...")
    best_accuracy = 0
    for epoch in range(EPOCHES):
        loss, time = train_epoch(train_data, net, optimizer, epoch)
        accuracy = evaluate(test_data, net)
        
        print(f"Epoch {epoch:2d}: Loss = {loss:.4f}, Accuracy = {accuracy:.4f}, Time: {time:.2f}s")
        
        # save best modul
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            torch.save(net.state_dict(), 'best_model\\best_mnist.pth')
    
    print(f"\nBest accuracy: {best_accuracy:.4f}")

    '''
    for (n, (x, _)) in enumerate(test_data):
        if n > 3:
            break
        predict = torch.argmax(net.forward(x[0].view(-1, 28*28)))
        plt.figure(n)
        plt.imshow(x[0].view(28, 28))
        plt.title("prediction: " + str(int(predict)))
    plt.show()
    '''


if __name__ == "__main__":
    print("\nImport packages successfully! ! !")
    main()
