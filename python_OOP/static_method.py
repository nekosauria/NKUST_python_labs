class Math:
    # 一打開就佔記憶體,但是比較快
    @staticmethod
    def add(a, b):
        return a + b


if __name__ == '__main__':
    print(Math.add(1, 2))



