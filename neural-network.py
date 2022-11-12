from utils import error, sigmoid, sigmoid_derivative
from pprint import pprint
from numpy import random, array
import matplotlib.pyplot as plt


class NeuralNetwork:
    LEARNING_RATE = 0.1

    def __init__(
        self,
        number_of_input,
        number_of_hidden,
        number_of_output,
        classes,
        hidden_layer_weights,
        hidden_layer_bias,
        ouput_layer_weights,
        output_layer_bias,
    ):
        self.number_of_input = number_of_input
        self.number_of_hidden = number_of_hidden
        self.number_of_output = number_of_output
        self.classes = classes

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

    def train(self, instances):
        total_error = 0
        for instance in instances:
            input = instance[0]
            target = [1 if cls == instance[1] else 0 for cls in self.classes]
            output = self.feed_forward(input)
            total_error += error(target, output)
            self.propagate_backward(input, output, target)

        return total_error

    def feed_forward(self, input):
        hidden_layer_output = self.hidden_layer.get_layer_output(input)
        return self.output_layer.get_layer_output(hidden_layer_output)

    def propagate_backward(self, input, output, target):
        ##################### Output layer #########################
        # Individual errors
        # errors = [0.5 * pow((target[o] - output[o]), 2) for o in range(0, len(output))]
        # print(errors)

        # Total error
        # total_error = error(target, output)
        # print(total_error)

        # The partial derivative of the Error with respect to output
        pd_errors_wrt_output = [(output[o] - target[o]) for o in range(0, len(output))]

        # The partial derivative of output with respect to the total net input
        pd_output_wrt_total_net_input = [
            output[o] * (1 - output[o]) for o in range(0, len(output))
        ]

        # The partial derivative of the total net input with respect to the weight
        pd_total_net_input_wrt_weigth = [
            self.hidden_layer.get_layer_output(input)[o] for o in range(0, len(output))
        ]

        gradient = [
            pd_errors_wrt_output[o] * pd_output_wrt_total_net_input[o]
            for o in range(0, len(output))
        ]
        ############################################################

        ##################### Hidden layer #########################
        hidden_layer_output = self.hidden_layer.get_layer_output(input)

        # The sum of the error gradients times the weight downstream
        pd_errors_wrt_output_hidden = [
            sum(
                [
                    gradient[o] * self.output_layer.neurons[o].weights[h]
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
                    self.LEARNING_RATE * gradient[o] * pd_total_net_input_wrt_weigth[o]
                )

            # Update output layer biases
            self.output_layer.neurons[o].bias -= self.LEARNING_RATE * gradient[o]

        # Update hidden layer weights:
        for h in range(0, len(self.hidden_layer.neurons)):
            for w in range(0, len(self.hidden_layer.neurons[h].weights)):
                self.hidden_layer.neurons[h].weights[w] -= (
                    self.LEARNING_RATE
                    * pd_errors_wrt_output_hidden[h]
                    * pd_output_wrt_total_net_input_hidden[h]
                    * pd_total_net_input_wrt_weigth_hidden[h]
                )

            # Update output hidden layer biases:
            self.hidden_layer.neurons[h].bias -= (
                self.LEARNING_RATE
                * pd_errors_wrt_output_hidden[h]
                * pd_output_wrt_total_net_input_hidden[h]
            )


class NeuronLayer:
    def __init__(self, number_of_neurons, bias):
        self.neurons = [Neuron(bias) for i in range(0, number_of_neurons)]

    def get_layer_output(self, input):
        return [neuron.get_neuron_output(input) for neuron in self.neurons]


class Neuron:
    def __init__(self, bias):
        self.bias = bias
        self.weights = []

    def get_neuron_output(self, input):
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
    training_instances = data[10:]
    test_instances = data[0:10]
    classes = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
    training_error_values = []
    test_error_values = []

    neural_network = NeuralNetwork(
        4,
        4,
        3,
        classes,
        [random.uniform(-1, 1) for i in range(0, 16)],
        random.uniform(-1, 1),
        [random.uniform(-1, 1) for i in range(0, 12)],
        random.uniform(-1, 1),
    )

    MAX_EPOCH_NUMBER = 1000
    print("###################### Training ######################")
    for count in range(0, MAX_EPOCH_NUMBER):
        total_error = neural_network.train(training_instances)
        training_error_values.append(total_error)

    print("######################################################\n")

    print("######################Validation######################")
    error_count = 0
    for instance in training_instances:
        output = neural_network.feed_forward(instance[0])
        decision = classes[output.index(max(output))]

        if decision != instance[1]:
            error_count += 1

        colored_decision = (
            "\033[1m\033[91m" + str(decision) + "\033[0m"
            if decision != instance[1]
            else "\033[1m\033[92m" + str(decision) + "\033[0m"
        )

        print(str(instance) + " " + str(output) + " -> " + colored_decision)

    validation_error = error_count / len(training_instances)
    print(
        "Validation accuracy: "
        + "\033[1m\033[92m"
        + str((1 - validation_error) * 100)
        + "%"
        + "\033[0m"
    )
    print("######################################################\n")

    print("######################Test######################")
    error_count = 0
    for test_instance in test_instances:
        output = neural_network.feed_forward(test_instance[0])
        decision = classes[output.index(max(output))]

        if decision != test_instance[1]:
            error_count += 1

        colored_decision = (
            "\033[1m\033[91m" + str(decision) + "\033[0m"
            if decision != test_instance[1]
            else "\033[1m\033[92m" + str(decision) + "\033[0m"
        )

        print(str(test_instance) + " " + str(output) + " -> " + colored_decision)

    test_error = error_count / len(test_instances)
    print(
        "Test accuracy: "
        + "\033[1m\033[92m"
        + str((1 - test_error) * 100)
        + "%"
        + "\033[0m"
    )
    print("################################################")

    plt.plot(array(training_error_values))
    plt.show()
