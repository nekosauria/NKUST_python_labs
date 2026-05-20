import torch

# 1. 建立一個「數位算盤」數據 (Tensor)
# 假設這是一個輸入值 2.0，我們希望追蹤它的修正過程
x = torch.tensor([2.0], requires_grad=True)

# 2. 定義一個簡單的公式: y = x^2 (假設這是我們的 AI 模型)
y = x ** 2

# 3. 啟動「自動修正」功能
y.backward()

# 4. 看看如果 x 變動一點點，對 y 的影響力是多少 (導數)
print(x.grad) # 輸出會是 4.0 (因為 y=x^2 的導函數是 2x，2*2=4)