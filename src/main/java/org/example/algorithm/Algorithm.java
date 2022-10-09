package org.example.algorithm;

import lombok.RequiredArgsConstructor;
import org.example.Problem;
import org.example.Solution;
import org.example.State;

@RequiredArgsConstructor
public abstract class Algorithm {
    protected final Problem problem;
    protected Solution solution;

    public abstract void solve();

    public void initialize() {
        solution = new Solution();

        solution.addState(problem.getInitialState());
    }

    protected State fillFirstJug(State state) {
        return new State(problem.getFirstJugCapacity(), state.getSecond());
    }

    protected State fillSecondJug(State state) {
        return new State(state.getFirst(), problem.getSecondJugCapacity());
    }

    protected State transferIntoFirstJug(State state) {
        State newState = new State();
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
        State newState = new State();
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
