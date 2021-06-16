import numpy as np
import copy

def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs

class TreeNode():
    
    def __init__(self, parent, prior_p):
        self.parent = parent
        self.children = {}
        self.n_visit = 0
        self.u = 0
        self.Q = 0
        self.p = prior_p


    def expand(self, action_priors):
        for action, prior in action_priors:
            if action not in self.children:
                self.children[action] = TreeNode(self,prior)

    def select(self, c_puct):
        return max(self.children.items(),
                   key = lambda act_node: act_node[1].get_value(c_puct))

    def get_value(self, c_puct):
        self.u = (c_puct*self.p*\
                  np.sqrt(self.parent.n_visit)/(1+self.n_visit))

        return self.Q + self.u

    def update(self,leaf_value):
        self.n_visit += 1
        self.Q += 1.0*(leaf_value-self.Q)/self.n_visit

    def update_recursive(self,leaf_value):
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def is_leaf(self):
        return self.children == {}

    def is_root(self):
        return self.parent is None


class MCTS():
    def __init__(self, policy_value_fn, c_puct=5, n_playout = 2000):
        # policy_value_fn is what the neural network does, output
        # action probability pair as well as an estimated score

        self.root = TreeNode(None, 1.0)
        self.policy = policy_value_fn
        self.c_puct = c_puct
        self.n_playout = n_playout

    def playout(self, game):
        node = self.root
        while True:
            if node.is_leaf():
                break
            action, node = node.select(self.c_puct)
            ## action looks like an arrow, [(current),(next)]
           
            game.select(action[0][0],action[0][1])
            game.select(action[1][0],action[1][1])
            
            #
        action_probs, leaf_value = self.policy(game)
        winner = game.winner()
        if winner is None:
            node.expand(action_probs)
        else:
            if winner == game.get_current_player():
                leaf_value = 1.0
            else:
                leaf_value = -1.0
        # you are evaluating the child node, so need -leaf_value
        node.update_recursive(-leaf_value)
        
    def get_move_probs(self,game,temp=1e-3):
        for n in range(self.n_playout):
            game_copy = copy.deepcopy(game)
            self.playout(game_copy)

        act_visits = [(act,node.n_visit) for act, node in\
                      self.root.children.items()]
        acts, visits = zip(*act_visits)
        act_probs = softmax(1.0/temp * np.log(np.array(visits) + 1e-10))

        return acts, act_probs

    def update_with_move(self, last_move):
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
            self.root.parent = None
        else:
            self.root = TreeNode(None, 1.0)


class MCTSPlayer():
    def __init__(self, policy_value_function, c_puct = 5, n_playout = 2000,
                 is_selfplay = 0):
        
        self.mcts = MCTS(policy_value_function, c_puct, n_playout)
        self.is_selfplay = is_selfplay

    def reset_player(self):
        self.mcts.update_with_move(-1)

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, game, temp = 1e-03, return_prob = 0):
        move_probs = np.zeros([17,17,17,17])
        acts, probs = self.mcts.get_move_probs(game, temp)
       
        for i in range(len(acts)):
            move_probs[acts[i][0][0]][acts[i][0][1]][acts[i][1][0]][acts[i][1][1]]=probs[i]
        
        if self.is_selfplay:
            move_id = np.random.choice(
                    len(acts),
                    p=0.75*probs + 0.25*np.random.dirichlet(0.3*np.ones(len(probs)))
                )
            move = acts[move_id]
            self.mcts.update_with_move(move)
        else:
            move_id = np.random.choice(len(acts), p=probs)
            move = acts[move_id]
            self.mcts.update_with_move(-1)
        # human playing return moves only, self-play return move and probs to calculate policy loss 
        if return_prob:
            return move, move_probs
        else:
            return move



    
        
        
