
from chaser.game import Game

from tqdm import tqdm, trange

import pandas as pd

import os

if __name__ == '__main__':
    game_records = list()
    for game_no in trange(3):
        game = Game()
        game_records.append((game_no, game.number_of_turn, game.blocksize))



    df = pd.DataFrame(game_records, columns=['trial', 'survival', 'blocksize'])
    game.graph.plotSurvival(df)
    print(df)