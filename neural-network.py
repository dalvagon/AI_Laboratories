from utils import error, sigmoid, sigmoid_derivative
import random
from pprint import pprint


class NeuralNetwork:
    LEARNING_RATE = 0.5

    def __init__(
        self,
        number_of_input,
        number_of_hidden,
        number_of_output,
        hidden_layer_weights,
        hidden_layer_bias,
        ouput_layer_weights,
        output_layer_bias,
    ):
        self.number_of_input = number_of_input
        self.number_of_hidden = number_of_hidden
        self.number_of_output = number_of_output

        self.hidden_layer = NeuronLayer(number_of_hidden, hidden_layer_bias)
        self.output_layer = NeuronLayer(number_of_output, output_layer_bias)

        self.init_weights_from_input_to_hidden(hidden_layer_weights)
        self.init_weights_from_hidden_to_output(ouput_layer_weights)

    def init_weights_from_input_to_hidden(self, weights):
        index = 0
        for h in range(len(self.hidden_layer.neurons)):
            for i in range(self.number_of_input):
                self.hidden_layer.neurons[h].weights.append(weights[index])
                index += 1

    def init_weights_from_hidden_to_output(self, weights):
        index = 0
        for o in range(len(self.output_layer.neurons)):
            for h in range(len(self.hidden_layer.neurons)):
                self.output_layer.neurons[o].weights.append(weights[index])
                index += 1

    def train(self, inputs, target):
        for input in inputs:
            output = self.propagate_forward(input)
            self.propagate_backward(input, output, target)

    def propagate_forward(self, input):
        hidden_layer_output = self.hidden_layer.get_output(input)

        return self.output_layer.get_output(hidden_layer_output)

    def propagate_backward(self, input, output, target):
        ##################### Output layer #########################
        # The partial derivative of the Error with respect to output
        pd_errors_wrt_output = [-(target[o] - output[o]) for o in range(0, len(output))]

        # The partial derivative of output with respect to the total net input
        pd_output_wrt_total_net_input = [
            output[o] * (1 - output[o]) for o in range(0, len(output))
        ]

        # The partial derivative of the total net input with respect to the weight
        pd_total_net_input_wrt_weigth = [
            self.hidden_layer.get_output(input)[o] for o in range(0, len(output))
        ]
        ############################################################

        ##################### Hidden layer #########################
        hidden_layer_output = self.hidden_layer.get_output(input)

        # The sum of the error gradients times the weight downstream
        pd_errors_wrt_output_hidden = [
            sum(
                [
                    pd_errors_wrt_output[o]
                    * pd_output_wrt_total_net_input[o]
                    * self.output_layer.neurons[o].weights[h]
                    for o in range(0, len(self.output_layer.neurons))
                ]
            )
            for h in range(0, len(hidden_layer_output))
        ]

        # The partial derivative of output with respect to the total net input
        pd_output_wrt_total_net_input_hidden = [
            hidden_layer_output[h] * (1 - hidden_layer_output[h])
            for h in range(0, len(hidden_layer_output))
        ]

        # The partial derivative of the total net input with respect to the weight
        pd_total_net_input_wrt_weigth_hidden = [
            self.hidden_layer.neurons[h].get_total_net_input(input)
            for h in range(0, len(self.hidden_layer.neurons))
        ]
        ############################################################

        # Update output layer weights:
        for o in range(0, len(self.output_layer.neurons)):
            for w in range(0, len(self.output_layer.neurons[o].weights)):
                self.output_layer.neurons[o].weights[w] -= (
                    self.LEARNING_RATE
                    * pd_errors_wrt_output[o]
                    * pd_output_wrt_total_net_input[o]
                    * pd_total_net_input_wrt_weigth[o]
                )

        # Update hidden layer weights:
        for h in range(0, len(self.hidden_layer.neurons)):
            for w in range(0, len(self.hidden_layer.neurons[h].weights)):
                self.hidden_layer.neurons[h].weights[w] -= (
                    self.LEARNING_RATE
                    * pd_errors_wrt_output_hidden[h]
                    * pd_output_wrt_total_net_input_hidden[h]
                    * pd_total_net_input_wrt_weigth_hidden[h]
                )


class NeuronLayer:
    def __init__(self, number_of_neurons, bias):
        self.neurons = [Neuron(bias) for i in range(0, number_of_neurons)]

    def get_output(self, input):
        return [neuron.get_output(input) for neuron in self.neurons]


class Neuron:
    def __init__(self, bias):
        self.bias = bias
        self.weights = []

    def get_output(self, input):
        return sigmoid(self.get_total_net_input(input))

    def get_total_net_input(self, input):
        total = 0
        for index in range(0, len(input)):
            total += input[index] * self.weights[index]

        return total + self.bias


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
    test_instances = data[0:15]
    training_instances = data[15:]

    # print("Training data:")
    # pprint(training_instances)
    # print("Test data:")
    # pprint(test_instances)

    neural_network = NeuralNetwork(
        4,
        4,
        3,
        [round(random.uniform(-0.1, 0.1), 2) for i in range(0, 16)],
        round(random.uniform(-0.1, 0.1), 2),
        [round(random.uniform(-0.1, 0.1), 2) for i in range(0, 12)],
        round(random.uniform(-0.1, 0.1), 2),
    )

    MAX_EPOCH_NUMBER = 1000
    target = [1 / 3, 1 / 3, 1 / 3]
    training_data = list(map(lambda instance: instance[0], training_instances))
    for count in range(0, MAX_EPOCH_NUMBER):
        neural_network.train(
            training_data,
            target,
        )

    print(
        "Error: "
        + str(error(target, neural_network.propagate_forward(training_data[0])))
    )

    # neural_network = NeuralNetwork(
    #     2, 2, 2, [0.15, 0.2, 0.25, 0.3], 0.35, [0.4, 0.45, 0.5, 0.55], 0.6
    # )

    # neural_network.train([[0.05, 0.10]], [[0.01, 0.99]])
    # print(
    #     [
    #         neural_network.output_layer.neurons[o].weights
    #         for o in range(0, len(neural_network.output_layer.neurons))
    #     ]
    # )

    # print(
    #     [
    #         neural_network.hidden_layer.neurons[h].weights
    #         for h in range(0, len(neural_network.hidden_layer.neurons))
    #     ]
    # )
