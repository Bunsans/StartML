import numpy as np

import torch
from torch import nn
from torch.nn import functional as F


def create_model():
    model = nn.Sequential(nn.Linear(100, 10), nn.ReLU(), nn.Linear(10, 1))
    return model

