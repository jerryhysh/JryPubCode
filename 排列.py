import itertools
import time
'''
从n个不同的元素中取出m(m<=n)个元素，并按照一定的顺序排成一列，
叫做从n个元素中取出m个元素的一个排列
特别地，当m=n时，这个排列被称作全排列
'''

if __name__ == "__main__":
    # 排列
    mylist1 = list(itertools.permutations([1,2,3,4],3))
    print(mylist1)
    print(len(mylist1))
    # 组合
    mylist2 = list(itertools.combinations([1,2,3,4],3))
    print(mylist2)
    print(len(mylist2))
    # 排列组合
    mylist3 = list(itertools.product("123456",repeat=3))
    print(mylist3)
    print(len(mylist3))

    # 迭代器
    passwd = ("".join(x) for x in itertools.product("123456",repeat=3))
    while True:
        try:
            time.sleep(0.5)
            str = next(passwd)
            print(str)
        except StopIteration as e:
            break