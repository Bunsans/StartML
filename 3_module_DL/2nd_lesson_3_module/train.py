import numpy as np

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torch.optim import Optimizer


def train(model: nn.Module, data_loader: DataLoader, optimizer: Optimizer, loss_fn):
    total_loss = 0
    model.train()
    for x_batch, y_batch in data_loader:
        optimizer.zero_grad()
        # forward
        output = model(x_batch)

        loss = loss_fn(output, y_batch)
        loss.backward()
        total_loss += loss.item()

        print(round(loss.item(), 5))
        optimizer.step()
    return total_loss / len(data_loader)
