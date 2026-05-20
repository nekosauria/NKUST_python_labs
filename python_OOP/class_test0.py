
# 定義一個 class 並給予 default 值
class Car():
    # 這是類別屬性 (Class Attributes)
    brand = 'unknown'
    engine = 'oil_type'
    total_count = 0

    # 建構子 , 物件的誕生裡 （ object 封裝到記憶體 ）
    # 若沒寫這個建構子 , 實際上還是會有隱式的建構子
    def __init__(self, brand=None, engine=None):
        print('constructor')
        # 如果有傳入參數就用參數，沒有就用類別預設值
        self.brand = brand if brand else Car.brand
        self.engine = engine if engine else Car.engine
        # 類別變數
        Car.total_count += 1







if __name__ == "__main__":
    car = Car()
    print(car.brand)
    print(car.engine)
    print(car.total_count)

    honda_car = Car(brand='honda', engine='v4')
    print(honda_car.brand)
    print(honda_car.engine)
    print(car.total_count)
