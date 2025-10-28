'''
MNIST dataset
MAX: 99.29%
'''
# import packages
# system packages
import time
# pytorch packages
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import Net_cifar_10
# data proccessing packages
import matplotlib.pyplot as plt


# init parameters
BATCH_SIZE = 256
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
EPOCHES = 100



# get data from MNIST
def get_data_loader(is_train):
    if is_train:
        to_tensor = transforms.Compose([
            transforms.Resize(40),
            transforms.RandomResizedCrop(32, scale=(0.64, 1.0), ratio=(1.0, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
            transforms.ToTensor(),
            transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010]),
            transforms.RandomErasing(p=0.5, scale=(0.02, 0.2), ratio=(0.3, 3.3))
        ])
    else:
        to_tensor = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.4914, 0.4822, 0.4465], [0.2023, 0.1994, 0.2010])
        ])
    data_set = datasets.CIFAR10("CIFAR10", train=is_train, transform=to_tensor, download=True)
    data_loader = DataLoader(data_set, batch_size=BATCH_SIZE, shuffle=is_train, num_workers=4, pin_memory=True, drop_last=is_train)
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
        
        # compute time
        batch_time = time.time() - batch_start_time
        batch_times.append(batch_time)
        epoch_time += batch_time
        
        # print the loss every batch
        if  batch_index and batch_index % 50 == 0:
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


def plot_train_history(losses, accuracies, epochs):
    # init figure
    plt.figure(figsize=(10, 6))
    epochs_range = range(1, epochs + 1)
    
    # plot losses
    plt.plot(epochs_range, losses, 'b-', linewidth=2, marker='o', 
             markersize=6, label='Training Loss')
    # plot accuracies
    plt.plot(epochs_range, accuracies, 'r--', linewidth=2, marker='s', 
             markersize=6, label='Test Accuracy')

    # set figure
    plt.xlabel('Epoch')
    plt.ylabel('Value')
    plt.title('Loss and Accuracy over Epochs in Training')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
    # plt.savefig('training_history_single.png', dpi=300, bbox_inches='tight')



def main():

    # get data
    train_data = get_data_loader(is_train=True)
    test_data = get_data_loader(is_train=False)
    
    # init model
    net = Net_cifar_10().to(DEVICE)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.001)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
    initeal_accuracy = evaluate(test_data, net)
    print()
    print(f"Using device: {DEVICE}")
    print(f"Initial accuracy: {initeal_accuracy:.4f}")
    
    # init lists
    times = []
    losses = []
    accuracies = []
    
    # start train
    print()
    print("Training...")
    best_accuracy = 0
    for epoch in range(EPOCHES):
        # train model
        loss, time = train_epoch(train_data, net, optimizer, epoch)
        accuracy = evaluate(test_data, net)
        current_lr = scheduler.get_last_lr()[0]
        print(f"Epoch {epoch:2d}: Loss = {loss:.4f}, Accuracy = {accuracy:.4f}, LR = {current_lr:.6f}, Time: {time:.2f}s")
        scheduler.step()
        
        # append lists
        times.append(time)
        losses.append(loss)
        accuracies.append(accuracy)
        
        # save best modul
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            torch.save(net.state_dict(), f'best_model\\best_cifar_10_accuracy_{best_accuracy:.4f}.pth')
    
    print(f"\nBest accuracy: {best_accuracy * 100:.2f}%")
    
    # plot figure
    print("\nGenerating training history plot...")
    plot_train_history(losses, accuracies, EPOCHES)
    plt.savefig('CIFAR10_train_history.png')


if __name__ == "__main__":
    print("\nImport packages successfully! ! !")
    main()
