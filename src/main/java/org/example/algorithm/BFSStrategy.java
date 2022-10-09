package org.example.algorithm;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.example.Problem;
import org.example.State;

import java.util.*;

public class BFSStrategy extends Algorithm {

    public BFSStrategy(Problem problem) {
        super(problem);
    }

    @Override
    public void solve() {
        System.out.println("\nSolving with the BFS strategy...........");
        bfs();
        System.out.println("Solved with the BFS strategy...........\n");
    }

    private void bfs() {
        Queue<Node> nodes = new LinkedList<>();
        nodes.add(new Node(problem.getInitialState(), null));

        List<State> visited = new ArrayList<>();

        while (!nodes.isEmpty()) {
            Node node = nodes.poll();
            visited.add(node.getState());

            if (problem.isFinal(node.getState())) {
                printSolution(node);
                break;
            }

            State currentState = node.getState();
            List<State> states = List.of(
                    emptyFirstJug(currentState),
                    emptySecondJug(currentState),
                    transferIntoFirstJug(currentState),
                    transferIntoSecondJug(currentState),
                    fillFirstJug(currentState),
                    fillSecondJug(currentState)
            );

            for(State state : states) {
                if(!visited.contains(state)) {
                    nodes.add(new Node(state, node));
                }
            }
        }
    }

    private void printSolution(Node node) {
        if(node != null) {
            printSolution(node.previous);
            System.out.println(node.getState());
        }
    }

    @Data
    @AllArgsConstructor
    private static class Node {
        State state;
        Node previous;
    }
}
