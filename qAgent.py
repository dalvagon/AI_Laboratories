from pprint import pprint
import random
import sys

sys.setrecursionlimit(5000)


class QAgent:
    def __init__(self, board):
        self.START = (3, 0)
        self.WIN_STATE = (3, 11)
        self.ACTIONS = ["up", "right", "down", "left"]
        self.LEARNING_RATE = 0.9
        self.DISCOUNT = 0.1
        self.epsilon = 1

        self.board = board
        self.qTable = {}
        self.rewards = {}
        self.pos = self.START

        self.init_rewards()
        self.init_QTable()

    def train(self):
        while True:
            # Select next action
            if random.uniform(0, 1) < self.epsilon:
                action = self.get_random_action()
            else:
                action = self.get_optimal_action()

            # Get next position
            nxt_pos = self.board.get_next_pos(self.pos, action)
            # End iteration if win state is reached
            if nxt_pos == self.WIN_STATE:
                self.pos = self.START
                break

            # Get the current q value
            curr_q = self.qTable[self.pos][self.ACTIONS.index(action)]

            # Update the current q value: current_q = current_q + lr * (reward + dicount * max(q') - current_q)
            self.qTable[self.pos][self.ACTIONS.index(action)] += self.LEARNING_RATE * (
                self.board.get_reward(nxt_pos)
                + self.DISCOUNT * max([q for q in self.qTable[nxt_pos] if q != None])
                - curr_q
            )

            # Update the position
            if self.board.get_reward(nxt_pos) == -100:
                self.pos = self.START  # Go to start if agent falls off cliff
            else:
                self.pos = nxt_pos  # Go to next state

        # Update epsilon
        if self.epsilon >= 0.15:
            self.epsilon -= 0.05

    # Returns the action with the biggest Q given the current position
    def get_optimal_action(self):
        max_q = max([q for q in self.qTable[self.pos] if q != None])

        return self.ACTIONS[self.qTable[self.pos].index(max_q)]

    # Returns a random action given the current position
    def get_random_action(self):
        return random.choice(
            [
                a
                for a in self.ACTIONS
                if self.qTable[self.pos][self.ACTIONS.index(a)] != None
            ]
        )

    def print_qTable(self):
        pprint(self.qTable)

    # Return the path taken by the agent
    def get_path(self):
        state = self.START
        path = {}
        step = 1
        while True:
            path[state] = step
            qs = [q for q in self.qTable[state] if q != None]
            action = self.ACTIONS[self.qTable[state].index(max(qs))]
            state = self.board.get_next_pos(state, action)
            step += 1

            if state == self.WIN_STATE:
                path[state] = step
                break

        return path

    def init_rewards(self):
        for row in range(len(self.board.cells)):
            for col in range(len(self.board.cells[0])):
                self.rewards[(row, col)] = [
                    self.board.get_reward(nxt_pos)
                    for nxt_pos in [
                        self.board.get_next_pos(
                            (row, col), action
                        )  # gets the positions obtainied by applying actions to (row, col)
                        for action in self.ACTIONS
                    ]
                ]

    def init_QTable(self):
        for row in range(len(self.board.cells)):
            for col in range(len(self.board.cells[0])):
                self.qTable[(row, col)] = [
                    None
                    if self.rewards[(row, col)][self.ACTIONS.index(a)] == None
                    else 0
                    for a in self.ACTIONS
                ]
