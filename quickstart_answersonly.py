from wordle import wordle
from policy_tree import policy_tree
import sys
#import numpy as np
from tqdm import tqdm
import random

default_path = "data\\"
default_guesses = "guesses.txt"
default_answers = "answers.txt"

CORRECT_ANSWER = 100
GAMMA = 0.5
BAD_GUESS_PENALTY = -10

starter = "SALET"

value_actions = {}

def main():
    (guesses, answers) = open_files()
    w = wordle(init_list_from_file(guesses),init_list_from_file(answers))
    possible_guesses = w.possible_guesses
    possible_answers = w.possible_answers
    initial_belief = [1/len(possible_answers) for a in possible_answers]
    policy = policy_tree(possible_answers, starter)
    policy.create_child_nodes(w)
    policy.value = get_value_of_tree(w, policy)
    #print(policy)
    evaluate_performance(w, policy)

def evaluate_performance(w, policy):
    history = []
    leaderboard = []
    errorlog = []
    successes = 0
    failures = 0
    errors = 0
    for i in tqdm(range(len(w.allowed_answers))):
        num_guesses = 0
        feedback = "BBBBB"
        cur_policy = policy
        w.reset(i)
        while feedback != "GGGGG":
            feedback = w.guess(cur_policy.action, False)
            if feedback == "ULOST":
                failures+=1
                break
            elif feedback == "XXXXX":
                errors+=1
                errorlog.append( (cur_policy.action, w._answer) )
            cur_policy = cur_policy.children[feedback]
            num_guesses+=1
        leaderboard.append(w.get_leaderboard_string()+"\n")
        successes +=1
        history.append(num_guesses)
    print(f"Errors: {errors}")
    if errors>0:
        print(errorlog)
    print(f"Number of failures: {failures}")
    print(f"Average guesses: {sum(history)/successes}")
    for i in range(1, 7):
        print(f"Number of {i}s: {len([x for x in history if x==i])}")
    output_file = open("output_a.txt", "w")
    output_file.writelines(leaderboard)
    output_file.close()

def decide_action(w, policy):
    #policy_tree is the root of a policy tree
    #policy_tree has    possibilities = list of different actions we can take
    #                   belief = belief[i] = belief that the answer is the word at possibilities[i]
    #                   action = currently undecided action to take at that node
    #                   height = the height of the node (nodes will not be expanded after 0 height)
    # So, this function needs to get a set of possibilities, decide what action is best, and then decide_action for the children.
    best_value = -1000
    best_tree = None
    for a in policy.possibilities:
        #create a policy_tree with this action
        #find its value
        new_tree = policy_tree(policy.possibilities, a, policy.height)
        new_tree.create_child_nodes(w)
        new_tree.value = get_value_of_tree(w, new_tree)
        if new_tree.value > best_value:
            best_value = new_tree.value
            best_tree = new_tree
    if not best_tree:
        print("Decide_action recieved: \n")
        print(policy)
        print("Returning NONE\n----")
    return best_tree

def get_value_of_tree(w, policy):
    #we have a policy_tree with an action and we need to decide the value of that action from the belief state defined in the node
    #we have to do this by expanding the entire subtree.
    #policy_tree.children = {observation: policy_tree}
    #for each of the policy_trees in children, decide_action of those which will call get_value etc etc.
    #decide_action also initializes policy_tree.value so by the time we get back to this function, we can just add up the probability of each outcome*child.value
    value = 0
    if len(policy.possibilities) == 1:
        #If we only have 1 possibility, then it *should* be guaranteed to be the correct answer.
        return CORRECT_ANSWER
    if len(policy.possibilities) == 0:
        return 0
    for obs in policy.children:
        new_node = decide_action(w, policy.children[obs])
        policy.children[obs] = new_node
        value+=policy.children[obs].value
    return CORRECT_ANSWER/len(policy.possibilities) + value*GAMMA


#this was just really used for testing
def manual_game(w):
    n = ""
    print("PYWORDLE")
    while True:
        n = input()
        if n.upper() == "QUIT":
            break
        if n.upper() == "ANSWER":
            print(w._answer)
        f = w.guess(n, True)
        if f == "XXXXX":
            print("INVALID")

#uppercase and remove \n from all words in list
def init_list_from_file(f):
    return [w.upper()[:-1] for w in f]

#open either default files or those specified in command line arguments
def open_files():
    argc = len(sys.argv)
    guesses_path = default_path+default_guesses if argc!=3 else sys.argv[1]
    answers_path = default_path+default_answers if argc!=3 else sys.argv[2]
    if argc!=3:
        print(f"Improper number of arguments provided. Using default filepaths {guesses_path} and {answers_path}.")
    else:
        print(f"Opening {guesses_path} and {answers_path} for guesses and answers.")

    guesses = open(guesses_path)
    answers = open(answers_path)
    if guesses and answers:
        return (guesses, answers)
    else:
        print("Error opening files. Terminating...")
        quit()

if __name__== "__main__":
    main()
