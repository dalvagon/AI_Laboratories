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

            List<State> states = getNeighborStates(currentState);
            states.removeAll(solution.getStates());
            State bestAccessibleState = states.stream().max(Comparator.comparingInt(this::heuristic)).get();

            if (solution.getStates().contains(bestAccessibleState)) {
                System.out.println("No solution could be fomund");
                return;
            }

            solution.addState(bestAccessibleState);
        }
    }

    private int heuristic(State state) {
        return (Math.abs(state.getFirst() - problem.getDesiredOutput())) * (-1);
    }

    private void printSolution() {
        System.out.println(solution);
    }
}
