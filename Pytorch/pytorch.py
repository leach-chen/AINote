import torch
import numpy as np

tensor0d = torch.tensor(1)
tensor1d = torch.tensor([1, 2, 3])
tensor2d = torch.tensor([[1, 2], [3, 4]])
tensor3d = torch.tensor([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
ary3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
tensor3d_2 = torch.tensor(ary3d)
tensor3d_3 = torch.from_numpy(ary3d)

print(torch.__version__)
print(tensor0d)
print(tensor1d)
print(tensor2d)
print(tensor3d)
print(ary3d)
print(tensor3d_2)
print(tensor3d_3)

print(tensor1d.shape)
print(tensor2d.shape)
print(tensor3d.shape)

import torch.nn.functional as F
from torch.autograd import grad

y = torch.tensor([1.0])
x1 = torch.tensor([1.1])
w1 = torch.tensor([2.2], requires_grad=True)
b = torch.tensor([0.0], requires_grad=True)

z = x1 * w1 + b
a = torch.sigmoid(z)

loss = F.binary_cross_entropy(a, y)
grad_L_w1 = grad(loss, w1, retain_graph=True)
grad_L_b = grad(loss, b, retain_graph=True)
print(loss)
print(grad_L_w1)
print(grad_L_b)

loss.backward()
print(w1.grad)
print(b.grad)


class NeuraNetwork(torch.nn.Module):
    def __init__(self, num_inputs, num_outputs):
        super().__init__()
        self.layers = torch.nn.Sequential(
            # 1st hidden layer
            torch.nn.Linear(num_inputs, 30),
            torch.nn.ReLU(),

            # 2nd hidden layer
            torch.nn.Linear(30, 20),
            torch.nn.ReLU(),

            # output layer
            torch.nn.Linear(20, num_outputs)
        )

    def forward(self, x):
        logits = self.layers(x)
        return logits


model = NeuraNetwork(num_inputs=50, num_outputs=3)
print(model)

num_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print("Total number of trainable model parameters:", num_params)
print(model.layers[0].weight)
print(model.layers[0].weight.shape)

torch.manual_seed(123)

X = torch.rand((1, 50))
out = model(X)
print(out)

with torch.no_grad():
    out = model(X)
print(out)

with torch.no_grad():
    out = torch.softmax(model(X), dim=1)
print(out)