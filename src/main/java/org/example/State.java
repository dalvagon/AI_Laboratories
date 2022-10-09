package org.example;

import lombok.*;

import java.util.Objects;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class State {
    private Integer first;
    private Integer second;

    @Override
    public String toString() {
        return "("+ first + ", " + second + ")";
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        State state = (State) o;
        return Objects.equals(first, state.first) && Objects.equals(second, state.second);
    }

    @Override
    public int hashCode() {
        return Objects.hash(first, second);
    }
}
