package org.example;

import lombok.Data;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Data
public class Problem {
    private final int firstJugCapacity;
    private final int secondJugCapacity;
    private final int desiredOutput;

    public State getInitialState() {
        return new State(0, 0);
    }

    public boolean isFinal(State state) {
        return (desiredOutput == state.getFirst() && 0 == state.getSecond()) || (desiredOutput == state.getSecond() && 0 == state.getFirst());
    }

    public boolean isSolvable() {
        return desiredOutput % gcd(firstJugCapacity, secondJugCapacity) == 0;
    }

    private int gcd(int x, int y) {
        if (y == 0) {
            return x;
        }

        return gcd(y, x % y);
    }
}
