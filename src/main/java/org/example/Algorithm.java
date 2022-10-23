package org.example;

import lombok.RequiredArgsConstructor;

import java.util.*;
import java.util.stream.IntStream;

@RequiredArgsConstructor
public class Algorithm {
    private final Problem problem;
    private final Solution solution = new Solution();
    private boolean foundSolution = false;

    public void solve() {
        backtrack(getMinimumRemainingValuesVariable());

        if (!foundSolution) {
            System.out.println("No solution found");
        }
    }

    private void backtrack(Variable minimumRemainingValuesVariable) {
        if(foundSolution) {
            return;
        }

        if (minimumRemainingValuesVariable != null) {
            List<Integer> minimumRemainingValuesVariableDomain = getDomainFor(minimumRemainingValuesVariable);
            for (Integer value : minimumRemainingValuesVariableDomain) {
                minimumRemainingValuesVariable.setValue(value);
                solution.getAssignments().put(minimumRemainingValuesVariable.getKey(), value);

                if (foundSolution()) {
                    System.out.println(solution);
                    foundSolution = true;
                } else {
                    backtrack(getMinimumRemainingValuesVariable());
                }

                minimumRemainingValuesVariable.setValue(0);
            }
        }
    }

    private Variable getMinimumRemainingValuesVariable() {
        return problem.getVariables().stream()
                .filter(variable -> variable.getDomain().size() > 0)
                .filter(variable -> variable.getValue() == 0)
                .min(Comparator.comparingInt(variable -> variable.getDomain().size()))
                .orElse(null);
    }

    private List<Integer> getDomainFor(Variable variable) {
        List<Integer> domain = new ArrayList<>(IntStream.rangeClosed(1, problem.getVariables().size()).boxed().toList());

        for (Variable otherVariable : problem.getVariables()) {
            int index = variable.getKey() - otherVariable.getKey();
            int value = otherVariable.getValue();

            if(value != 0) {
                domain.removeAll(Arrays.asList(
                                value,
                                value - index,
                                value + index
                        )
                );
            }
        }

        return domain;
    }

    private boolean foundSolution() {
        for (Variable variable : problem.getVariables()) {
            if (variable.getValue() == 0) {
                return false;
            }
        }

        return true;
    }
}
