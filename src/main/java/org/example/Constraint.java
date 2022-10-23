package org.example;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class Constraint {
    private Integer key;
    private Integer blocked;
}
