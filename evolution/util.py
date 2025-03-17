import random
MU, SIGMA, MIN, MAX = 0, 1, -3, 3
SIGMA_D = 0.2

# here I aim at generating data from normal distribution but normalize it for further use
# I could have just used uniform but this does not really represent real circumstances
def generate_normalized_value():
    raw_value = random.normalvariate(MU, SIGMA)
    while raw_value < MIN or raw_value > MAX:
        raw_value = random.normalvariate(MU, SIGMA)
    normalized_value = (raw_value - MIN) / (MAX - MIN)
    return normalized_value

def generate_random_delta():
    return random.normalvariate(MU, SIGMA_D)