from pprint import pprint
import random


class NeuralNetwork:
    LEARNING_RATE = 0.1
    MAX_EPOCH_NUMBER = 100

    def __init__(
        self,
        number_of_inputs,
        number_of_hidden,
        number_of_outputs,
        input_layer_weights,
        hidden_layer_weights,
    ):
        self.input_layer = NeuronLayer(number_of_inputs)
        self.hidden_layer = NeuronLayer(number_of_hidden)
        self.output_layer = NeuronLayer(number_of_outputs)

        self.init_weights_from_inputs_to_hidden(input_layer_weights)
        self.init_weights_from_hidden_to_outputs(hidden_layer_weights)

    def init_weights_from_inputs_to_hidden(self, weights):
        index = 0
        for i in range(len(self.input_layer.neurons)):
            for h in range(len(self.hidden_layer.neurons)):
                self.input_layer.neurons[i].weights.append(weights[index])
                index += 1

    def init_weights_from_hidden_to_outputs(self, weights):
        index = 0
        for h in range(len(self.hidden_layer.neurons)):
            for o in range(len(self.output_layer.neurons)):
                self.hidden_layer.neurons[h].weights.append(weights[index])
                index += 1


class NeuronLayer:
    def __init__(self, number_of_neurons):
        self.neurons = [Neuron() for i in range(0, number_of_neurons)]


class Neuron:
    def __init__(self):
        self.weights = []


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

    pprint(test_data)
    pprint(training_data)

    neural_network = NeuralNetwork(
        4, 4, 3, [0 for i in range(0, 16)], [0 for i in range(0, 16)]
    )
