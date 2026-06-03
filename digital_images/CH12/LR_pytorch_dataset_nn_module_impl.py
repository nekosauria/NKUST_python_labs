import numpy
import matplotlib.pyplot as plt
import torch
from digital_images.CH12.pytorch_dataset_model_impl import DatasetImpl, ModelImpl
from torch.utils.data import DataLoader
from torch.utils.data import SequentialSampler


# 設定超參數 (Hyperparameters)
n_epoch = 4000  # 訓練輪數（完整掃過整個資料集的次數）
batch_size = 2  # Mini-batch 大小（每次挑選多少筆資料來計算梯度並更新參數）
eta = 0.01  # Learning rate（學習率），控制每次參數更新的步長

# 樣本資料（答案）：由 6 個 (x, y) 座標組成的 NumPy 陣列
data_points = numpy.array([
    [0.11, 1.24],
    [0.20, 1.40],
    [0.49, 2.00],
    [0.65, 2.27],
    [0.67, 2.41],
    [0.83, 2.52]
])

# 準備 LRDataset
lr_dataset = DatasetImpl(data_points)

index = list(range(len(lr_dataset)))
# index 打散順序
sampler = SequentialSampler(index)
# Shuffle, batch_size 實作分批訓練處理 class
lr_loader = DataLoader(dataset=lr_dataset, batch_size=batch_size, sampler=sampler)

lr_model = ModelImpl()

# 準備自動調參工具（優化器）
# 起始值從 ModelImpl 拿
optimizer = torch.optim.SGD(lr_model.parameters(), eta)

# 印出初始（第 0 輪）的斜率 a 和截距 b
print(f"[epoch 0], lr_model.a = {lr_model.a[0]:.4f}, lr_model.b = {lr_model.b[0]:.4f}")

# 開始跑線性回歸訓練
for epoch in range(n_epoch):

    for x,y in lr_loader:

        lr_model.train()
        y_hat = lr_model(x)

        # 訊量誤差值
        y_error = y - y_hat
        # 計算均方誤差 (Mean Squared Error, MSE)
        mse_loss = (y_error ** 2).mean()

        mse_loss.backward()

        optimizer.step()
        optimizer.zero_grad()

        # --- 畫圖與資訊呈現 (僅在訓練前期每 4 輪畫一次，最多到 300 輪) ---
        if epoch % 4 == 0 and epoch < 300:
            plt.clf()  # 清除上一次的畫布，避免圖像重疊

            # 繪製原始的 6 個數據點（散佈圖）
            x_data = data_points[:, 0]
            y_data = data_points[:, 1]
            plt.scatter(x_data, y_data)

            # 繪製當前模型預測的迴歸直線
            x_line = numpy.linspace(0, 1, 100)  # 在 x 軸從 0 到 1 之間均勻產生 100 個點

            # 由於 a 和 b 帶有梯度追蹤(requires_grad=True)，轉回 NumPy 畫圖前必須使用 .detach() 將其分離
            y_line = lr_model.a.detach().numpy() * x_line + lr_model.b.detach().numpy()

            plt.plot(x_line, y_line, color="red")  # 畫出紅色的迴歸線

            # 設定圖表標題，即時顯示目前的 epoch 數、a 值、b 值與 MSE 損失大小
            plt.title(f"epoch: {epoch}\n lr_model.a: {lr_model.a.item():.4f}, lr_model.b: {lr_model.b.item():.4f}\nMSE: {mse_loss.item():.4f}")
            plt.pause(0.1)  # 暫停 0.1 秒，製造出動態動畫的效果

    print(f"\n\n[epoch {epoch}], \nlr_model.a:{lr_model.a}, \nlr_model.b:{lr_model.b}")
# 訓練結束，印出最終（第 4000 輪）優化後的斜率 a 和截距 b
print(f"\n[epoch {epoch}], lr_model.a = {lr_model.a[0]:.4f}, b = {lr_model.b[0]:.4f}")