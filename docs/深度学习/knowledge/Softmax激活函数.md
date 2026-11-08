## Softmax 函数详解

Softmax 是深度学习中**多分类问题输出层的标准激活函数**，能将任意实数向量转换为概率分布。

---

### 数学定义

对于输入向量 \(x = [x_1, x_2, ..., x_C]\)，其中 \(C\) 是类别总数：

$$
\text{Softmax}(x_i) = \frac{e^{x_i}}{\sum_{j=1}^{C} e^{x_j}}, \quad i = 1, 2, ..., C
$$

---

### 输出性质

| 性质 | 说明 |
|---|---|
| **非负** | 指数函数保证 \(e^{x_i} > 0\)，每个输出都是正数 |
| **和为 1** | \(\sum_{i=1}^{C} \text{Softmax}(x_i) = 1\)，所有概率之和为 1 |
| **单调性** | 输入 \(x_i\) 越大，输出概率也越大（保持相对大小） |
| **可微** | 处处可导，可用于反向传播 |

---

### 直觉理解

> Softmax 做了什么？
>
> 1. 对每个输入取指数 \(e^{x_i}\) → 把负数变正，把大数变得更大
> 2. 除以所有指数之和 → 归一化，使总和等于 1
>
> 结果就是一个**合法的概率分布**。

---

### 一个具体例子

假设 3 分类问题，模型输出（logits）：

$$
x = [2.0, 1.0, 0.1]
$$

**Step 1：计算指数**

$$e^{2.0} = 7.389$$
$$e^{1.0} = 2.718$$
$$e^{0.1} = 1.105$$

**Step 2：求总和**

$$7.389 + 2.718 + 1.105 = 11.212$$

**Step 3：归一化**

$$P(\text{类别1}) = \frac{7.389}{11.212} = 0.659 \quad (65.9\%)$$
$$P(\text{类别2}) = \frac{2.718}{11.212} = 0.242 \quad (24.2\%)$$
$$P(\text{类别3}) = \frac{1.105}{11.212} = 0.099 \quad (9.9\%)$$

**预测结果：类别 1**（概率最高）

---

### 数值稳定性问题

当 \(x_i\) 很大时（如 \(x_i = 100\)），\(e^{100}\) 会导致**数值溢出**。

**解决方案：减去最大值**

$$
\text{Softmax}(x_i) = \frac{e^{x_i - \max(x)}}{\sum_{j=1}^{C} e^{x_j - \max(x)}}
$$

为什么有效？
- 减去最大值后，最大值为 0，所有指数 \(\leq 1\)
- 不会改变最终结果（指数运算的性质保证）

**例子：** \(x = [100, 99, 98]\)

$$\max(x) = 100$$

$$e^{100-100} + e^{99-100} + e^{98-100} = e^0 + e^{-1} + e^{-2} = 1 + 0.368 + 0.135 = 1.503$$

结果与直接计算完全一致，但避免了溢出。

---

### Softmax 的导数

在反向传播中需要计算 Softmax 的导数。

对于输出 \(s_i = \text{Softmax}(x_i)\)，其偏导数为：

**情况 1：当 \(i = j\) 时**

$$\frac{\partial s_i}{\partial x_j} = s_i (1 - s_i)$$

**情况 2：当 \(i \neq j\) 时**

$$\frac{\partial s_i}{\partial x_j} = -s_i s_j$$

**统一写成：**

$$
\frac{\partial s_i}{\partial x_j} = s_i (\delta_{ij} - s_j)
$$

其中 \(\delta_{ij}\) 是克罗内克函数（\(\delta_{ij} = 1\) 当 \(i=j\)，否则为 0）

---

### Softmax 与交叉熵损失

多分类任务中，Softmax 通常与交叉熵损失（Cross-Entropy Loss）配合使用：

$$
\text{Loss} = -\sum_{i=1}^{C} y_i \log(s_i)
$$

其中：
- \(y_i\)：one-hot 编码的真实标签（只有真实类别为 1，其余为 0）
- \(s_i\)：Softmax 输出的概率

**简化**（因为 one-hot 只有一个位置为 1）：

$$
\text{Loss} = -\log(s_{\text{真实类别}})
$$

**反向传播的关键特性：**

$$
\frac{\partial \text{Loss}}{\partial x_i} = s_i - y_i
$$

这是一个非常简洁的梯度形式，也是 Softmax + CrossEntropy 成为黄金组合的原因。

---

### 代码实现

#### Python 原生实现

```python
import numpy as np

def softmax(x):
    # 数值稳定性处理
    x = x - np.max(x)
    exp_x = np.exp(x)
    return exp_x / np.sum(exp_x)

# 使用
logits = np.array([2.0, 1.0, 0.1])
probs = softmax(logits)
print(probs)  # [0.659, 0.242, 0.099]
print(np.sum(probs))  # 1.0
```

#### PyTorch 实现

```python
import torch.nn as nn
import torch

# 方法1：直接使用
softmax = nn.Softmax(dim=1)  # dim=1 表示对类别维度
probs = softmax(logits)

# 方法2：结合 CrossEntropyLoss（推荐）
# 注意：CrossEntropyLoss 内部已经包含 Softmax，不需要手动添加
criterion = nn.CrossEntropyLoss()
loss = criterion(logits, labels)  # 直接传入 logits
```

---

### 与 Sigmoid 的区别

| | **Softmax** | **Sigmoid** |
|---|---|---|
| **适用场景** | 多分类（互斥） | 二分类 / 多标签分类 |
| **输出** | 概率向量（和为 1） | 单个概率值（0~1） |
| **类别关系** | 类别互斥（只能选一个） | 类别独立（可以多个同时成立） |
| **公式** | \(\frac{e^{x_i}}{\sum e^{x_j}}\) | \(\frac{1}{1+e^{-x}}\) |

**什么时候用？**

| 场景 | 使用 |
|---|---|
| 手写数字识别（0~9 选一个） | **Softmax** |
| 猫/狗二分类 | **Sigmoid** |
| 一张图同时识别"猫、狗、人"（多标签） | **Sigmoid**（每个标签独立） |
| 新闻分类（政治/体育/科技 选一个） | **Softmax** |

---

### Softmax 的温度参数

Softmax 有一个扩展版本，引入**温度参数 \(T\)**：

$$
\text{Softmax}(x_i) = \frac{e^{x_i / T}}{\sum_{j=1}^{C} e^{x_j / T}}
$$

| \(T\) 值 | 效果 |
|---|---|
| \(T = 1\) | 标准 Softmax |
| \(T > 1\) | 概率分布更平滑（更"软"），各类别概率接近 |
| \(T < 1\) | 概率分布更锐利（更"硬"），最大值更突出 |

**应用场景：** 知识蒸馏（Knowledge Distillation）中，用高温 Softmax 让学生模型学习更丰富的类别关系。

---
