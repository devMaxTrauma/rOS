import random


def simulate():
    seats = [0] * 100
    for i in range(100):
        seats[i] = 0
    for i in range(100):
        if i == 0:
            random_seat = random.randint(0, 99)
            seats[random_seat] = 1
        else:
            if seats[i] == 0:
                seats[i] = i
            else:
                random_seat = random.randint(0, 99)
                while seats[random_seat] != 0:
                    random_seat = random.randint(0, 99)
                seats[random_seat] = i

    if seats[99] == 99:
        return True
    else:
        return False


def main():
    count = 0
    simulating_target = 100000
    for i in range(simulating_target):
        print("simulating: ", i, "th time.")
        if simulate():
            count += 1

    print("Probability of the last passenger getting his seat: ", count/simulating_target)


main()
