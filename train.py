from board import board
from game import game
import numpy as np
import random
from mcts_alpha import MCTSPlayer
from network import policyvaluenet
from collections import defaultdict, deque
import pygame


class TrainPipeline():
    def __init__(self, init_model=None):
        # params of the board and the game
      
        self.board = board()
        self.game = game()
        # training params
        self.learn_rate = 2e-3
        
        self.temp = 1.0  # the temperature param
        self.n_playout = 400  # num of simulations for each move
        self.c_puct = 5
        self.buffer_size = 10000
        self.batch_size = 64  # mini-batch size for training
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.play_batch_size = 1
        self.epochs = 1  # num of train_steps for each update
        self.kl_targ = 0.02
        self.check_freq = 50
        self.game_batch_num = 1500
        self.best_win_ratio = 0.0
        # num of simulations used for the pure mcts, which is used as
        # the opponent to evaluate the trained policy
        self.pure_mcts_playout_num = 1000
        if init_model:
            # start training from an initial policy-value net
            self.policy_value_net = policyvaluenet(model_file=init_model)
        else:
            # start training from a new policy-value net
            self.policy_value_net = policyvaluenet()
        self.mcts_player = MCTSPlayer(self.policy_value_net.policy_value_fn,
                                      c_puct=self.c_puct,
                                      n_playout=self.n_playout,
                                      is_selfplay=1)


    def collect_selfplay_data(self, n_games=1):
        """collect self-play data for training"""
        #FPS = 60
        #WIN = pygame.display.set_mode((400, 800))
        #pygame.display.set_caption('Checkers')
        for i in range(n_games):
            winner, play_data = self.game.start_self_play(self.mcts_player,
                                                          temp=self.temp,show=None)
            print(winner)
            play_data = list(play_data)[:]
            self.episode_len = len(play_data)
            # augment the data
            self.data_buffer.extend(play_data)

    def policy_update(self):
        """update the policy-value net"""
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = np.reshape([data[1] for data in mini_batch],[self.batch_size,17*17*17*17])
        winner_batch = [data[2] for data in mini_batch]
     
        for i in range(self.epochs):
            print("start training")
            loss, entropy = self.policy_value_net.train(
                    state_batch,
                    mcts_probs_batch,
                    winner_batch,
                    self.learn_rate)
            
        print((
               
               "loss:{}").format(loss))
        return loss

    def run(self):
        """run the training pipeline"""
        try:
            for i in range(self.game_batch_num):
                self.collect_selfplay_data(self.play_batch_size)
                print("batch i:{}, episode_len:{}".format(
                        i+1, self.episode_len))
                if len(self.data_buffer) > self.batch_size:
                    loss= self.policy_update()
                # check the performance of the current model,
                # and save the model params
                if (i+1) % self.check_freq == 0:
                    print("current self-play batch: {}".format(i+1))
                    #win_ratio = self.policy_evaluate()
                    self.policy_value_net.save_model('./current_policy.model')
                    
        except KeyboardInterrupt:
            print('\n\rquit')

if __name__ == '__main__':
    training_pipeline = TrainPipeline()
    training_pipeline.run()
