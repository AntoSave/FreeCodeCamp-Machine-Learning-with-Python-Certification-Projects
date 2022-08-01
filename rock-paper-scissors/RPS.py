import random
import functools
# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago.

def player(prev_play, opponent_history=[]):
    if prev_play != "":
      opponent_history.append(prev_play)
  
    """
    guess = "R"
    if len(opponent_history) > 2:
        guess = opponent_history[-2]
    """
    #guess=get_random_guess() #Results: about 50% win rate against all players
    #guess=get_frequentist_guess(opponent_history) #Results:50% win rate against quincy, then 30% or less
    #guess=get_frequentist_guess_2(opponent_history) #Results: 85% win rate against mrugesh, 100% win rate against quincy
    #guess=get_frequentist_guess_3(opponent_history) #Results: 70% win rate against mrugesh, 92% win rate against quincy, 86% win rate against kris, 59% win rate against abbey
    guess=get_frequentist_guess_n(opponent_history,4) #GG
    return guess


#Generate a random guess. Used to have a performance baseline.
def get_random_guess():
  choices = ["R","P","S"]
  return random.choice(choices)

#Returns optimal move based on opponent's predicted move.
def get_best_counter(opponent_move):
  best_moves = {"R": "P", "P": "S", "S": "R"}
  return best_moves[opponent_move]
  
#Returns a guess based on the predicted move of the opponent.
#The predicted move is the one played the most.
def get_frequentist_guess(opponent_history):
  opponent_moves_count = {"R":0, "P":0, "S": 0}
  for move in opponent_history:
    opponent_moves_count[move] += 1
  return get_best_counter(max(opponent_moves_count,key=opponent_moves_count.get))

#Returns a guess based on the predicted move of the opponent.
#The predicted move is the one played the most after the last move.
def get_frequentist_guess_2(opponent_history):
  opponent_moves_count = {"R":{"R":0, "P":0, "S": 0},
                          "P":{"R":0, "P":0, "S": 0},
                          "S":{"R":0, "P":0, "S": 0}}
  for move_i in range(1,len(opponent_history)):
    move = opponent_history[move_i]
    prev_move = opponent_history[move_i-1]
    opponent_moves_count[prev_move][move] += 1
  last_move = opponent_history[-1] if len(opponent_history) != 0 else "R"
  return get_best_counter(max(opponent_moves_count[last_move],key=opponent_moves_count[last_move].get))

#Returns a guess based on the predicted move of the opponent.
#The predicted move is the one played the most after the last two moves.
def get_frequentist_guess_3(opponent_history):
  opponent_moves_count = {"R":{
                              "R":{"R":0, "P":0, "S": 0},
                              "P":{"R":0, "P":0, "S": 0},
                              "S":{"R":0, "P":0, "S": 0}
                              },
                          "P":{
                              "R":{"R":0, "P":0, "S": 0},
                              "P":{"R":0, "P":0, "S": 0},
                              "S":{"R":0, "P":0, "S": 0}
                              },
                          "S":{
                              "R":{"R":0, "P":0, "S": 0},
                              "P":{"R":0, "P":0, "S": 0},
                              "S":{"R":0, "P":0, "S": 0}
                              }
                         }
  for move_i in range(2,len(opponent_history)):
    move = opponent_history[move_i]
    prev_move = opponent_history[move_i-1]
    prev_prev_move = opponent_history[move_i-2]
    opponent_moves_count[prev_prev_move][prev_move][move] += 1
  last_move = opponent_history[-1] if len(opponent_history) > 0 else "R"
  before_last_move = opponent_history[-2] if len(opponent_history) > 1 else "R"
  return get_best_counter(max(opponent_moves_count[before_last_move][last_move],key=opponent_moves_count[before_last_move][last_move].get))


#Returns a guess based on the predicted move of the opponent.
#The predicted move is the one played the most after the last n moves.
def get_frequentist_guess_n(opponent_history,n):
  opponent_moves_count = {}
  for move_i in range(n,len(opponent_history)):
    prev_moves = opponent_history[move_i-n:move_i]
    prev_moves_string = functools.reduce(lambda x,y: x+y,prev_moves)
    last_move = opponent_history[move_i]
    #print(prev_moves_string)
    #print(last_move)
    opponent_moves_count.setdefault(prev_moves_string,{"R":0, "P":0, "S": 0})
    opponent_moves_count[prev_moves_string][last_move] += 1
  if len(opponent_history) >= n:
    last_n_moves = functools.reduce(lambda x,y: x+y,opponent_history[-n:])
  else:
    last_n_moves = functools.reduce(lambda x,y: x+y,["R" for i in range(n)])
  opponent_moves_count.setdefault(last_n_moves,{"R":0, "P":0, "S": 0})
  #print(opponent_moves_count)
  return get_best_counter(max(opponent_moves_count[last_n_moves],key=opponent_moves_count[last_n_moves].get))
