package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Pair<K, V> {
    private K first;
    private V second;

    @Override
    public String toString() {
        return "(" + first +
                ", " + second +
                ')';
    }
}
