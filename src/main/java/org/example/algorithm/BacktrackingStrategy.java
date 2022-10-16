package org.example.algorithm;

import org.example.Problem;
import org.example.State;

import java.util.List;

public class BacktrackingStrategy extends Algorithm {

    public BacktrackingStrategy(Problem problem) {
        super(problem);
    }

    @Override
    public void solve() {
        System.out.println("\nSolving with the backtracking strategy...........");
        backtrack();
        System.out.println("Solved with the backtracking strategy...........\n");
    }

    private void backtrack() {
        State currentState = solution.getLastState();
        List<State> states = getAvailableStates(currentState);

        for (State state : states) {
            if (isValid(state)) {
                solution.addState(state);
                System.out.println(state);
                if (problem.isFinal(state)) {
                    System.out.println("Found a new solution:\n" + solution);
                } else {
                    backtrack();
                }
                solution.removeLastState();
            }
        }
    }

    private boolean isValid(State state) {
        return !solution.getStates().contains(state);
    }
}
