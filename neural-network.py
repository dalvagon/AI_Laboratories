from utils import error, sigmoid, sigmoid_derivative
from pprint import pprint
from numpy import random, array
import matplotlib.pyplot as plt


class NeuralNetwork:
    LEARNING_RATE = 0.01

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
            for _ in range(self.number_of_input):
                self.hidden_layer.neurons[h].weights.append(weights[index])
                index += 1

    def init_weights_from_hidden_to_output(self, weights):
        index = 0
        for o in range(len(self.output_layer.neurons)):
            for _ in range(self.number_of_hidden):
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


def print_confusion_matrix(actuals_and_predictions):
    predictions = list(
        set(
            list(
                map(
                    lambda actual_and_prediction: actual_and_prediction[1],
                    actuals_and_predictions,
                )
            )
        )
    )

    actuals = list(
        set(
            list(
                map(
                    lambda actual_and_prediction: actual_and_prediction[0],
                    actuals_and_predictions,
                )
            )
        )
    )

    space_adjust = (
        max([len(string) for string in actuals + predictions]) + len("Predicted") + 5
    )

    print("".ljust(space_adjust), end="")
    for prediction in predictions:
        print("Predicted " + prediction.ljust(space_adjust), end="")
    print("\n")

    for actual in actuals:
        print("Actual " + actual.ljust(space_adjust), end="")
        for prediction in predictions:
            count = len(
                [
                    actuals_and_predictions
                    for actual_and_prediction in actuals_and_predictions
                    if actual_and_prediction[0] == actual
                    and actual_and_prediction[1] == prediction
                ]
            )

            print(
                str(count)
                + " / "
                + str(len(actuals_and_predictions)).ljust(space_adjust),
                end="",
            )

        print("\n")


def scatter_points(true_predicted_points, false_predicted_points):
    plt.scatter(
        [tup[0] for tup in true_predicted_points],
        [tup[1] for tup in true_predicted_points],
        color="green",
        label="Correctly classified",
        marker="+",
    )

    plt.scatter(
        [tup[0] for tup in false_predicted_points],
        [tup[1] for tup in false_predicted_points],
        color="red",
        label="Incorrectly classified",
        marker="_",
    )

    plt.legend()
    plt.show()


if __name__ == "__main__":
    input_file = open("./iris.data", "r")
    data = read_data(input_file)
    random.shuffle(data)
    training_instances = data[10:]
    test_instances = data[0:10]
    classes = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
    training_error_values = []

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

    plt.plot(array(training_error_values))
    plt.title("Error as function of epochs")
    plt.show()
    print("######################################################\n")

    print("######################Validation######################")
    true_predicted_points = []
    false_predicted_points = []
    actuals_and_predictions = []
    error_count = 0
    for instance in training_instances:
        output = neural_network.feed_forward(instance[0])
        prediction = classes[output.index(max(output))]

        actuals_and_predictions.append((instance[1], prediction))

        if prediction != instance[1]:
            false_predicted_points.append(
                (
                    instance[0][0] + instance[0][1],
                    instance[0][2] + instance[0][3],
                )
            )
            error_count += 1
        else:
            true_predicted_points.append(
                (
                    instance[0][0] + instance[0][1],
                    instance[0][2] + instance[0][3],
                )
            )

        colored_prediction = (
            "\033[1m\033[91m" + str(prediction) + "\033[0m"
            if prediction != instance[1]
            else "\033[1m\033[92m" + str(prediction) + "\033[0m"
        )

        print(str(instance) + " " + str(output) + " -> " + colored_prediction)

    validation_error = error_count / len(training_instances)
    print(
        "Validation accuracy: "
        + "\033[1m\033[92m"
        + str((1 - validation_error) * 100)
        + "%"
        + "\033[0m"
    )

    print_confusion_matrix(actuals_and_predictions)
    scatter_points(true_predicted_points, false_predicted_points)
    print("######################################################\n")

    print("######################Test######################")
    actuals_and_predictions = []
    true_predicted_points = []
    false_predicted_points = []
    error_count = 0
    for test_instance in test_instances:
        output = neural_network.feed_forward(test_instance[0])
        prediction = classes[output.index(max(output))]

        actuals_and_predictions.append((test_instance[1], prediction))

        if prediction != test_instance[1]:
            false_predicted_points.append(
                (
                    test_instance[0][0] + test_instance[0][1],
                    test_instance[0][2] + test_instance[0][3],
                )
            )
            error_count += 1
        else:
            true_predicted_points.append(
                (
                    test_instance[0][0] + test_instance[0][1],
                    test_instance[0][2] + test_instance[0][3],
                )
            )

        colored_prediction = (
            "\033[1m\033[91m" + str(prediction) + "\033[0m"
            if prediction != test_instance[1]
            else "\033[1m\033[92m" + str(prediction) + "\033[0m"
        )

        print(str(test_instance) + " " + str(output) + " -> " + colored_prediction)

    test_error = error_count / len(test_instances)
    print(
        "Test accuracy: "
        + "\033[1m\033[92m"
        + str((1 - test_error) * 100)
        + "%"
        + "\033[0m"
    )

    print_confusion_matrix(actuals_and_predictions)
    scatter_points(true_predicted_points, false_predicted_points)
    print("################################################")
