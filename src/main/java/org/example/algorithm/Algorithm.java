package org.example.algorithm;

import lombok.RequiredArgsConstructor;
import org.example.Problem;
import org.example.Solution;
import org.example.State;

import java.util.List;
import java.util.stream.Collectors;

@RequiredArgsConstructor
public abstract class Algorithm {
    protected final Problem problem;
    protected Solution solution;

    public abstract void solve();

    public void initialize() {
        solution = new Solution();

        solution.addState(problem.getInitialState());
    }

    public List<State> getAvailableStates(State state) {
        List<State> availableStates = new java.util.ArrayList<>(List.of(
                emptyFirstJug(state),
                emptySecondJug(state),
                transferIntoFirstJug(state),
                transferIntoSecondJug(state),
                fillFirstJug(state),
                fillSecondJug(state)
        ));

        availableStates = availableStates.stream().distinct().collect(Collectors.toList());
        availableStates.remove(state);

        return availableStates;
    }

    protected State fillFirstJug(State state) {
        return new State(problem.getFirstJugCapacity(), state.getSecond());
    }

    protected State fillSecondJug(State state) {
        return new State(state.getFirst(), problem.getSecondJugCapacity());
    }

    protected State transferIntoFirstJug(State state) {
        State newState;
        int firstJugFreeSpace = problem.getFirstJugCapacity() - state.getFirst();
        if (firstJugFreeSpace <= state.getSecond()) {
            newState = fillFirstJug(state);
            newState.setSecond(state.getSecond() - firstJugFreeSpace);
        } else {
            newState = emptySecondJug(state);
            newState.setFirst(state.getFirst() + state.getSecond());
        }

        return newState;
    }

    protected State transferIntoSecondJug(State state) {
        State newState;
        int secondJugFreeSpace = problem.getSecondJugCapacity() - state.getSecond();
        if (secondJugFreeSpace <= state.getFirst()) {
            newState = fillSecondJug(state);
            newState.setFirst(state.getFirst() - secondJugFreeSpace);
        } else {
            newState = emptyFirstJug(state);
            newState.setSecond(state.getSecond() + state.getFirst());
        }

        return newState;
    }

    protected State emptyFirstJug(State state) {
        return new State(0, state.getSecond());
    }

    protected State emptySecondJug(State state) {
        return new State(state.getFirst(), 0);
    }
}
