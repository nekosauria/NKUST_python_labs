import numpy
import matplotlib.pyplot as plt

# 使用前 data 要先包成 pytorch tensor 格式
import torch
# autograd package ( pytorch 自動算偏微分工具 ) 「自動算梯度」
# torch.optim, 參數更新器（optimizer）模組 「自動調整模型參數」


# 隨機測試起始值
# requires_grad=True 表示告訴 PyTorch 這個變數需要計算梯度（即算偏微分），之後才能拿來更新
a = torch.randn(1, requires_grad=True)  # weight（斜率 w）
b = torch.randn(1, requires_grad=True)  # bias（截距 b）
print(f"a = {a}, b = {b}")

# 樣本資料（答案）：由 6 個 (x, y) 座標組成的 NumPy 陣列
data_points = numpy.array([
    [0.11, 1.24],
    [0.20, 1.40],
    [0.49, 2.00],
    [0.65, 2.27],
    [0.67, 2.41],
    [0.83, 2.52]
])

# 設定超參數 (Hyperparameters)
n_epoch = 4000  # 訓練輪數（完整掃過整個資料集的次數）
batch_size = 2  # Mini-batch 大小（每次挑選多少筆資料來計算梯度並更新參數）
eta = 0.01  # Learning rate（學習率），控制每次參數更新的步長

# 準備自動調參工具（優化器）
# 使用隨機梯度下降法 (SGD)，傳入要優化的參數 [a, b] 與學習率 eta
optimizer = torch.optim.SGD([a, b], eta)

# 印出初始（第 0 輪）的斜率 a 和截距 b
print(f"[epoch 0], a = {a[0]:.4f}, b = {b[0]:.4f}")

# 開始跑線性回歸訓練
for epoch in range(n_epoch):

    # 每一輪開始前，將資料點隨機洗牌 (Shuffle)，確保每次 Mini-batch 拿到的資料組合不同，有助於跳出局部最佳解
    numpy.random.shuffle(data_points)

    # 根據 batch_size 區隔資料，分批進行訓練 (Mini-batch SGD)
    for start_index in range(0, len(data_points), batch_size):
        # 取出當前批次的資料點 (例如：每次取 2 筆)
        points = data_points[start_index:start_index + batch_size]

        # 將 NumPy 格式的資料轉換為 PyTorch 的 FloatTensor，以便進行張量運算
        x = torch.FloatTensor(points[:, 0])  # 預測變數 x
        y = torch.FloatTensor(points[:, 1])  # 真實標籤 y

        # --- 1. 前向傳播 (Forward Pass) ---
        y_hat = a * x + b  # 預測值公式：y = wx + b
        y_error = y - y_hat  # 計算誤差（殘差）

        m_loss = (y_error ** 2).mean()  # 計算均方誤差 (Mean Squared Error, MSE)
        # m_loss = torch.abs(y_error).mean()  # 改成計算平均絕對誤差 (Mean Absolute Error, MAE)

        # --- 2. 反向傳播 (Backward Pass) ---
        # 透過 PyTorch 的 Autograd 機制，自動計算 Loss 對參數 a 和 b 的偏微分（梯度）
        m_loss.backward()

        # --- 3. 參數更新 (Optimization Step) ---
        optimizer.step()  # 根據剛剛算出來的梯度，自動依照 SGD 公式更新 a 和 b 的值
        optimizer.zero_grad()  # 關鍵！清除舊的梯度。因為 PyTorch 預設會累積梯度，不清除的話下一批次計算會出錯

        # --- 4. 畫圖與資訊呈現 (僅在訓練前期每 4 輪畫一次，最多到 300 輪) ---
        if epoch % 4 == 0 and epoch < 300:
            plt.clf()  # 清除上一次的畫布，避免圖像重疊

            # 繪製原始的 6 個數據點（散佈圖）
            x_data = data_points[:, 0]
            y_data = data_points[:, 1]
            plt.scatter(x_data, y_data)

            # 繪製當前模型預測的迴歸直線
            x_line = numpy.linspace(0, 1, 100)  # 在 x 軸從 0 到 1 之間均勻產生 100 個點

            # 由於 a 和 b 帶有梯度追蹤(requires_grad=True)，轉回 NumPy 畫圖前必須使用 .detach() 將其分離
            y_line = a.detach().numpy() * x_line + b.detach().numpy()

            plt.plot(x_line, y_line, color="red")  # 畫出紅色的迴歸線

            # 設定圖表標題，即時顯示目前的 epoch 數、a 值、b 值與 MSE 損失大小
            plt.title(f"epoch: {epoch}\n a: {a.item():.4f}, b: {b.item():.4f}\nMSE: {m_loss.item():.4f}")
            plt.pause(0.1)  # 暫停 0.1 秒，製造出動態動畫的效果

# 訓練結束，印出最終（第 4000 輪）優化後的斜率 a 和截距 b
print(f"[epoch {epoch}], a = {a[0]:.4f}, b = {b[0]:.4f}")