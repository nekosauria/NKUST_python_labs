import torch
from digital_images.CH13.HOGDataset import LeNetImpl
import os
from utils.pypath import load_PP
import digital_images.HOGs_SVM.MNIST as mnist

# 自動選擇最佳裝置（跨平台友好）
if torch.cuda.is_available():
    device = torch.device("cuda")          # NVIDIA GPU
elif torch.backends.mps.is_available():
    device = torch.device("mps")           # Apple Silicon Mac
else:
    device = torch.device("cpu")

print(f"使用裝置: {device}")

# add test data
os.chdir(load_PP("digital_images/HOGs_SVM/"))
mnist_test = mnist.MNIST("t10k-images.idx3-ubyte", "t10k-labels.idx1-ubyte")

# add accuracy tmp
n_test = len(mnist_test)
n_correct = 0
n_wrong = 0

# add model with gpu
le_model = LeNetImpl().to(device)

# 請確保這個路徑與你實際存檔的檔名、位置一致
model_path = load_PP("digital_images/HOGs_SVM/le.pth")
print(f"模型權重 path：{model_path}")

state_dict = torch.load(model_path, map_location=device, weights_only=True)
le_model.load_state_dict(state_dict)

# get test
for idx in range(n_test):
    # get item
    image, target_label = mnist_test[idx]

    images = torch.unsqueeze(image, dim=0).to(device)

    pred_label = le_model(images).to(device)
    pred_label = torch.squeeze(pred_label)
    pred_label = torch.argmax(pred_label)

    if target_label == pred_label:
        n_correct = n_correct + 1
    else:
        n_wrong = n_wrong + 1

accuracy = n_correct / n_test

# 輸出範例：正確數: 9904, 總數: 10000, 準確率: 99.04%
print(f"正確數: {n_correct}, 總數: {n_test}, 準確率: {accuracy:.2%}")
