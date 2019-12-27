from expr import *

# do
assert do([]) == False, "do with empty array returns False"
assert do([1]) == 1, "do with single value returns the value"
assert do([1, 2, 3]) == 3, "do with multiple values returns the last value"
assert do([
    x := 1,
    y := 2,
    x + y
]) == 3, "do with assignment expressions OK"

# loop_while
loops = Box(0)
loop_while(lambda: do([
    loops.set(lambda n: n + 1),
    loops.get() < 5
])) 
assert loops.get() == 5, "loop_while calls the callback until the value is False"

# for_each
loops.set(lambda _: 0)
for_each(range(5), lambda _:)

print("all tests passed")
