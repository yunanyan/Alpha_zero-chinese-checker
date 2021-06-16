
import numpy as np
import tensorflow as tf

class policyvaluenet():
    def __init__(self, checkpoint=None):
        self.input_states = tf.placeholder(tf.float32, \
                                           shape=[None, 4, 17,17])
        # why need this transpose?
        self.input_state = tf.transpose(self.input_states, [0,2,3,1])
        
        # convolution blocks
        self.conv1 = tf.layers.conv2d(inputs=self.input_state, filters=32,
                                      kernel_size = [3,3], padding = 'same',
                                      data_format = 'channels_last',
                                      activation = tf.nn.relu)
        self.conv2 = tf.layers.conv2d(inputs=self.conv1, filters=64,
                                      kernel_size=[3, 3], padding="same",
                                      data_format="channels_last",
                                      activation=tf.nn.relu)
        self.conv3 = tf.layers.conv2d(inputs=self.conv2, filters=128,
                                      kernel_size=[3, 3], padding="same",
                                      data_format="channels_last",
                                      activation=tf.nn.relu)
        # policy_head
        self.action_conv = tf.layers.conv2d(inputs=self.conv3, filters=4,
                                            kernel_size=[1, 1], padding="same",
                                            data_format="channels_last",
                                            activation=tf.nn.relu)
        self.action_conv_flat = tf.reshape(
                self.action_conv, [-1, 4*17*17])
        self.action_fc = tf.layers.dense(inputs=self.action_conv_flat,
                                         units=17*17*17*17,
                                         activation=tf.nn.log_softmax)
        # Reshape for convenience
        self.action_fc2 = tf.reshape(self.action_fc, shape = [17,17,17,17])
        
        

        # value head
        self.evaluation_conv = tf.layers.conv2d(inputs=self.conv3, filters=2,
                                                kernel_size=[1, 1],
                                                padding="same",
                                                data_format="channels_last",
                                                activation=tf.nn.relu)
        self.evaluation_conv_flat = tf.reshape(
                self.evaluation_conv, [-1, 2 *17*17])
        self.evaluation_fc1 = tf.layers.dense(inputs=self.evaluation_conv_flat,
                                              units=64, activation=tf.nn.relu)
        self.evaluation_fc2 = tf.layers.dense(inputs=self.evaluation_fc1,
                                              units=1, activation=tf.nn.tanh)
        # win or not as the label
        self.labels = tf.placeholder(tf.float32, shape=[None, 1])
        self.value_loss = tf.losses.mean_squared_error(self.labels,
                                                       self.evaluation_fc2)
        # policy loss
        self.mcts_probs = tf.placeholder(
                tf.float32, shape=[None, 17*17*17*17])
        self.policy_loss = tf.negative(tf.reduce_mean(
                tf.reduce_sum(tf.multiply(self.mcts_probs, self.action_fc), 1)))
        # regularization loss
        l2_penalty_beta = 1e-4
        vars = tf.trainable_variables()
        l2_penalty = l2_penalty_beta * tf.add_n(
            [tf.nn.l2_loss(v) for v in vars if 'bias' not in v.name.lower()])
        # total loss
        self.loss = self.value_loss + self.policy_loss + l2_penalty
        self.learning_rate = tf.placeholder(tf.float32)
        self.optimizer = tf.train.AdamOptimizer(
                learning_rate=self.learning_rate).minimize(self.loss)

        # Make a session
        self.session = tf.Session()
        self.entropy = tf.negative(tf.reduce_mean(
                tf.reduce_sum(tf.exp(self.action_fc) * self.action_fc, 1)))
        self.session.run(tf.global_variables_initializer())
        self.saver = tf.train.Saver()
        if checkpoint is not None:
            self.restore_model(checkpoint)
    
        
    def policy_value(self, inputs):
        """
        input: a batch of states
        output: a batch of action probabilities and state values
        """
        log_act_probs, value = self.session.run(
                [self.action_fc2, self.evaluation_fc2],
                feed_dict={self.input_states: inputs}
                )
        act_probs = np.exp(log_act_probs)
        return act_probs, value

    def policy_value_fn(self, game):
        """
        input: board
        output: a list of (action, probability) tuples for each available
        action and the score of the board state
        """
        current_state = np.ascontiguousarray(game.get_currentstate().reshape(-1,4,17,17))
        act_probs, value = self.policy_value(current_state)
        legal_moves = game.get_all_valid_moves()
        
        probs = []

       
        
        
        for item in legal_moves:
            index1 = item[0][0]
            index2 = item[0][1]
            index3 = item[1][0]
            index4 = item[1][1]
            probs.append(act_probs[index1,index2,index3,index4])
            
        act_probs = zip(legal_moves, probs)
        return act_probs, value

    def train(self, inputs, mcts_probs, win, lr):
        win = np.reshape(win, (-1,1))
        loss, entropy, _ = self.session.run([self.loss, self.entropy,self.optimizer],
                                            feed_dict={self.input_states:inputs,
                                                       self.mcts_probs: mcts_probs,
                                                       self.labels: win,
                                                       self.learning_rate:lr})
        return loss, entropy

    def save_model(self, model_path):
        self.saver.save(self.session, model_path)

    def restore_model(self, model_path):
        self.saver.restore(self.session, model_path)





        
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    

    
