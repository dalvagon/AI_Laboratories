package org.example;

import lombok.Data;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

@Data
public class Game {
    private Map<Pair<String, String>, Pair<Integer, Integer>> strategies = new HashMap<>();

    public void addStrategy(Pair<String, String> strategy, Pair<Integer, Integer> scores) {
        strategies.put(strategy, scores);
    }

    public List<Pair<String, Integer>> getPlayer1Score(String player2Strategy) {
        List<Pair<String, Integer>> scores = new ArrayList<>();

        for (Pair<String, String> strategy : strategies.keySet()) {
            if (strategy.getSecond().equals(player2Strategy)) {
                scores.add(new Pair<>(strategy.getFirst(), strategies.get(strategy).getFirst()));
            }
        }

        return scores;
    }

    public List<Pair<String, Integer>> getPlayer2Score(String player1Strategy) {
        List<Pair<String, Integer>> scores = new ArrayList<>();

        for (Pair<String, String> strategy : strategies.keySet()) {
            if (strategy.getFirst().equals(player1Strategy)) {
                scores.add(new Pair<>(strategy.getSecond(), strategies.get(strategy).getSecond()));
            }
        }

        return scores;
    }

    public String getDominantStrategyForPlayer1() {
        Set<String> chosenStrategies = new HashSet<>();

        for (String strategy : getPlayer2Strategies()) {
            chosenStrategies.addAll(getPLayer1StrategiesFor(strategy));
        }

        if (chosenStrategies.size() == 1) {
            return chosenStrategies.stream().findAny().get();
        }

        return null;
    }

    public String getDominantStrategyForPlayer2() {
        Set<String> chosenStrategies = new HashSet<>();

        for (String strategy : getPlayer1Strategies()) {
            chosenStrategies.addAll(getPLayer2StrategiesFor(strategy));
        }

        if (chosenStrategies.size() == 1) {
            return chosenStrategies.stream().findAny().get();
        }

        return null;
    }

    public List<Pair<String, String>> getNashEquilibria() {
        List<Pair<String, String>> equilibrias = new ArrayList<>();

        for (Pair<String, String> strategy : strategies.keySet()) {
            Set<String> player1Strategies = getPLayer1StrategiesFor(strategy.getSecond());
            Set<String> player2Strategies = getPLayer2StrategiesFor(strategy.getFirst());

            if(player1Strategies.contains(strategy.getFirst()) && player2Strategies.contains(strategy.getSecond())) {
                equilibrias.add(strategy);
            }
        }

        return equilibrias;
    }

    public Set<String> getPLayer1StrategiesFor(String player2Strategy) {
        Set<String> player1Strategies = new HashSet<>();
        int maximumScore = getMinimumScore();

        for (String player1Strategy : getPlayer1Strategies()) {
            int strategyScore = strategies.get(new Pair<>(player1Strategy, player2Strategy)).getFirst();
            if (strategyScore > maximumScore) {
                player1Strategies = new HashSet<>();
                player1Strategies.add(player1Strategy);
                maximumScore = strategyScore;
            }
            else if (strategyScore == maximumScore){
                player1Strategies.add(player1Strategy);
            }
        }

        return player1Strategies;
    }

    public Set<String> getPLayer2StrategiesFor(String player1Strategy) {
        Set<String> player2Strategies = new HashSet<>();
        int maximumScore = getMinimumScore();

        for (String player2Strategy : getPlayer2Strategies()) {
            int strategyScore = strategies.get(new Pair<>(player1Strategy, player2Strategy)).getSecond();
            if (strategyScore > maximumScore) {
                player2Strategies = new HashSet<>();
                player2Strategies.add(player2Strategy);
                maximumScore = strategyScore;
            }
            else if (strategyScore == maximumScore){
                player2Strategies.add(player2Strategy);
            }
        }

        return player2Strategies;
    }

    private Set<String> getPlayer1Strategies() {
        return strategies.keySet().stream().map(Pair::getFirst).collect(Collectors.toSet());
    }

    private Set<String> getPlayer2Strategies() {
        return strategies.keySet().stream().map(Pair::getSecond).collect(Collectors.toSet());
    }

    private Integer getMinimumScore() {
        return strategies.keySet().stream()
                .map(key -> strategies.get(key))
                .flatMap(pair -> Stream.of(pair.getFirst(), pair.getSecond()))
                .min(Comparator.naturalOrder())
                .get();
    }
}
