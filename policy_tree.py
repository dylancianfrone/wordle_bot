class policy_tree:

    #action:    action to take (word to guess)
    #children:  {observation: child}

    def __init__(self, possibilities, action=None, height=6):
        self.action = action
        self.children = {}
        self.possibilities = possibilities
        self.belief = [1/len(possibilities) for p in possibilities]
        self.height = height
        self.value = 0
    #create child nodes - overwrites any previous ones.
    #child nodes have not been expanded.
    def create_child_nodes(self, w):
        if self.height <= 0:
            return
        self.children = {}
        for p in self.possibilities:
            feedback = w.get_feedback(self.action, p)
            if feedback not in self.children:
                self.children[feedback]=policy_tree([x for x in self.possibilities if w.is_possible(self.action, feedback, x)], None, self.height-1)
                if len(self.children[feedback].possibilities) == 0:
                    print(f"Problem - {feedback} from {self.action} on {p} for \n{self.possibilities}\n")
                    print(w.is_possible(self.action, feedback, p))

    def __repr__(self):
        st = ""
        st+=self.action+"\n" if self.action else "[No Action]\n"
        st+="Possibilities: "+str(self.possibilities[:10])+ ("...\n" if len(self.possibilities)>10 else "\n")
        st+="Children: "+str([o+": "+self.children[o].action+", " if self.children[o] and self.children[o].action else o+": [No Action], " for o in self.children])+"\n" if self.children else "[No Children]\n"
        return st
