original_file = open("./originalFile1.txt", "r")
parsed_file = open("./parsedFile1.txt", "w")

lines = [line.strip() for line in original_file]
player1_moves = lines[0].split()
player1_moves.remove(player1_moves[0])

player2_moves = lines[1].split()
player2_moves.remove(player2_moves[0])

index = 2
for player1_move in player1_moves:
    scores = lines[index].split()
    index += 1
    score_index = 0
    for player2_move in player2_moves:
        two_scores = scores[score_index].split("/")
        score_index += 1
        parsed_file.write(
            player1_move
            + " "
            + player2_move
            + " "
            + two_scores[0]
            + " "
            + two_scores[1]
            + "\n"
        )
