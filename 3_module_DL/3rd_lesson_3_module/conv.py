from torch import nn


def create_conv_model():
    second_model = nn.Sequential(
        nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=2),
        nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5),
        nn.ReLU(),
        nn.MaxPool2d(kernel_size=3),
        nn.Flatten(),
        nn.Linear(3 * 3 * 64, 256),
        nn.ReLU(),
        nn.Linear(256, 10),
    )
