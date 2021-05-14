from chaser.game import Game

from tqdm import tqdm, trange
import sys

from chaser.postprocessor import Postprocessor

if __name__ == '__main__':

    simulation_no = int(sys.argv[1])
    print(simulation_no)
    #game_records = list()

    for game_no in trange(100):
        game = Game(simulation_no, game_no)
        #game_records.append((game_no, game.number_of_turn, game.blocksize))

        try:
            # start post process
            simulation_process = Postprocessor(game, simulation_no)

            # save agent track
            simulation_process.save_data(game)

            # distribute discounted reward
            simulation_process.discounted_contribution(game)

            # dump dictionary model
            simulation_process.dump_pickle(is_runner=True)
            simulation_process.dump_pickle(is_runner=False)
        except:
            print("ERROR - Err occured! on game: ", game_no)


    '''
    filename = 'filename'
    outfile = open(filename, 'wb')
    pickle.dump(df_hist,outfile)
    outfile.close()

    #df = pd.DataFrame(game_records, columns=['trial', 'survival', 'blocksize'])
    #game.graph.plotSurvival(df)
    #print(df)
    '''