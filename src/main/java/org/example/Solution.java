package org.example;

import lombok.Data;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

import java.util.HashMap;
import java.util.Map;

@Data
public class Solution {
    private Map<Integer, Integer> assignments = new HashMap<>();

    @Override
    public String toString() {
        StringBuilder stringBuilder = new StringBuilder();

        for (int key : assignments.keySet()) {
            stringBuilder.append(key).append("  ").append(assignments.get(key)).append("\n");
        }

        return stringBuilder.toString();
    }
}
