def letter_to_number(letter):
    return ord(letter.upper()) - 64

def min_distance(letter_a, letter_b):
    a = letter_to_number(letter_a)
    b = letter_to_number(letter_b)
    diff_a_b = abs(a-b)
    # if difference without crossing Z-A is less than with crossing Z-A
    if diff_a_b <= 13:
        return diff_a_b
    return 26 - diff_a_b

# Brute Force:
word = "RITANGLE"
current_word = []
min_val = 999999999999999
min_word = None
max_val = 0
max_word = None
for letter_1 in word:
    current_word.append(letter_1)
    for letter_2 in word:
        if letter_2 not in current_word:
            current_word.append(letter_2)
            for letter_3 in word:
                if letter_3 not in current_word:
                    current_word.append(letter_3)
                    for letter_4 in word:
                        if letter_4 not in current_word:
                            current_word.append(letter_4)
                            for letter_5 in word:
                                if letter_5 not in current_word:
                                    current_word.append(letter_5)
                                    for letter_6 in word:
                                        if letter_6 not in current_word:
                                            current_word.append(letter_6)
                                            for letter_7 in word:
                                                if letter_7 not in current_word:
                                                    current_word.append(letter_7)
                                                    for letter_8 in word:
                                                        if letter_8 not in current_word:
                                                            current_word.append(letter_8)
                                                            path_length = 0
                                                            for i in range(7):
                                                                path_length += min_distance(current_word[i], current_word[i+1])
                                                            if path_length < min_val:
                                                                min_val = path_length 
                                                                min_word = "".join(current_word)
                                                            if path_length > max_val:
                                                                max_val = path_length
                                                                max_word = "".join(current_word)
                                                            current_word.pop()
                                                    current_word.pop()
                                            current_word.pop()
                                    current_word.pop()
                            current_word.pop()
                    current_word.pop()
            current_word.pop()
    current_word.pop()

print(f"Min: {min_val}, Min Word: {min_word}")
print(f"Max: {max_val}, Max Word: {max_word}")

# clue 851
