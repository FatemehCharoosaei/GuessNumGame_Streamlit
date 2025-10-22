import random

def validate_input(input_num):
    if not input_num.isdigit():
        print('Invalid input. Please enter a number.')
        return False

    input_num = int(input_num)
    if input_num < 1 or input_num > 100:
        print('Invalid input. Please enter a number between 1 and 100.')
        return False

    return True

def start_game():
    rand_num = random.randint(1, 100)
    attemped = 0

    while True:
        input_num = input("Enter your guess between 1 and 100:")

        if input_num == 'q':
            print('Goodbye!')
            break

        if not validate_input(input_num):
            continue

        input_num = int(input_num)
        if input_num == rand_num:
            print(f'You guessed correctly! You attemed {attemped} times')
            wanna_play = input('Do you want to play again? (y/n)')
            if wanna_play == 'y':
                rand_num = random.randint(1, 100)
                attemped = 0
                continue
            else:
                print('Goodbye!')
                break

        elif input_num > rand_num:
            print('You guessed too high!')
        else:
            print('You guessed too low!')

        attemped += 1

if __name__ == '__main__':
    start_game()