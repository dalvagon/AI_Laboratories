import math
import random


class NeuralNetwork:
    LEARNING_RATE = 0.1
    MAX_EPOCH_NUMBER = 100
    y_hidden_layer = []  # the output of the neurons from the hidden layer
    y_output_layer = []  # the output of the neurons from the output layer

    def __init__(
            self,
            number_of_inputs,
            number_of_hidden,
            number_of_outputs,
            input_layer_weights,
            hidden_layer_weights,
            inputs
    ):
        self.input_layer = NeuronLayer(number_of_inputs)
        self.hidden_layer = NeuronLayer(number_of_hidden)
        self.output_layer = NeuronLayer(number_of_outputs)

        self.inputs = inputs

        self.init_weights_from_inputs_to_hidden(input_layer_weights)
        self.init_weights_from_hidden_to_outputs(hidden_layer_weights)

    def init_weights_from_inputs_to_hidden(self, weights):
        for i in range(len(self.input_layer.neurons)):
            for h in range(len(self.hidden_layer.neurons)):
                self.input_layer.neurons[h].weights.append(weights[i])

    def init_weights_from_hidden_to_outputs(self, weights):
        for h in range(len(self.hidden_layer.neurons)):
            for o in range(len(self.output_layer.neurons)):
                self.hidden_layer.neurons[o].weights.append(weights[h])

    def forward_propagation(self):
        for index in range(len(self.inputs)):
            x_inputs = self.inputs[index][0]
            # calculate output from the neurons from the hidden layer
            summa_hidden = 0
            index_neuron = 0
            while index_neuron < len(self.input_layer.neurons):
                for index_input in range(len(self.input_layer.neurons)):
                    summa_hidden += x_inputs[index_input] * self.input_layer.neurons[index_neuron].weights[index_input]
                self.y_hidden_layer.append(sigmoid(summa_hidden))
                index_neuron += 1

            # calculate output from the neurons from the output layer
            summa_output = 0
            index_neuron = 0
            print(self.y_hidden_layer)
            while index_neuron < len(self.output_layer.neurons):
                for index_hidden in range(len(self.hidden_layer.neurons)):
                    pos = (-1) * len(self.hidden_layer.neurons)
                    summa_output += self.y_hidden_layer[pos + index_hidden] * \
                                    self.hidden_layer.neurons[index_neuron].weights[index_hidden]
                self.y_output_layer.append(sigmoid(summa_output))
                index_neuron += 1


class NeuronLayer:
    def __init__(self, number_of_neurons):
        self.neurons = [Neuron() for i in range(0, number_of_neurons)]


class Neuron:
    def __init__(self):
        self.weights = []


def sigmoid(x):
    return 1 / (1 + pow(math.e, x * (-1)))


def derivative_sigmoid(x):
    der_sigmoid = sigmoid(x)
    return der_sigmoid(1 - der_sigmoid)


def error(target, output):
    err = 0
    for i in range(len(target)):
        err += 0.5 * pow((target[i] - output[i]), 2)
    return err


def read_data(input_file):
    lines = input_file.readlines()
    data = [
        (
            [float(value) for value in line.strip().split(",")[:-1:]],
            line.strip().split(",")[-1],
        )
        for line in lines
    ]

    return data


if __name__ == "__main__":
    input_file = open("./iris.data", "r")
    data = read_data(input_file)
    random.shuffle(data)
    test_data = data[0:15]
    training_data = data[15:]

    # pprint(test_data)
    # pprint(training_data)

    neural_network = NeuralNetwork(
        4, 4, 3, [round(random.uniform(-0.1, 0.1), 2) for i in range(0, 16)],
        [round(random.uniform(-0.1, 0.1), 2) for i in
         range(0, 16)], training_data
    )
    neural_network.forward_propagation()
    print(neural_network.y_hidden_layer)
    print(neural_network.y_output_layer)
