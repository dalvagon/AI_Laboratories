package org.example.algorithm;

import org.example.Problem;
import org.example.State;

import java.util.Comparator;
import java.util.List;

public class HillClimbingStrategy extends Algorithm {
    public HillClimbingStrategy(Problem problem) {
        super(problem);
    }

    @Override
    public void solve() {
        System.out.println("\nSolving with the Hillclimbing strategy...........");
        hillclimb();
        System.out.println("Solved with the Hillclimbing strategy...........\n");
    }

    private void hillclimb() {
        while (true) {
            State currentState = solution.getLastState();

            if (problem.isFinal(currentState)) {
                printSolution();
                return;
            }

            List<State> states = getAvailableStates(currentState);
            states.removeAll(solution.getStates());
            State bestAccessibleState = states.stream().min(Comparator.comparingInt(this::heuristic)).get();

            if (solution.getStates().contains(bestAccessibleState)) {
                System.out.println("No solution could be found");
                return;
            }

            solution.addState(bestAccessibleState);
        }
    }

    private int heuristic(State state) {
        return Math.abs(problem.getFirstJugCapacity() + problem.getSecondJugCapacity() - problem.getDesiredOutput() - state.getFirst() - state.getSecond());
    }

    private void printSolution() {
        for (State state : solution.getStates()) {
            System.out.println(state + " " + heuristic(state));
        }
    }
}
