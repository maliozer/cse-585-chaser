import numpy as np
import pandas as pd

from collections import defaultdict

import pickle

class Postprocessor():
    def __init__(self, game, simulation_id):
        self.simulation_id = str(simulation_id)
        self.game = game

        if simulation_id == 7:
            self.runner_history = defaultdict()
            self.chaser_history = defaultdict()
        else:
            self.runner_history, self.chaser_history = self.load_pickle()

    def save_data(self, game):
        game.runner_track = np.delete(game.runner_track, 0, 0)
        game.runner_move_track = np.delete(game.runner_move_track, 0, 0)

        pd.DataFrame(game.runner_track).to_csv('./simulations/simulation'+self.simulation_id+'/runner.csv', index=False)
        pd.DataFrame(game.runner_move_track).to_csv('./simulations/simulation'+self.simulation_id+'/runner_actions.csv', index=False)

        if game.winner == 1:
            game.ch1_track = np.delete(game.ch1_track, 0, 0)
            game.ch1_move_track = np.delete(game.ch1_move_track, 0, 0)

            pd.DataFrame(game.ch1_track).to_csv('./simulations/simulation'+self.simulation_id+'/ch1.csv', index=False)
            pd.DataFrame(game.ch1_move_track).to_csv('./simulations/simulation'+self.simulation_id+'/ch1_actions.csv', index=False)

        elif game.winner == 2:
            game.ch2_track = np.delete(game.ch2_track, 0, 0)
            game.ch2_move_track = np.delete(game.ch2_move_track, 0, 0)

            pd.DataFrame(game.ch2_track).to_csv('./simulations/simulation'+self.simulation_id+'/ch2.csv', index=False)
            pd.DataFrame(game.ch2_move_track).to_csv('./simulations/simulation'+self.simulation_id+'/ch2_actions.csv', index=False)

    def save_experience(self, df_actions, is_runner=True):
        if is_runner:
            agent_history = self.runner_history
        else:
            agent_history = self.chaser_history

        for row in df_actions.iterrows():
            action = row[1][0]
            reward = row[1][1]
            state = row[1][2]

            if state not in agent_history.keys():
                agent_history[state] = defaultdict(list)
            agent_history[state][action].append(reward)

    def dump_pickle(self, is_runner=True):
        if is_runner:
            agent_history = self.runner_history
            path = 'models/model'+self.simulation_id+'/' + 'runner_model'
        else:
            agent_history = self.chaser_history
            path = 'models/model'+self.simulation_id+'/' + 'chaser_model'

        outfile = open(path, 'wb')
        pickle.dump(agent_history, outfile)
        outfile.close()

    def load_pickle(self):
        paths = ['models/model'+self.simulation_id+'/runner_model', 'models/model'+self.simulation_id+'/chaser_model']
        models = list()
        for path in paths:
            file = open(path, 'rb')
            model = pickle.load(file)
            file.close()
            models.append(model)
        return models[0], models[1]

    # reward function
    def get_chaser_reward(self, df, gamma=0.65):
        df['reward'] = 100 - (df.index.values ** gamma)
        df = df[df.reward > 20]
        return df

    def get_runner_reward(self, df, gamma=0.65):
        df['reward'] = df.index.values ** gamma

    def discounted_contribution(self, game):
        # chaser model
        if game.winner == 1:
            df_chaser_actions = pd.read_csv('./simulations/simulation'+self.simulation_id+'/ch1_actions.csv')
            df_chaser_states = pd.read_csv('./simulations/simulation'+self.simulation_id+'/ch1.csv', sep='#')

        elif game.winner == 2:
            df_chaser_actions = pd.read_csv('./simulations/simulation'+self.simulation_id+'/ch2_actions.csv')
            df_chaser_states = pd.read_csv('./simulations/simulation'+self.simulation_id+'/ch2.csv', sep='#')


        df_chaser_actions.columns = ['action']
        df_chaser_actions = df_chaser_actions[::-1].reset_index(drop=True)

        df_chaser_states.columns = ['state']
        df_chaser_states = df_chaser_states[::-1].reset_index(drop=True)
        df_chaser_actions = self.get_chaser_reward(df_chaser_actions)
        df_chaser_actions['state'] = df_chaser_states['state']

        # runner model
        df_runner_actions = pd.read_csv('./simulations/simulation'+self.simulation_id+'/runner_actions.csv')
        df_runner_actions.columns = ['action']
        df_runner_actions = df_runner_actions[::-1].reset_index(drop=True)

        df_runner_states = pd.read_csv('./simulations/simulation'+self.simulation_id+'/runner.csv', sep='#')
        df_runner_states.columns = ['state']
        df_runner_states = df_runner_states[::-1].reset_index(drop=True)

        self.get_runner_reward(df_runner_actions)
        df_runner_actions['state'] = df_runner_states['state']

        self.save_experience(df_runner_actions)
        self.save_experience(df_chaser_actions, is_runner=False)
