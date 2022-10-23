package org.example;

import lombok.Data;

import java.util.List;

@Data
public class Problem {
    private List<Variable> variables;
    private List<Constraint> constraints;

    public Problem(List<Variable> variables, List<Constraint> constraints) {
        this.variables = variables;
        this.constraints = constraints;
    }

    public void applyConstraints() {
        for (Constraint constraint : constraints) {
            getByKey(constraint.getKey()).getDomain().remove(constraint.getBlocked());
        }
    }

    public Variable getByKey(int key) {
        for (Variable variable : variables) {
            if (key == variable.getKey()) {
                return variable;
            }
        }

        return null;
    }
}
