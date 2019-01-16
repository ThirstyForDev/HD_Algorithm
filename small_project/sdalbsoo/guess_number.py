import random
import sys

def generate_number():
    return random.randint(1, 100)


def guess_number_game():
    random_number = generate_number()
    print("정답은 1에서 100사이의 숫자입니다.")
    while(1):
        num = int(input("숫자 입력: "))
        if random_number > num:
            print("입력 값이 정답보다 작습니다.")
            pass
        elif random_number < num:
            print("입력 값이 정답보다 큽니다.")
            pass
        else:
            print(num, "이 정답입니다! 축하합니다!")
            sys.exit()


def main():
    guess_number_game()


if __name__ == '__main__':
    main()
