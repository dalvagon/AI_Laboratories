package org.example;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Scanner;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class Main {
    public static void main(String[] args) {
        File folder = new File("src/main/resources/testFiles");

        for (File file : Objects.requireNonNull(folder.listFiles())) {
            try {
                System.out.println(file.getName() + ":");
                solve(file);
            } catch (FileNotFoundException e) {
                throw new RuntimeException(e);
            }
        }

//        try {
//            solve(new File("src/main/resources/testFiles/test.param"));
//        } catch (FileNotFoundException e) {
//            throw new RuntimeException(e);
//        }
    }

    private static void solve(File file) throws FileNotFoundException {
        Scanner scanner = new Scanner(file);
        List<Variable> variables = new ArrayList<>();
        List<Constraint> constraints = new ArrayList<>();

        int n = scanner.nextInt();
        for (int index = 1; index <= n; index++) {
            variables.add(new Variable(index, IntStream.rangeClosed(1, n).boxed().collect(Collectors.toList()), 0));
        }

        while (scanner.hasNext()) {
            Integer key = scanner.nextInt();
            Integer blocked = scanner.nextInt();

            constraints.add(new Constraint(key, blocked));
        }

        Problem problem = new Problem(variables, constraints);
        problem.applyConstraints();
        Algorithm algorithm = new Algorithm(problem);
        algorithm.solve();

        scanner.close();
    }
}