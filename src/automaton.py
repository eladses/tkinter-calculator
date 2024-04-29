#!/usr/bin/env python3

class Automaton:
    Q=[]
    Sigma=[]
    delta={}
    q0='q0'
    F=[]

    q=''

    def __init__(self,Q,Sigma,delta,q0='q0',F=[]):
        self.Q=Q
        self.Sigma=Sigma
        self.delta=delta
        self.q0=q0
        self.F=F

    def check_word(self,s):
        def check_word(s):
            if (s==''):
                return self.q in self.F
            else:
                return check_char(s[0]) and check_word(s[1:])

        # check the next char in the string
        def check_char(c):

            if (self.q,c) in self.delta:                #check if delta heve this key
#                print(self.q, c, self.delta[(self.q, c)])          #if you want to see the Automaton actions
                self.q = self.delta[(self.q,c)]         #move to the next q
                return True
            else:                                       #if delta dont have the transition return false
                return False

        self.q=self.q0                                  #befor starting to check, put q0 as the start
        return check_word(s)
