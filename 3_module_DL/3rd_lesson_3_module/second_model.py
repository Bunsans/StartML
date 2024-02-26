from torch import nn


def create_conv_model():
    second_model = nn.Sequential(
        nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),
        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),
        nn.Flatten(),
        nn.Linear(4 * 4 * 64, 256),
        nn.BatchNorm1d(256),
        nn.Dropout(0.3),
        nn.ReLU(),
        nn.Linear(256, 32),
        nn.BatchNorm1d(32),
        nn.Dropout(0.3),
        nn.ReLU(),
        nn.Linear(32, 10),
    )
    return second_model
