from random import uniform

def v(u, t, th):
    result = 1 - ((1 - u) ** th * (t ** (th / (1 - th)) - 1) + 1) ** (1 / th)
    return result

for i in range(500):
    th = 2.0
    u, t = uniform(0, 1), uniform(0, 1)
    print u, v(u, t, th)
