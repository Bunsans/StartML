import torch
from torch import nn


def function04(x: torch.Tensor, y: torch.Tensor):
    n_steps = 2000

    step_size = 1e-2
    layer = nn.Linear(in_features=x.shape[1], out_features=1)

    for i in range(n_steps):
        y_pred = layer(x).ravel()

        mse = torch.mean((y_pred - y) ** 2)
        if mse < 0.3:
            break

        mse.backward()

        with torch.no_grad():
            layer.weight -= layer.weight.grad * step_size
            layer.bias -= layer.bias.grad * step_size

        layer.zero_grad()
    return layer
