def all_variants(text):
    for start in range(len(text)):
        for end in range(len(text) - start):
            yield text[end:end + start + 1]


a = all_variants("abc")
for i in a:
    print(i)
