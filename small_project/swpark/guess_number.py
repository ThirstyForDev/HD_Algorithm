from random import *


random_value = randint(1, 5)

while True:
    print("1~5까지 임의의 정수를 추측해 보세요 : ")
    user_value = int(input())

    if user_value < random_value:
        print("정수가 너무 작아요")

    if user_value > random_value:
        print("정수가 너무 커요")

    if user_value == random_value:
        print("정답입니다 ! ")
        break
