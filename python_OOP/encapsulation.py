# 封裝 , e.g 不想讓別人知道程式碼在幹麻
# 不想讓人知道類別怎解決 , e.g. python lib package
# python 預設都是 public 的 , 跟其他程式語言設計不太一樣
import unittest


class test_encapsulation(unittest.TestCase):


    def __init__(self):
        print('my_fun')

# public
    def my_public_fun(self):
        print('my_public_fun')

# private
    def __my_private_fun(self):
        print('__my_private_fun')

# protected
# e.g. 子類別可以呼叫
    def _my_protected_fun(self):
        print('_my_protected_fun')


# if __name__ == "__main__":
# 這在 Python 中有一個很專業（也很酷）的名字，叫做 Magic Methods（魔術方法），或者因為前後都有雙底線，大家常簡稱為 Dunder Methods (Double UNDERscore)。
# 如果你看到像 __init__、__call__ 或者你舉例的 __myfun__ 這種寫法，它們代表的是 「Python 系統內建的特殊掛鉤 (Hooks)」。
# Python object model 的接口（protocol）