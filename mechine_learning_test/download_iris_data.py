import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# 1. 載入資料並整理為完整的 DataFrame
iris = load_iris()
df_features = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df_target = pd.DataFrame(data=iris.target, columns=['target'])

# 將特徵與標籤合併
df = pd.concat([df_features, df_target], axis=1)

# (選用) 如果你想存成一個總檔案，可以用這行
# df.to_csv('iris_full.csv', index=False)

# 2. 定義特徵 (X) 與 標籤 (y)
X = df.drop('target', axis=1)
y = df['target']

# 3. 切分資料 (訓練集 80% / 測試集 20%)
# random_state 是隨機種子，設定後每次執行切分結果都會一樣
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"原始資料筆數: {len(df)}")
print(f"訓練集筆數: {len(X_train)}")
print(f"測試集筆數: {len(X_test)}")

# 驗證前幾筆訓練集資料
print("\n--- 訓練集前 5 筆 ---")
print(X_train.head())