
from chaser.game import Game

from tqdm import tqdm, trange

import pandas as pd
import numpy as np

import os
import pickle


def save_data(game):
    game.runner_track = np.delete(game.runner_track, 0, 0)
    game.ch1_track = np.delete(game.ch1_track, 0, 0)
    game.ch2_track = np.delete(game.ch2_track, 0, 0)

    pd.DataFrame(game.runner_track).to_csv('./simulation/runner.csv', index=False)
    pd.DataFrame(game.ch1_track).to_csv('./simulation/ch1.csv', index=False)
    pd.DataFrame(game.ch2_track).to_csv('./simulation/ch2.csv', index=False)


if __name__ == '__main__':
    game_records = list()
    df_hist = pd.DataFrame()
    df_hist.astype(object)
    print(os.listdir())
    for game_no in trange(1):
        game = Game()
        game_records.append((game_no, game.number_of_turn, game.blocksize))

        save_data(game)




    '''
    filename = 'filename'
    outfile = open(filename, 'wb')
    pickle.dump(df_hist,outfile)
    outfile.close()

    #df = pd.DataFrame(game_records, columns=['trial', 'survival', 'blocksize'])
    #game.graph.plotSurvival(df)
    #print(df)
    '''