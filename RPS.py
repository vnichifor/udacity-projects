#!/usr/bin/env python3
import random

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


# Parent class
class Player:
    rounds_won = 0
    name = ""
    first_round = True

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass


# Human player
class HumanPlayer(Player):
    def move(self):
        choice = valid_input("Rock,Paper,Scissors? > ",
                             "rock", "paper", "scissors")
        return choice


# computer player that plays a random move
class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)


# computer player that plays the opponent's last choice
class ReflectPlayer(Player):
    last_move = ""

    def move(self):
        if self.first_round:
            return random.choice(moves)
        else:
            return self.last_move

    def learn(self, my_move, their_move):
        self.last_move = their_move
        self.first_round = False


# computer player that cycles through the list of moves
class CyclePlayer(Player):
    count = 0
    choice = ""

    def move(self):
        if self.first_round:
            self.first_round = False
            self.choice = random.choice(moves)
            if self.choice == "paper":
                self.count = 2
            elif self.choice == "scissors":
                self.count = 0
            else:
                self.count = 1
            return self.choice
        elif self.count != 3:
            self.choice = moves[self.count]
            self.count += 1
            return self.choice
        else:
            self.count = 1
            choice = super().move()
            return choice


# function to validate the input from the human player
def valid_input(prompt, option1, option2, option3):
    while True:
        answer = input(prompt).lower()
        if option1 == answer:
            return option1
        elif option2 == answer:
            return option2
        elif option3 == answer:
            return option3
        else:
            continue
    return answer


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


# updates/returns the number of won rounds for the given player
def keep_score(p):
    p.rounds_won += 1
    print(("* * YOU WIN " if p is HumanPlayer else f"* * {p.name} WINS ")
          + "THE ROUND! * *")
    return p.rounds_won


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        p1.name = "Player one"
        p2.name = "Player two"

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        if isinstance(self.p1, HumanPlayer):
            print(f"You played {move1}.")
        else:
            print(f"Player one chose {move1}.")
        print(f"Opponent played {move2}.")
        print(f"Player 1: {move1}  Player 2: {move2}")
        if move1 != move2:
            if beats(move1, move2):
                keep_score(self.p1)
            else:
                keep_score(self.p2)
        else:
            print("* * TIE! * *")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)
        print(f"Score: {self.p1.name} - {self.p1.rounds_won}, "
              f"{self.p2.name} - {self.p2.rounds_won}\n")

    def play_game(self):
        print("\nGame start!")
        for round in range(1, 6):
            print(f"Round {round} * * * * * * * * *")
            self.play_round()
        while True:
            if self.p1.rounds_won > self.p2.rounds_won:
                self.game_won(self.p1, self.p2)
                break
            elif self.p1.rounds_won < self.p2.rounds_won:
                self.game_won(self.p2, self.p1)
                break
            else:
                print("*****************")
                print("* * GAME TIE! * *")
                print("* * Playing one more round! * *")
                self.play_round()
                print()
        print("GAME OVER!")

    def game_won(self, p1, p2):
        print("*****************")
        print(f"Final score {p1.rounds_won} - {p2.rounds_won} "
              f"for {p1.name.upper()}")
        print(f"{p1.name.upper()} WINS THE GAME")


# menu for choosing the players of the game
def choose_player(p_number):
    choice = int(valid_input(f"Choose PLAYER {p_number.upper()}:\n"
                             "1 - Human\n"
                             "2 - Computer\n\t>>", "1", "2", "2"))
    if choice == 1:
        player = HumanPlayer()
        return player
    else:
        choice_computer = int(valid_input("Choose computer behaviour:\n"
                                          "1 - Random\n"
                                          "2 - Reflect\n"
                                          "3 - Cycle\n\t>>", "1", "2", "3"))
        if choice_computer == 1:
            player = RandomPlayer()
            return player
        elif choice_computer == 2:
            player = ReflectPlayer()
            return player
        else:
            player = CyclePlayer()
            return player


if __name__ == '__main__':
    player1 = choose_player("one")
    player2 = choose_player("two")
    game = Game(player1, player2)
    game.play_game()
