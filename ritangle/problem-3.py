import random

num_trials = 0
num_success = 0
max_num_trials = 2000000

while num_trials < max_num_trials:
    num_trials += 1
    all_dice = [random.randint(1,6) for i in range(0,5)]

    if 2 in all_dice and 5 in all_dice:
        num_success += 1
        continue

    elif 5 in all_dice and 0 in all_dice:
        num_success += 1
        continue

    try:
        zero_index = all_dice.index(0)
    except:
        continue

    try:
        zero_index = all_dice.index(0, zero_index)
    except:
        continue
    num_success += 1

print(num_success / num_trials)


# 0.2319
