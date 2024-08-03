first_strings = ['Elon', 'Musk', 'Programmer', 'Monitors', 'Variable']
second_strings = ['Task', 'Git', 'Comprehension', 'Java', 'Computer', 'Assembler']

first_result = [len(x) for x in first_strings if len(x) >= 5]

second_result = [(x, y) for x in first_strings for y in second_strings if len(x) == len(y)]

res = first_strings + second_strings
third_result = {x and y: len(x) and len(y) for x in res for y in res if len(x) % 2 == 0 and len(y) % 2 == 0}


print(first_result)
print(second_result)
print(third_result)

