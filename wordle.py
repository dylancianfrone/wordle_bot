import random
from colorama import init, Fore, Style
class wordle:

    GREEN = Fore.GREEN#'\033[92m'
    YELLOW = Fore.YELLOW#'\033[93m'
    DEFAULT = Style.RESET_ALL#'\033[0m'

    #_answer :          the answer of this wordle
    #remaining_guesses: the number of guesses remaining
    #guess_history:     all guesses taken, of the form ("word", "feedback")
    #allowed_guesses:   all words allowed to be played
    #allowed_answers:   all words allowed to be selected as an answer
    #possible_guesses:  all guesses that fit the current pattern required based on guesses
    #possible_answers:  all answers that are possible using the given guesses

    #feedback_results: {(guess, answer): feedback}

    #if answers is None, answers and guesses lists are the same
    #if answer_index >= 0, the answer is initialized as that index. Otherwise, it's random.
    def __init__(self, guesses, answers=None, answer_index=-1, num_guesses=6):
        init()

        self.allowed_guesses = guesses.copy()
        self.allowed_answers = guesses.copy() if not answers else answers.copy()
        self.possible_guesses = guesses.copy()
        self.possible_answers = self.allowed_answers.copy()

        selected_answer = None
        if answer_index < 0:
            selected_answer = random.choice(self.allowed_answers)
        else:
            selected_answer = self.allowed_answers[answer_index]

        self._answer = selected_answer
        self.remaining_guesses = num_guesses
        self.guess_history = []
        self.feedback_results = {}

    #returns feedback of the form 'B/Y/G' * 5
    #B = Black  = letter in that index does not appear in the word
    #Y = Yellow = letter in that index appears, but not in that location
    #G = Green  = letter in that index appears in that index
    #A character only turns yellow if the correct character does not already have a green in it.
    #Eg. Answer = Maple, Guess = There; return = "BBBBG" not "BBYBG"
    def guess(self, word, print_feedback=False):
        word = word.upper()
        if self.remaining_guesses<=0:
            return "ULOST"
        if word not in self.allowed_guesses or self.remaining_guesses <= 0:
            return "XXXXX"

        feedback = self.get_feedback(word, self._answer)

        self.guess_history.append((word, feedback))
        self.remaining_guesses -= 1
        self.update_possible(word, feedback)
        if print_feedback:
            self.print_guess_in_color(word, feedback)

        return feedback

    def get_feedback(self, word, answer):
        if (word, answer) in self.feedback_results:
            return self.feedback_results[(word, answer)]
        feedback = ["X", "X", "X", "X", "X"]
        ans = [answer[i] for i in range(5)]
        #add G
        for i in range(5):
            if word[i] == ans[i]:
                feedback[i] = "G"
                ans[i] = "_"
        #add Y and B
        for i in range(5):
            if feedback[i] == "X":
                f = ans.index(word[i]) if word[i] in ans else -1
                if f == -1:
                    feedback[i] = "B"
                else:
                    feedback[i] = "Y"
                    ans[f] = "_"
        feedback_s = "".join(feedback)
        self.feedback_results[(word, answer)] = feedback_s
        return feedback_s

    #Updates the list of possible guesses and answers based on this guess->feedback exchange.
    def update_possible(self, guess, feedback):
        #possible_guesses is maintained even though allowed_guesses is the checked one because this would allow for me to add hard mode easier later.
        self.possible_guesses = [x for x in self.possible_guesses if self.is_possible(guess, feedback, x)]
        self.possible_answers = [x for x in self.possible_answers if self.is_possible(guess, feedback, x)]

    #Returns false if guess->feedback makes x an impossible answer. True otherwise.
    def is_possible(self, guess, feedback, x):
        return self.get_feedback(guess, x) == feedback

    def print_guess_in_color(self, guess, feedback):
        pr = ""
        for i in range(5):
            if feedback[i] == "B":
                pr+=self.DEFAULT+guess[i]
            elif feedback[i] == "Y":
                pr+=self.YELLOW+guess[i]
            else:
                pr+=self.GREEN+guess[i]
        pr+=self.DEFAULT
        print(pr)

    def get_leaderboard_string(self):
        str = ""
        for guess in self.guess_history:
            if str != "":
                str+=","
            str += guess[0].lower()
        return str

    def reset(self, answer_index=-1, num_guesses=6):
        self.possible_guesses = self.allowed_guesses.copy()
        self.possible_answers = self.allowed_answers.copy()
        self._answer = random.choice(self.allowed_answers) if answer_index<0 else self.allowed_answers[answer_index]
        self.remaining_guesses = num_guesses
        self.guess_history = []
        self.feedback_results = {}
