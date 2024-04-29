#!/usr/bin/env python3

from tkinter import *
from enum import Enum
import math, re
import automaton

class Action(Enum):         #action enum
    add='+'
    sub='-'
    mul='*'
    div='/'
    pow='^'
    eql='='

class Parenthesis(Enum):    #parenthesis enum
    left='('
    right=')'




class Calculator:

    root=None
    main_canvas=None

    ans=0                       #the last answer saved here

    equation_label=None
    equation=''                 #the equation
    rusolut_label=None

    automaton_checker =None     #the automaton to check equation syntax

    def __init__(self):


        self.root = Tk()                                                                    #create the root and the main canvas
        self.main_canvas = Canvas(self.root, bg="yellow", height=28 * 6*2, width=28 * 5*2)

        self.root.geometry("280x338")           #set the size of the window
        self.root.resizable(0, 0)               #make the window size unchangeable
        self.root.title('Calculator')             #change the window name

        self.set_label_canvas()                 #set the labels and buttons
        self.set_clear_button_canvas()
        self.set_button_canvas()
        self.set_action_button_canvas()


        Q = ['q0', 'q1', 'q2']              #create the automaton
        Sigma = ['n', 'a', '(', ')']
        delta = {
            ('q0', 'n'): 'q1',
            ('q0', '('): 'q0',
            ('q1', 'n'): 'q1',
            ('q1', 'a'): 'q0',
            ('q1', ')'): 'q2',
            ('q2', 'a'): 'q0',
            ('q2', ')'): 'q2'
        }
        F = ['q1', 'q2']
        self.automaton_checker=automaton.Automaton(Q,Sigma,delta,q0='q0',F=F)

        self.main_canvas.pack()         #put the canvas on the window
        self.root.mainloop()            #start the window


    def set_button_canvas(self):
        button_canvas = Canvas(self.main_canvas, bg="gray", height=28 * 4*2, width=28 * 3*2)        #create numbers button's canvas


        # button .
        func=self.num_button_down_builder('.')
        b = Button(button_canvas, text='.', command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        button_canvas.create_window((4 + 28 * 0)*2, (3 + 3 * 28)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-.>", func)

        # button 0
        func = self.num_button_down_builder(0)
        b = Button(button_canvas, text=str(0), command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        button_canvas.create_window((3 + 28 * 1)*2, (3 + 3 * 28)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-0>", func)


        # button ans
        b = Button(button_canvas, text='ans', command=self.ans_button_down,font=('',9*2))
        b.configure(width=3, height=1, activebackground="#33B5E5", relief=RAISED)
        button_canvas.create_window((28 * 2)*2, (3 + 3 * 28)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-a>", self.ans_button_down)

        for i in range(1, 10):  # buttons 1-9
            func = self.num_button_down_builder(i)
            b = Button(button_canvas, text=str(i), command=func,font=('',9*2))
            b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
            button_canvas.create_window((4 + 28 * ((i - 1) % 3))*2, (3 + int((9 - i) / 3) * 28)*2, anchor=NW, window=b)
            self.root.bind("<KeyPress-"+str(i)+">", func)

        button_canvas.place(x=0, y=56*2)      #set this canvas on the main canvas

    #number button down func builder
    def num_button_down_builder(self,num):
        def num_button_down(event=None):
            self.apdate_equation_label(str(num))
        return num_button_down

    #answer button down func
    def ans_button_down(self,event=None):
        self.apdate_equation_label(str(self.ans))

    def set_action_button_canvas(self):
        action_button_canvas = Canvas(self.main_canvas, bg="orange", height=28*4*2, width=28*2*2)   #create action button's canvas

        # button (
        func = self.parenthesis_button_down_builder(Parenthesis.left)
        b = Button(action_button_canvas, text="(", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        action_button_canvas.create_window(4*2,3*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-(>", func)

        # button )
        func = self.parenthesis_button_down_builder(Parenthesis.right)
        b = Button(action_button_canvas, text=")", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        action_button_canvas.create_window((4+28)*2,3*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-)>", func)

        # button +
        func=self.action_button_down_builder(Action.add)
        b = Button(action_button_canvas, text="+", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        action_button_canvas.create_window(4*2,(3+28 *1)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-+>", func)

        # button -
        func = self.action_button_down_builder(Action.sub)
        b = Button(action_button_canvas, text="-", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        action_button_canvas.create_window((4+28)*2,(3+28 *1)*2, anchor=NW, window=b)
        self.root.bind("<minus>", func)

        # button *
        func = self.action_button_down_builder(Action.mul)
        b = Button(action_button_canvas, text="*", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        action_button_canvas.create_window(4*2,(3+28 *2)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-*>", func)

        # button /
        func = self.action_button_down_builder(Action.div)
        b = Button(action_button_canvas, text="/", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        action_button_canvas.create_window((4+28)*2,(3+28 *2)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-/>", func)

        # button =
        func = self.eql_button_down
        b = Button(action_button_canvas, text="=", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED,bg="gray")
        action_button_canvas.create_window(4*2,(3+28 *3)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-=>", func)
        self.root.bind("<Return>", func)

        # button ^
        func = self.action_button_down_builder(Action.pow)
        b = Button(action_button_canvas, text="^", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        action_button_canvas.create_window((4+28)*2,(3+28 *3)*2, anchor=NW, window=b)
        self.root.bind("<KeyPress-^>", func)

        action_button_canvas.place(x=84*2, y=56*2)      #set this canvas on the main canvas

    #action button down func builder
    def action_button_down_builder(self,action):
        def action_button_down(event=None):
            self.apdate_equation_label(action.value)
        return action_button_down

    #action button down
    def eql_button_down(self,event=None):

        #recursive function to solve the equation
        def main_solver(s):
            i = s.find('(')
            if (i == -1):       #if s dont have (, that means that you can solve it
                return sovle(s)
            else:               #else took the things between '(...)' and do main_solver on '...'
                l = 0
                r = 0
                for j in range(len(s)):
                    if (s[j] == '('):
                        l += 1
                    elif (s[j] == ')'):
                        r += 1
                    if (l > 0 and l == r):          #if you find the ')' of the first '(', do main_solver of the inside
                        sul=main_solver(s[i + 1:j])
                        if(sul==False):
                            return False
                        return main_solver(s[0:i] + str(sul) + s[j + 1:len(s) + 1])     #return the answer of what was befor the (), between and after


        def check_parenthesis_appirence(s):         #check if the parenthesis appirence are legal
            l = 0
            r = 0
            for i in range(len(s)):
                if (s[i] == '('):
                    l += 1
                elif (s[i] == ')'):
                    r += 1

                if (l < r):
                    return False
            if (l != r):
                return False
            return True

        def sovle(s):               #solve equation withuot parenthesis
            if(s==''):              #if you have nothing to sovle, dont solve it...
                return False
            is_last_was_action = True
            actions = []
            if (s[0] == '-'):
                s = '#' + s[1:len(s) + 1]
            for i in range(len(s)):
                for action in Action:
                    if s[i] == action.value:
                        actions.append(action)
                        if (i + 1 < len(s) and s[i + 1] == '-'):
                            s = s[0:i + 1] + '#' + s[i + 2:len(s) + 1]

            s = re.split('\\+|-|\\*|/|\\^', s)    #save the sine of the number ('-')
            for i in range(len(s)):
                s[i] = s[i].replace("#", "-")
            i = 0

            s[i] = float(s[i])
            while i != len(actions):        #calculate pow actions
                s[i + 1] = float(s[i + 1])

                if (actions[i] == Action.pow):
                    s[i] = math.pow(s[i], s[i + 1])
                    s.pop(i + 1)
                    actions.pop(i)
                else:
                    i += 1
            i = 0
            while i != len(actions):        #calculate mul/sub actions
                s[i + 1] = float(s[i + 1])
                if (actions[i] == Action.mul):
                    s[i] = s[i] * s[i + 1]
                    s.pop(i + 1)
                    actions.pop(i)
                elif (actions[i] == Action.div):
                    if (s[i + 1] == 0):
                        return  False
                    s[i] = s[i] / s[i + 1]
                    s.pop(i + 1)
                    actions.pop(i)
                else:
                    i += 1

            i = 0
            while i != len(actions):            #calculate add/sub actions
                if (actions[i] == Action.add):
                    s[i] = s[i] + s[i + 1]
                    s.pop(i + 1)
                    actions.pop(i)
                elif (actions[i] == Action.sub):
                    s[i] = s[i] - s[i + 1]
                    s.pop(i + 1)
                    actions.pop(i)
                else:
                    i += 1

            if (math.modf(s[0])[0] == 0):       #if there is nothing behide the '.', the dont save it
                s[0] = int(s[0])

            return s[0]

        #send to the automaton to chekcing the syntax
        def automaton_chekc(s,automaton_checker):

                #replace evry action with 'a' and number with 'n' for the chekc
            if (s[0] == '-'):
                s = 'n' + s[1:len(s) + 1]
            for i in range(len(s)):
                for action in Action:
                    if s[i] == action.value and i + 1 < len(s) and s[i + 1] == '-':
                        s = s[0:i + 1] + 'n' + s[i + 2:len(s) + 1]
            s = s.replace('.', 'n')
            for i in range(10):
                s = s.replace(str(i),'n')
            for a in Action:
                s = s.replace(a.value, 'a')
            return automaton_checker.check_word(s)      #the check


            #send to checks
        if (not check_parenthesis_appirence(self.equation) or not automaton_chekc(self.equation,self.automaton_checker)):
            self.rusolut_label.configure(text="Error")
            self.resat_equation_label()
            return

            #calculate
        try:
            ans= main_solver(self.equation)
        except OverflowError:                   #for to big numbers
            ans=False

        if(ans==False):
            self.rusolut_label.configure(text="Error")
            self.resat_equation_label()
            return

            #present
        self.ans=ans
        self.rusolut_label.configure(text=ans)
        self.resat_equation_label()

    #parenthesis button down func builder
    def parenthesis_button_down_builder(self, side):
        def parenthesis_button_down(event=None):
            self.apdate_equation_label(side.value)
        return parenthesis_button_down

    #set clear and backspace buttons
    def set_clear_button_canvas(self):
        clear_button_canvas = Canvas(self.main_canvas, bg="green", height=28*2*2, width=28*2)

        # button ace
        func = self.clear_button_down
        b = Button(clear_button_canvas, text="ac", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        clear_button_canvas.create_window(4*2,3*2, anchor=NW, window=b)
        self.root.bind("<Delete>", func)

        # button backspace
        func=self.del_button_down
        b = Button(clear_button_canvas, text="del", command=func,font=('',9*2))
        b.configure(width=2, height=1, activebackground="#33B5E5", relief=RAISED)
        clear_button_canvas.create_window(4*2,(3+28)*2, anchor=NW, window=b)
        self.root.bind("<BackSpace>", func)

        clear_button_canvas.place(x=112*2, y=0)

    #clear button down
    def clear_button_down(self,event=None):
        self.equation=''
        self.resat_equation_label()

    #backspace button down
    def del_button_down(self,event=None):
        self.equation=self.equation[0:len(self.equation)-1]
        self.equation_label.configure(text=self.equation)

    #set label canvas
    def set_label_canvas(self):
        label_canvas = Canvas(self.main_canvas, bg="white", height=28*2*2, width=28*4*2)

        #equation label
        l = Label(label_canvas, text="0",fg="gray",font=('',9*2),bg="white")
        label_canvas.create_window(3*2,5*2, anchor=NW, window=l)
        self.equation_label=l

        #resolut label
        l = Label(label_canvas, text="0",fg="black",bg="white",font=('',13*2),anchor='se')
        label_canvas.create_window((24*3)*2,(5+38)*2, window=l)

        self.rusolut_label = l

        label_canvas.place(x=0, y=0)

    #apdate equation label
    def apdate_equation_label(self,s):
        self.equation += s
        self.equation_label.configure(text=self.equation)

    #resat equationlabel
    def resat_equation_label(self):
        self.equation = ''
        self.equation_label.configure(text=self.equation)

Calculator()        #start calculator
