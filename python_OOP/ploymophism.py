# 抽象類型 e.g. 抽象介面
# abstractmethod
# abstractmethod 的目的是「強迫子類別實作某些功能」

# ** 繼承就像是 資料庫內可以直接呼叫的數據類型 e.g. str , datatime
# ** 抽象比較像是 資料庫每個欄位規定的 column type


# from abc import ABC , abstractmethod 為寫法
from abc import ABC , abstractmethod


# -----------------------------------
# 定義抽象類
class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass


# 實作（implement）抽象方法
class Dog(Animal):
    def make_sound(self):
        return 'woof'

class Cat(Animal):
    def make_sound(self):
        return 'mow'

# 執行上述結果 , 測試多行
if __name__ == '__main__':
    def animal_sound(animal):
        print(animal.make_sound())

    dog = Dog()
    animal_sound(dog)
    cat = Cat()
    animal_sound(cat)