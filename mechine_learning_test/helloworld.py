from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 1. 載入數據 (包含 150 筆資料，4 個特徵，3 個品種)
iris = load_iris()
X = iris.data  # 特徵：花萼長度、寬度，花瓣長度、寬度
y = iris.target # 標籤：0 (Setosa), 1 (Versicolour), 2 (Virginica)

# 2. 切分數據：80% 用來訓練模型，20% 留著考試 (測試)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3.1. 建立模型：使用邏輯斯迴歸 (Logistic Regression)
# 雖然它叫迴歸，但它是用來分類 3 個品種的機率
#model = LogisticRegression(max_iter=200)
# 3.2. 建立隨機森林模型
# 隨機森林是一種「集成學習（Ensemble Learning）」，它會同時建立很多棵決策樹，並透過投票機制決定最終結果。
model = RandomForestClassifier(n_estimators=100, random_state=42)

# 4. 訓練模型 (這就是權重矩陣 W 不斷微調的過程)
model.fit(X_train, y_train)

# 5. 進行預測
y_pred = model.predict(X_test)

# 6. 印出準確度
print(f"模型準確度: {accuracy_score(y_test, y_pred) * 100:.2f}%")

# 7. 隨機測試：丟入一組全新的數據 [花萼長, 花萼寬, 花瓣長, 花瓣寬]
sample = [[5.1, 3.5, 1.4, 0.2]]
prediction = model.predict(sample)
print(f"預測品種: {iris.target_names[prediction][0]}")

