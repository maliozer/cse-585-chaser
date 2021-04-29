
from chaser.game import Game

from tqdm import tqdm, trange

import pandas as pd
from chaser import brain

import os

if __name__ == '__main__':
    b1 = brain.Brain()
    b1.load_checkpoint()
    game_records = list()
    for game_no in trange(10):
        game = Game(brain_c1=b1)
        game_records.append((game_no, game.number_of_turn, game.blocksize))

    b1.checkpoint()

    #df = pd.DataFrame(game_records, columns=['trial', 'survival', 'blocksize'])
    #game.graph.plotSurvival(df)
    #print(df)