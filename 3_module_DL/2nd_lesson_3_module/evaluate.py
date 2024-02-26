import numpy as np

import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torch.optim import Optimizer


@torch.inference_mode()
def evaluate(model: nn.Module, data_loader: DataLoader, loss_fn):
    model.eval()
    total_loss = 0
    for x_batch, y_batch in data_loader:
        output = model(x_batch)
        loss = loss_fn(output, y_batch)
        total_loss += loss
    return total_loss / len(data_loader)
