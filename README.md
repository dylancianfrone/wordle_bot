
# POMDP Wordle 

Note: This was created for Dylan Cianfrone's final project for George Mason University's CS 695 in Spring 2022.

I formulated Wordle as a Partially Observable MDP where the unknown state is the answer word and each word to guess is an action. The belief state, then, is 1/(number of possible answers based on already existing guesses) for all remaining possible answers, and 0 for all other answers. 

This initial implementation only allows the bot to guess words that are answers, even though the real Wordle list of allowed guesses is about 13000 words long. Even so, the performance is quite good: Total guesses of 8146 for an average of about 3.519 guesses per word. It fails 6 times.

It also plays on hard mode always. The reason for these limitations is that the policy tree gets absolutely massive with the entire library of guesses available as actions. By limiting the number of actions available at each state, I can take the policy tree from completely unreasonable to compute to the current situation, which takes some time certainly but is possible to actually run and observe. 

For the same reason, the starting word is hard-coded as SALET. I found that a good start like SALET ends up breaking the entire list of 2300 answer words into subtrees with a little under 100 words each. I can fully expand a policy tree of 100 words in about 15 seconds, so even doing this 100 times only takes about 30 minutes. If I were to try every starting word, the thing would never finish.

I'll be writing more about this later (when I write my project report), but I wanted there to be some explanation before I posted to the leaderboard.



