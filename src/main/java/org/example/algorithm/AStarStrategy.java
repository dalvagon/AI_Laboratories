package org.example.algorithm;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.example.Problem;
import org.example.State;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;

public class AStarStrategy extends Algorithm {

    public AStarStrategy(Problem problem) {
        super(problem);
    }

    @Override
    public void solve() {
        System.out.println("\nSolving with the A* strategy...........");
        aStar();
        System.out.println("Solved with the A* strategy...........\n");
    }

    private void aStar() {
        State currentState = problem.getInitialState();
        int bestScore = score(problem.getFinalState());
        List<State> exploredStates = new ArrayList<>();
        List<State> sortedQueue = new LinkedList<>(this.getNeighborStates(currentState));
        sortedQueue.sort(Comparator.comparing(this::score));
        State state = firstUnexploredState(sortedQueue, exploredStates);

        while (score(state) <= bestScore) {
            if (problem.isFinal(state)) {
                bestScore = score(state);
            }

            exploredStates.add(state);
            sortedQueue.addAll(getNeighborStates(state));
            removeDuplicates(sortedQueue);
            sortedQueue.sort(Comparator.comparing(this::score));

            state = firstUnexploredState(sortedQueue, exploredStates);

            if (state == null) {
                break;
            }
        }

        printSolution(exploredStates);
    }

    private int score(State state) {
        return heuristic(state) + distance(state);
    }

    private int heuristic(State state) {
        State finalState = problem.getFinalState();
        if (finalState.getFirst() == 0) {
            return (Math.abs(state.getSecond() - problem.getDesiredOutput())) * (-1);
        }

        return (Math.abs(state.getFirst() - problem.getDesiredOutput())) * (-1);
    }

    private int distance(State state) {
        return state.getFirst() % problem.getFirstJugCapacity() + state.getSecond() % problem.getSecondJugCapacity();
    }

    private State firstUnexploredState(List<State> sortedQueue, List<State> exploredStates) {
        for (State state : sortedQueue) {
            if (!exploredStates.contains(state)) {
                return state;
            }
        }

        return null;
    }

    private void removeDuplicates(List<State> sortedQueue) {
        for (int index = 0; index < sortedQueue.size() - 1; index++) {
            State currentState = sortedQueue.get(index);
            State nextState = sortedQueue.get(index + 1);
            if (currentState == nextState) {
                if (score(currentState) >= score(nextState)) {
                    sortedQueue.remove(nextState);
                } else {
                    sortedQueue.remove(currentState);
                }
                index--;
            }
        }
    }

    private void printSolution(List<State> exploredStates) {
        State currentState = problem.getInitialState();
        List<State> partialSolution = new ArrayList<>();

        while (!problem.isFinal(currentState)) {
            List<State> neighbors = getNeighborStates(currentState);
            State nextState = neighbors.stream()
                    .filter(exploredStates::contains)
                    .filter(state -> !partialSolution.contains(state))
                    .max(Comparator.comparingInt(this::score))
                    .orElse(null);

            if (nextState == null) {
                System.out.println("No solution found");
                return;
            }

            partialSolution.add(nextState);
            currentState = nextState;
        }

        solution.getStates().addAll(partialSolution);

        System.out.println(solution);
    }
}
