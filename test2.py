

if __name__ == "__main__":
    a = 5
    b = a
    a = 7
    print(f"{a=} {b=}")

    li = [8, 9, 10]
    c = li[0]
    print(f"{li=} {c=}")
    li[0] = "gugus"
    print(f"{li = } {c = }")
    c = 99999
    print(f"{li=} {c=}")

    list1 = [5, 8, 32, 4930]
    ref = list1
    print(f"{list1=} {ref=}")
    ref[2] = 2
    print(f"{list1=} {ref=}")



