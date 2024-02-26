import torch


def function03(x: torch.Tensor, y: torch.Tensor):
    step_size = 1e-2
    w = torch.randn(x.shape[1], requires_grad=True, dtype=torch.float32)
    # b = torch.rand(1, requires_grad=True)

    while 1:
        y_pred = torch.matmul(x, w)  # + b

        mse = torch.mean((y_pred - y) ** 2)
        if mse < 1:
            break

        mse.backward()

        with torch.no_grad():
            w -= w.grad * step_size
            # b -= b.grad * step_size

        w.grad.zero_()
        # b.grad.zero_()
    return w
