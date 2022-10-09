package org.example;

import lombok.Getter;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Getter
public class Solution {
    private final List<State> states = new ArrayList<>();

    public State getLastState() {
        return states.get(states.size() - 1);
    }

    public void addState(State state) {
        states.add(state);
    }

    public void removeLastState() {
        states.remove(states.size() - 1);
    }

    @Override
    public String toString() {
        return states.stream().map(State::toString)
                .collect(Collectors.joining("\n"));
    }
}
