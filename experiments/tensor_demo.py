import torch

x = torch.tensor([
    [1, 2, 3],
    [4, 5, 6]
])

print("Tenseur x :")
print(x)

print("Shape de x :")
print(x.shape)

print("Type des données :")
print(x.dtype)

y = torch.tensor([
    [10, 20, 30],
    [40, 50, 60]
])

print("Addition x + y :")
print(x + y)