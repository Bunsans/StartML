import torch


def function02(tensor: torch.Tensor) -> torch.Tensor:
    return torch.randn(tensor.shape[1], requires_grad=True, dtype=torch.float32)
