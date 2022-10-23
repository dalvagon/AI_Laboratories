package org.example;

import lombok.Data;

import java.util.List;

@Data
public class Variable {
    private Integer key;
    private List<Integer> domain;
    private Integer value;

    public Variable(Integer key, List<Integer> domain, Integer value) {
        this.key = key;
        this.domain = domain;
        this.value = value;
    }
}
