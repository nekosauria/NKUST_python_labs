import torch
from torch.utils.data import SubsetRandomSampler, DataLoader
import plt
from digital_images.CH13.HOGDataset import LeNetImpl
import digital_images.HOGs_SVM.MNIST as mnist
from utils.pypath import load_PP
import os

# 確保程式的工作目錄切換到資料檔案所在的資料夾
os.chdir(load_PP("digital_images/HOGs_SVM/"))

# set hyper_parameter
n_epoch = 50
batch_size = 20
eta = 0.01

# init train data & answer
# 直接取純圖像不經過 DatasetImpl
minist_train = mnist.MNIST("train-images.idx3-ubyte", "train-labels.idx1-ubyte")

# create a pytorch loader
index_list = list(range(len(minist_train)))
sampler = SubsetRandomSampler(index_list)
loader = DataLoader(dataset=minist_train, sampler=sampler, batch_size=batch_size)

# add LeNetImpl model
le_model = LeNetImpl()

# add optimizer
# Stochastic Gradient Descent, 隨機梯度下降（或隨機梯度優化器）
# lr = learning rate
optimizer = torch.optim.SGD(le_model.parameters(), lr=eta)

# add loss function
# CrossEntropyLoss = Softmax 函數 + Cross Entropy (交叉熵) 計算
criterion = torch.nn.CrossEntropyLoss()

# 自動選擇最佳裝置（跨平台友好）
if torch.cuda.is_available():
    device = torch.device("cuda")          # NVIDIA GPU
elif torch.backends.mps.is_available():
    device = torch.device("mps")           # Apple Silicon Mac
else:
    device = torch.device("cpu")

print(f"使用裝置: {device}")


# 正確搬移模型到裝置
le_model = le_model.to(device)


if __name__ == '__main__':
    loss_list = []

    # 開始跑訓練
    for epoch in range(n_epoch):
        total_loss = 0
        n_batch = 0

        for images, target_labels in loader:
            # put data to gpu
            images = images.to(device)

            # 預測結果 (裡面會自己去 call 自己實作好的 forward function )
            predictions = le_model(images)

            # 真實結果
            target_labels = target_labels.to(device)

            # 計算 loss function 誤差
            loss = criterion(predictions, target_labels)

            # 計算 tatal loss
            total_loss += loss.item()
            n_batch += 1

            # backward propagation
            # 算梯度
            loss.backward()

            # 用梯度更新模型權重
            optimizer.step()
            # 初始化、清空、準備開始 optimizer (close)
            optimizer.zero_grad()

        # compute the average loss
        average_loss = total_loss / n_batch
        loss_list.append(average_loss)
        print(f"▶ Epoch [{epoch+1:02d}/{n_epoch}] - Loss: {average_loss:.4f}")


    # 下載成 model, .pth
    torch.save(le_model.state_dict(), "le.pth")

    print(f"成功將模型儲存至：{os.path.join(os.getcwd(), 'le.pth')}")
    print(f"{loss_list}")

    plt.plot(range(len(loss_list)), loss_list)
    plt.show()
