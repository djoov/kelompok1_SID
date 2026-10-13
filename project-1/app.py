def biaya(amount):
    if type(amount) is not int or amount < 0:
        raise ValueError("amount harus integer nonnegatif")
    return min(amount // 100, 5000)


if __name__ == "__main__":
    print(biaya(100000))
