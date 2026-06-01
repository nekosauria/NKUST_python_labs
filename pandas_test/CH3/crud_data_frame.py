import pandas as pd
import random
from utils.pypath import load_PP


# 注意 update delete 都不會影響到真實資料
data_path = load_PP("pandas_test/products.csv")
df = pd.read_csv(data_path, encoding="utf8")
df.columns = ["id", "type", "name", "price"]
ordinals = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
df.index = ordinals

print(df.info())

# update data (不改真實 data)
# s = ["z", "居家", "家樂福", 30.4]
# df.loc[ordinals[1]] = s
# print(df.head(3))
# df.loc[:, "price"] = [23.4, 56.7, 12.1, 90.5, 11.2, 34.1,12.5, 90.5, 11.2, 34.1, 12.5]
# print(df.head())

# 我們也可以使用布林索引找出欲更新資料後，一
# 次就更新整個 DataFrame 物件 ， 首先建立
# DataFrame物件df，如下所示：
# df3 = pd.DataFrame([random.sample(range(0,1000), 3),
# random.sample(range(0,1000), 3)])
# print(df3)
# print("\n")
# 然後 ， 我們準備使用布林索引條件來過 濾
# DataFrame物件，並且更新這些符合條件的記錄資
# 料，即都減100：
# print(df3[df3> 500])
# print("\n")
# df3[df3 > 500] = df3 - 100
# print(df3)

# delete data
# 如同更新純量值，刪除資料只是指定成None，
# 如下所示：
# df.loc[ordinals[0], "price"] = None
# df.iloc[1,2] = None
# print(df.head(3))

# DataFrame物件是使用drop()函數刪除記錄，參數
# 可以是索引標籤或位置，如下所示：
# df = df.drop(["B", "D"]) # 2,4 筆
# print(df.head())
# df.drop(df.index[[2,3]], inplace=True) # 3,4 筆
# print(df.head())

# 刪除欄位也是使用drop()函數，只是我需要指定
# axis參數值是1（預設值0是記錄；1是欄位），如下
# 所示
# df = df.drop(["price"], axis=1)
# print(df.head(3))

# 在DataFrame物件新增記錄（列）只需指定一個
# 不存在的索引標籤，就可以新增記錄，我們也可
# 以建立Series物件，然後使用append()函數來新
# 增記錄，如下所示：
# df.loc["X"] = ["X","科學", "全聯超", 28.5]
# print(df.tail(3))
# s = pd.Series({"id":"Y","type":"科學","name":"大潤發","price":79.2})
# df2 =  pd.concat([df, s.to_frame().T], ignore_index=True)
# print(df2.tail(3))

# add column
# df["sales"] = df["sales"] = [124.5,227.5,156.7,435.6,333.7,259.8, 0,0,0,0,0]
# print(df.head())
# df.loc[:,"city"] = ["台北","新竹","台北","台中","新北","高雄",0,0,0,0,0]
# print(df.tail())


# 於現存DataFrame物件，我們可以建立形狀相
# 同，但沒有資料的空DataFrame物件，也可以使
# 用copy()函數在處理前備份DataFrame物件，如
# 下所示：
# col = ["id","type", "name", "price"]
# df_empty = pd.DataFrame(None, index=ordinals,
# columns=col)
# print(df_empty)
# # • copy()函數可以複製DataFrame物件，如下所示：
# df_copy = df.copy()
# print(df_copy)

# Pandas 套件可以使用 describe() 函數顯示
# DataFrame物件指定欄位，或Series物件的資料
# 描述，如下所示：
# print(df["price"].describe())
# ================================

# DataFrame 統計函數（Pandas）
# ================================

# count()      : 非 NaN 值計數（統計有效資料筆數）
# mode()       : 眾數（出現次數最多的值）
# median()     : 中位數（排序後的中間值）
# quantile()   : 分位數（percentile）
#                q=0.25 -> 第一四分位數 (Q1)
#                q=0.50 -> 第二四分位數 (Median)
#                q=0.75 -> 第三四分位數 (Q3)

# mean()       : 平均數
# max()        : 最大值
# min()        : 最小值
# sum()        : 總和

# var()        : 變異數（資料離散程度）
# std()        : 標準差（變異數開根號）

# cov()        : 共變異數（兩個變數一起變動的關係）
# corr()       : 相關係數（-1 ~ 1，線性關係強度）

# cumsum()     : 累積總和（running total）
# cumprod()    : 累積乘積（running product）