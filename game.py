import numpy as np
import random
import itertools

NULL_TOKEN = [-1, -1]
INIT_OXYGEN = 25



def jumpingPlayers(min, max, players):
    jump = 0
    for p in players:
        if p.position >= min and p.position <= max:
            jump += 1
    return jump


def valueTreasure(tokens):
    return sum(token[1] for token in tokens)



class Player:

    def __init__(self, name):
        self.treasure = 0
        self.position = 0
        self.forward = True
        self.tokens = []
        self.name = name

    def Move(self, players):
        dice = random.randint(1, 3) + random.randint(1,3)
        print(f"A dice is thrown... {dice}")

        [pos_min, pos_max] = [self.position + 1, self.position + dice] \
                        if self.forward \
                        else [self.position - dice, self.position - 1]

        jump = jumpingPlayers(pos_min, pos_max, players)
        increment = max(0, dice + jump - len(self.tokens))
        self.position += increment if self.forward else -increment
        if jump:
            print(f"You jump over {jump} player(s).")


class Game:

    def __init__(self, players, n_rounds=3, oxygen=25):
        self.tokens = [
            [1, 0], [1, 1], [1, 3], [1, 2], [1, 1], [1, 2],
            [2, 4], [2, 5], [2, 6], [2, 7], [2, 5], [2, 6],
            [3, 10], [3, 8], [3, 9], [3, 10], [3, 8], [3, 9],
            [4, 11], [4, 12], [4, 13], [4, 12], [4, 15], [4, 12]]
        self.oxygen = oxygen
        self.n_rounds = n_rounds
        self.rnd = 0
        self.players = players
        self.turn = 0
        self.players_in_rnd = players.copy()
        self.isPlaying = True


    def NextPlayer(self):
        self.turn = 0 if self.turn == len(self.players_in_rnd) - 1 \
                      else self.turn + 1
        player = self.players_in_rnd[self.turn - 1]
        self.oxygen -= len(player.tokens)
        print(f"It is the turn of {player.name}. Oxygen is now {self.oxygen}")
        return player


    def RemovePlayer(self):
        del self.players_in_rnd[self.turn-1]
        self.turn -= 1


    def EndGame(self):
        print("The game is over!")
        max = -1
        winner = None
        for p in players:
            if p.treasure > max:
                max = p.treasure
                winner = p
        print(f"The winner is {winner.name}")

    def StartNewRound(self):
        for p in self.players:
            p.forward = True
        self.players_in_rnd = self.players.copy()
        self.turn = 0
        self.oxygen = INIT_OXYGEN
        # remove null tokens
        self.tokens = [x for x in self.tokens if x != NULL_TOKEN]


    def EndRound(self):
        print("The round is over!")
        self.rnd += 1
        if self.rnd == self.n_rounds:
            # end of the game
            self.EndGame()
            self.isPlaying = False
        else:
            # start a new round
            print(f"Let's start the round {self.rnd}!\n")
            self.StartNewRound()

    def CheckOxygen(self):
        if self.oxygen < 0:
            print("Oops... There is no more oxygen")
            for player in self.players_in_rnd:
                print(f"{player.name} has to release his/her tokens")
                player.tokens = []
            self.EndRound()





if __name__ == "__main__":
    names = ["Lolo", "Samuel", "Pilou"]
    players = [Player(name) for name in names]
    game = Game(players, n_rounds = 3, oxygen = INIT_OXYGEN)

    while game.isPlaying:
        game.CheckOxygen()
        player = game.NextPlayer()

        if player.forward:
            ans = input("Do you want to go backward? Yes/[No]")
            if ans == "Yes" or ans == "Y":
                player.forward = False

        player.Move(game.players_in_rnd)

        if player.position >= 0:
            print(f"You new position is {player.position}")
            [side_up, side_down] = game.tokens[player.position]

            if side_up == -1 and len(player.tokens):
                ans = input("There is no token. Do you want to leave a token here? Yes/[No]")
                if ans == "Yes" or ans == "Y":
                    print("Which token do you want to leave?")
                    for i, token in enumerate(player.tokens):
                        print(f"Answer {i} for the token {token[0]}")
                    number = int(input("(answer the number)"))
                    game.tokens[player.position] = player.tokens[number]
                    player.tokens.remove(player.tokens[number])


            elif side_up >= 0:
                ans = input(f"There is a token with {side_up}. Do you want to take it with you? Yes/[No]")
                if ans == "Yes" or ans == "Y":
                    player.tokens.append([side_up, side_down])
                    game.tokens[player.position] = NULL_TOKEN
                    print(f"Great! You know have {len(player.tokens)} token(s)")




        else:
            # the player arrived at the submarine
            print(f"Congratulations, you arrived safely into the submarine!")
            value = valueTreasure(player.tokens)
            print(f"You took back {value}")
            player.treasure += value
            player.tokens = []
            print(f"You have now a treasure of {player.treasure}!")
            game.RemovePlayer()

            if not len(game.players_in_rnd):
                # end of a round
                game.EndRound()


        print("")
