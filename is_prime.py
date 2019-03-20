import math

from expr import *

is_prime = lambda n: func(
    lambda has_divisors: \
        False if n <= 1 else \
        True  if n <= 3 else \
        False if n % 2 == 0 else \
        not has_divisors,
    where(
        has_divisors=any([n % m == 0 for m in range(3, math.floor(n / 2) + 1)])
    )
)

consume(
    print(f"{i}: {is_prime(i)}") for i in range(30)
)
