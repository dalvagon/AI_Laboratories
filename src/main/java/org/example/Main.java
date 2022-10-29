package org.example;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Game game = new Game();

        try {
            File file = new File("src/main/resources/parsedFile.txt");
            Scanner scanner = new Scanner(file);

            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();

                String[] tokens = line.split(" ");

                game.addStrategy(new Pair<>(tokens[0], tokens[1]), new Pair<>(Integer.parseInt(tokens[2]), Integer.parseInt(tokens[3])));
            }
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        }

        String player1DominantStrategy = game.getDominantStrategyForPlayer1();
        if (player1DominantStrategy == null) {
            System.out.println("There is no dominant strategy for player 1");
        }  else {
            System.out.println("The dominant strategy for player 1 is " + player1DominantStrategy);
        }

        String player2DominantStrategy = game.getDominantStrategyForPlayer2();
        if (player2DominantStrategy == null) {
            System.out.println("There is no dominant strategy for player 2");
        }  else {
            System.out.println("The dominant strategy for player 2 is " + player2DominantStrategy);
        }

        System.out.println("The Nash Equilibrias are: " + game.getNashEquilibria());
    }
}