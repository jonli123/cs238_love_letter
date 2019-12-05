from game import Game
from lambda_player import LambdaPlayer
import copy
from random import random
import numpy as np

numGenerations = 10
generation_size = 128
keep_elite = generation_size//8
lambda_names=['g2', 'g4', 'g5', 'g7', 'b2', 'b4', 'b5', 'b6', 'b7', 'p2', 'p6']
games_per_round = 100

mutation = 0.8
random_children = generation_size//8

def make_generation(elite):    
    new_gen = copy.copy(elite)
    rand_kids = [[random() for i in range(len(lambda_names))] for i in range(random_children)]
    new_gen = new_gen + rand_kids
    while(len(new_gen) < generation_size):
        np.random.shuffle(elite)
        for i in range(0, len(elite)-1, 2):
            pairents = list(zip(elite[i], elite[i+1]))

            mix = [np.random.choice(pair) for pair in pairents]
            if random() < mutation:
                mix[np.random.randint(0,len(mix))] = random()
            new_gen.append(mix)

            avg = [np.average(pair) for pair in pairents]
            if random() < mutation:
               avg[np.random.randint(0,len(mix))] = random()
            new_gen.append(avg)
    return new_gen

#helper does a game given two lambda dictionaries
def do_game(lam0, lam1):   
    deck = Card.shuffle_deck()
    player0 = LambdaPlayer(0, deck[0],2, lam0)
    player1 = LambdaPlayer(0, deck[0],2, lam1)
    deck = deck[2:]
    players = [player0,player1]
    g = Game(deck,players)
    return g.simulate()

#takes a generation, does a round robin tournament
#returns top num_elite members, runs in O(n^2)
def round_robin(generation, num_elite):
    gwins = [0 for g in range(len(generation))]
    for g0 in range(len(generation)):
        for g1 in range(len(generation)):
            lam0 = dict(zip(lambda_names, generation[g0]))
            lam1 = dict(zip(lambda_names, generation[g1]))
            wins = [0, 0]
            for i in range(games_per_round):
                wins[do_game(lam0, lam1)] += 1
            gwins[g0] += wins[0]
            gwins[g1] += wins[1]
    l = list(zip(gwins, range(len(gwins))))
    l.sort()
    elite_i = l[-num_elite:]
    elite = [generation[i] for x, i in elite_i]
    return elite

#takes a generation, does a bracket tournament
#returns top num_elite members
def tournament(generation, num_elite):
    next_round = copy.copy(generation)
    while(len(next_round) > keep_elite):
        prev_round = next_round
        next_round = []
        for g0 in range(0, len(prev_round), 2):
            g1 = g0 + 1
            if g1 >= len(prev_round):
                g_next.append(prev_round[g0]) #they get a bye
            else:
                lam0 = dict(zip(lambda_names, prev_round[g0]))
                lam1 = dict(zip(lambda_names, prev_round[g1]))
                wins = [0, 0]
                for i in range(games_per_round):
                    wins[do_game(lam0, lam1)] += 1
                    wins[int(not do_game(lam1, lam0))] += 1
                if wins[0] > wins[1]:
                    next_round.append(prev_round[g0])
                else:
                    next_round.append(prev_round[g1])
    return next_round

gen = [[random() for l in lambda_names] for i in range(generation_size)]
for i in range(numGenerations):
    #elite = round_robin(gen, keep_elite)
    elite = tournament(gen, keep_elite)
    gen = make_generation(elite)

#best = roud_robin(gen, keep_elite)
best = tournament(gen, 8)
for b in best:
    print([round(x, 2) for x in b])