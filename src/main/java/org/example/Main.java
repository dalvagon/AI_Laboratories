package org.example;

import org.example.algorithm.Algorithm;
import org.example.algorithm.BFSStrategy;
import org.example.algorithm.BacktrackingStrategy;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        while (true) {
            System.out.println("\n \n \n \nEnter an instance of the water jug problem(first_jug_capacity second_jug_capacity desired_output): ");
            int firstJugCapacity = input.nextInt();
            int secondJugCapacity = input.nextInt();
            int desiredOutput = input.nextInt();

            System.out.println("Enter the number of the strategy you wish to solve the water jug problem with: ");
            System.out.println("1. Backtracking strategy");
            System.out.println("2. BFS strategy");

            int strategyNumber = input.nextInt();
            Problem problem = new Problem(firstJugCapacity, secondJugCapacity, desiredOutput);

            if (!problem.isSolvable()) {
                continue;
            }

            if (strategyNumber == 1) {
                solveWithBacktrackingStrategy(problem);
            } else if (strategyNumber == 2) {
                solveWithBFSStrategy(problem);
            }
        }
    }

    private static void solveWithBacktrackingStrategy(Problem problem) {
        Algorithm algorithm = new BacktrackingStrategy(problem);
        algorithm.initialize();
        algorithm.solve();
    }

    private static void solveWithBFSStrategy(Problem problem) {
        Algorithm algorithm = new BFSStrategy(problem);
        algorithm.initialize();
        algorithm.solve();
    }
}