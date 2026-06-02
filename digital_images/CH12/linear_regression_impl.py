import numpy
import matplotlib.pyplot as plt

# =========================
# Step 1: 隨機初始化模型參數 （隨機測試起始值）
# =========================
# 線性回歸模型: y = a * x + b
#  numpy.random.randn(1) = 平均值 = 0、標準差 = 1 的「標準常態分布」隨機數
a = numpy.random.randn(1)  # weight（斜率）
b = numpy.random.randn(1)  # bias（截距）
print(f"a = {a}, b = {b}")


# =========================
# Step 2: 準備訓練資料
# =========================
# 每一列 = [x, y]
# 目標是學出 y ≈ a*x + b
# x = input feature
# y = label
# a,b = parameters learned by gradient descent

data_points = numpy.array([
    [0.11, 1.24],
    [0.20, 1.40],
    [0.49, 2.00],
    [0.65, 2.27],
    [0.67, 2.41],
    [0.83, 2.52]
])


# =========================
# Step 3: 設定超參數（hyperparameters）
# =========================
n_epoch = 4000        # 訓練輪數（完整掃過資料集的次數）
batch_size = 2        # mini-batch 大小
eta = 0.01            # learning rate（學習率）


# =========================
# Step 4: Training Loop（核心）
# =========================

# print 斜率 a 和截距 b
print(f"[epoch 0], a = {a[0]:.4f}, b = {b[0]:.4f}")

for epoch in range(n_epoch):

    # 每個 epoch 都會打亂資料（提升泛化能力）
    numpy.random.shuffle(data_points)

    # =========================
    # Step 5: Mini-batch iteration
    # =========================
    # 每次取 batch_size 筆資料做一次更新
    for start_index in range(0, len(data_points), batch_size):

        # 取出 mini-batch
        points = data_points[start_index:start_index+batch_size]

        # 拆出 x / y
        x = points[:, 0]
        y = points[:, 1]

        # =========================
        # Step 6: Forward pass（預測）
        # =========================
        # 線性模型：y_hat = ax + b
        y_hat = a * x + b

        # =========================
        # Step 7: Loss 計算（MSE）
        # =========================
        # Mean Squared Error
        y_error = y - y_hat
        mse_loss = (y_error ** 2).mean()

        # =========================
        # Step 8: Gradient 計算（手動微分）
        # =========================
        # 對 a 的梯度（斜率）
        a_grad = -2 * (x * y_error).mean()

        # 對 b 的梯度（截距）
        b_grad = -2 * (y_error.mean())

        # =========================
        # Step 9: Parameter update（梯度下降）
        # =========================
        a = a - eta * a_grad
        b = b - eta * b_grad

        # print img and info
        if epoch % 4 == 0 and epoch <300:
            plt.clf()

            x = data_points[:, 0]
            y = data_points[:, 1]

            plt.scatter(x, y)

            x_line = numpy.linspace(0, 1, 100)
            y_line = a * x_line + b

            plt.plot(x_line, y_line, color="red")

            # print 斜率 a 和截距 b
            plt.title(f"epoch: {epoch}\n a: {a}, b: {b}\nMSE: {mse_loss}")
            plt.pause(0.1)

print(f"[epoch {epoch}], a = {a[0]:.4f}, b = {b[0]:.4f}")