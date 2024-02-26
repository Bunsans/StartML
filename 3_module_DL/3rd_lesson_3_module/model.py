from torch import nn


def create_mlp_model():
    first_model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(28 * 28, 256),
        nn.ReLU(),
        nn.Linear(256, 100),
        nn.ReLU(),
        nn.Linear(100, 10),
    )

    return first_model
