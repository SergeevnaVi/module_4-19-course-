def is_prime(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        if res == 2:
            print('Простое')
        if res <= 1:
            print('Составное')
        for n in range(2, res):
            if res % n == 0:
                print('Составное')
                break
        else:
            print('Простое')
        return res
    return wrapper


@is_prime
def sum_three(a, b, c):
    return a + b + c


result = sum_three(2, 3, 6)
print(result)
result2 = sum_three(5, 5, 5)
print(result2)
result3 = sum_three(5, 3, 9)
print(result3)
