import math


def sigmoid(x):
    return 1 / (1 + pow(math.e, x * (-1)))


def sigmoid_derivative(x):
    sigmoid_value = sigmoid(x)
    return sigmoid_value * (1 - sigmoid_value)


def error(target, output):
    return sum([0.5 * pow((target[i] - output[i]), 2) for i in range(0, len(target))])
