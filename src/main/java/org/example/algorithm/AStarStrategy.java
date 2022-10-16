package org.example.algorithm;

import org.example.Problem;

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

    }
}
