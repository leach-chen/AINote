import numpy as np
import torch

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


from torch.utils.data import Dataset
from torch.utils.data import DataLoader

class ToyDataset(Dataset):
    def __init__(self, X, y):
        self.features = X
        self.labels = y

    def __getitem__(self, index):
        one_x = self.features[index]
        one_y = self.labels[index]
        return one_x, one_y

    def __len__(self):
        return self.labels.shape[0]


X_train = torch.tensor([
    [-1.2, 3.1],
    [-0.9, 2.9],
    [-0.5, 2.6],
    [2.3, -1.1],
    [2.7, -1.5]
])

y_train = torch.tensor([0, 0, 0, 1, 1])

X_test = torch.tensor([
    [-0.8, 2.8],
    [2.6, -1.6],
])

y_test = torch.tensor([0, 1])

train_ds = ToyDataset(X_train, y_train)
test_ds = ToyDataset(X_test, y_test)

print(len(train_ds))


train_loader = DataLoader(dataset = train_ds,batch_size=2,shuffle=True,num_workers=0,drop_last=True)

test_loader = DataLoader(dataset=test_ds, batch_size=2, shuffle=False, num_workers=0)

for idx,(x,y) in enumerate(train_loader):
    print(f"Batch {idx + 1}:", x, y)

##
model = NeuraNetwork(num_inputs=2, num_outputs=2)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1) #创建一个随机梯度下降（Stochastic Gradient Descent）优化器，负责根据梯度更新模型参数。
num_epochs = 3

for epoch in range(num_epochs):
    model.train()
    for batch_idx, (features, labels) in enumerate(train_loader):
        logits = model(features)  # 原始得分，形状 [B, 2]
        loss = F.cross_entropy(logits, labels)  # softmax + 负对数似然，一步完成
        optimizer.zero_grad()  # 清空上一轮梯度
        loss.backward()  # 计算梯度
        optimizer.step()  # 更新参数

        ### LOGGING
        print(f"Epoch: {epoch + 1:03d}/{num_epochs:03d}"
              f" | Batch {batch_idx + 1:03d}/{len(train_loader):03d}"
              f" | Train/Val Loss: {loss:.2f}")
    model.eval()
    # Optional model evaluation

model.eval()
with torch.no_grad():
    outputs = model(X_train)
    print(outputs)
torch.set_printoptions(sci_mode=False) #关闭张量打印时的科学计数法。默认 PyTorch 对很小的数会打印成 1.2e-05 这种形式，关掉后显示为 0.000012，更易读
probas = torch.softmax(outputs,dim=1)  #把logits 沿类别维度（dim=1）转成概率,每个值落在 (0, 1)
predictions = torch.argmax(probas,dim=1) #沿类别维度取最大概率的下标，即预测类别，形状 [N]，类型为int64
print(probas)
print(predictions)

torch.save(model.state_dict(), "model.pth")

model = NeuraNetwork(2, 2) # needs to match the original model exactly
model.load_state_dict(torch.load("model.pth", weights_only=True))