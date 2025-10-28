# import packages
# system packages
import time
# pytorch packages
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
# data proccessing packages
import matplotlib.pyplot as plt



"""
Model For CIFAR_10
"""
class Net_cifar_10(torch.nn.Module):

    def __init__(self, dropout_rate=0.3):
        super().__init__()
        # Conv
        # padding = (kernel_size - 1) / 2
        self.conv_layers = torch.nn.Sequential(           
            # 3 -> 64
            torch.nn.Conv2d(3, 64, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(64, 64, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(64),
            torch.nn.ReLU(inplace=True),
            torch.nn.MaxPool2d(2),  # 32 * 32 -> 16 * 16
            torch.nn.Dropout2d(dropout_rate/2),
            
            # 64 -> 128
            torch.nn.Conv2d(64, 128, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(128),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(128, 128, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(128),
            torch.nn.ReLU(inplace=True),
            torch.nn.MaxPool2d(2),  # 16 * 16 -> 8 * 8
            torch.nn.Dropout2d(dropout_rate/2),
            
            # 128 -> 256
            torch.nn.Conv2d(128, 256, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(256),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(256, 256, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(256),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(256, 256, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(256),
            torch.nn.ReLU(inplace=True),
            torch.nn.MaxPool2d(2),  # 8 * 8 -> 4 * 4
            torch.nn.Dropout2d(dropout_rate),
            
            # 256 -> 512
            torch.nn.Conv2d(256, 512, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(256, 512, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU(inplace=True),
            torch.nn.Conv2d(256, 512, kernel_size=3, padding=1),
            torch.nn.BatchNorm2d(512),
            torch.nn.ReLU(inplace=True),
            torch.nn.AdaptiveAvgPool2d((2, 2)), # 2 * 2
            torch.nn.Dropout2d(dropout_rate),
            
        )
        
        # Linear Connection
        self.fc_layers = torch.nn.Sequential(
            # 128 * 4 * 4 -> 1024
            torch.nn.Linear(512 * 2 * 2, 1024),
            torch.nn.BatchNorm1d(1024),
            torch.nn.ReLU(inplace=True),
            torch.nn.Dropout(dropout_rate),
            
            # 1024 -> 512
            torch.nn.Linear(1024, 512),
            torch.nn.BatchNorm1d(512),
            torch.nn.ReLU(inplace=True),
            torch.nn.Dropout(dropout_rate),
            
            # 512 -> 10
            torch.nn.Linear(512, 10)
        )
        
        # init weights
        self._initialize_weights()
    
    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, torch.nn.Conv2d):
                torch.nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    torch.nn.init.constant_(m.bias, 0)
            elif isinstance(m, torch.nn.BatchNorm2d):
                torch.nn.init.constant_(m.weight, 1)
                torch.nn.init.constant_(m.bias, 0)
            elif isinstance(m, torch.nn.Linear):
                torch.nn.init.normal_(m.weight, 0, 0.01)
                torch.nn.init.constant_(m.bias, 0)
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        x = self.fc_layers(x)
        return torch.nn.functional.log_softmax(x, dim=1)