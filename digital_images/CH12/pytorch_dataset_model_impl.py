import torch
from torch.utils.data import Dataset


class DatasetImpl(Dataset):
    # 樣本資料（答案）：由 6 個 (x, y) 座標組成的 NumPy 陣列
    def __init__(self, data_points):
        self.data_points = data_points

    def __getitem__(self, index):
        x = torch.tensor(self.data_points[index][0],dtype=torch.float)
        y = torch.tensor(self.data_points[index][1],dtype=torch.float)

        return x,y

    def __len__(self):
        return len(self.data_points)


class ModelImpl(torch.nn.Module):
    def __init__(self):
        super(ModelImpl, self).__init__()

        self.a = torch.nn.Parameter(torch.randn(1, requires_grad=True))
        self.b = torch.nn.Parameter(torch.randn(1, requires_grad=True))

    def forward(self, x):
        return self.a * x + self.b