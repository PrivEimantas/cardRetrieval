import PySimpleGUI as sg
import datetime, time,json,csv,os
import csv
import _csv
import numpy as np
import pandas as pd
import pickle

Learning_Alg_Layout = [
]

# User_Decks = [['Front1', 'Back1', 0,0,0, datetime.datetime(2020, 11, 2, 19, 0, 51, 922267)],
#               ['Front2', 'Back2', 0, 0, 0, datetime.datetime(2020, 11, 2, 19, 1, 0, 66117)]]

"""
                Question, Answer , delay in days, factor of points, interval for fail/hard/ok/easy 
"""
# User_Decks = [['Front1', 'Back1', datetime.datetime(2020, 11, 2, 19, 0, 51, 922267)],
#               ['Front2', 'Back2', datetime.datetime(2020, 11, 2, 19, 1, 0, 66117)]]

class CreateCard:
    def __init__(self):
        self.deck = [] # Initialise empty deck
        self.create_card() # Launch method


    def create_card(self):
        self.layout = [ # Update layout
            [sg.Text('Submit your flash cards here')],
            [sg.Text('Front:'),sg.Input('',key='front')],
            [sg.Text('Back:'),sg.Input('',key='back')],
            [sg.Text('Deck Name:'), sg.Input('',key='deck_name')],
            [sg.Submit('Enter card',key='submit_card')],
            [sg.Submit('Finished deck',key='submit_deck')]
        ]
        window_display = sg.Window('REVISION', self.layout)
        while True:
             # Continue checking for any action from user
            event, value = window_display.read()  # Set up the actual window
            if event in ('Exit', None):  # If clicks 'X', proceed to quit
                window_display.close()
                break
            if event == 'submit_card':
                self.card = [] # New card, append values of front and back along with current time
                self.front = str(value['front'])
                self.back = str(value['back'])
                self.deck_name = str(value['deck_name'])
                self.card.append(self.front)
                self.card.append(self.back)
                self.card.append(datetime.datetime.now())
                self.card.append(datetime.datetime.now())
                self.deck.append(self.card)

            if event == 'submit_deck':
                self.deck_name = str(value['deck_name'])
                slash = '\ ' # Special character, split to use
                slash.split(" ")
                with open(r'C:\Users\Eimantas\Desktop\A Level CS Stuff\Project\Learning_Alg'+ slash + self.deck_name + '.data','wb') as file:
                    pickle.dump(self.deck,file) # Save as a pickle data file
                self.deck = [] # New deck

CreateCard()




class Revision:
    def __init__(self):
        #self.user_decks = [['Front1', 'Back1',
                           #  datetime.datetime(2020, 11, 2, 19, 0, 51, 922267),
                           #  datetime.datetime(2020, 11, 2, 19, 0, 51, 922267),
                           #  200],
                           # ['Front2', 'Back2',
                           #  datetime.datetime(2020, 11, 2, 19, 1, 0, 66117),
                           #  datetime.datetime(2020, 11, 2, 19, 1, 0, 66117),
                           #  200]]
        # STRUCTURE: QUESTION, ANSWER, PREVIOUS DATE, DATE DUE, FACTOR

        self.deck = None  # Declare variables to be accessed everywhere
        self.m0 = None
        self.m4 = None
        self.m = None
        self.layout = None

        self.set_up() # Start process


    def set_up(self):
        self.layout = [  # Present starting information which is to retrieve data from user
            [sg.Text('Select the deck of cards you want to use for a test')],
            [sg.InputText(key='deck'), sg.FileBrowse('Select Deck')],
            [sg.Text('Select the interval parameter to change output times, interval modifier')],
            [sg.Input(key='m')],
            [sg.Text('Select the interval parameter to change output times, easy modifier')],
            [sg.Input(key='m4')],
            [sg.Text('Select the interval parameter to change output times, hard modifier ')],
            [sg.Input(key='m0')],
            [sg.Submit(key='submit')]
        ]

        while True:
            window_display = sg.Window('REVISION', self.layout)  # Continue checking for any action from user
            event, value = window_display.read()  # Set up the actual window
            if event in ('Exit', None):  # If clicks 'X', proceed to quit
                window_display.close()
                break
            if event == 'submit':
                self.user_decks = self.retrieveDeck(value['deck'])  # Fetch values and update
                self.m = float(value['m'])
                self.m4 = float(value['m4'])
                self.m0 = float(value['m0'])
                window_display.close()  # Close current window and start main
                self.run_main()

    def display_question(self):
        window_display = sg.Window('REVISION', self.layout)
        print(self.user_decks)
        while True:
            # Continue checking for any action from user
            event, value = window_display.read()  # Set up the actual window
            if event in ('Exit', None):  # If clicks 'X', proceed to quit
                break
            if event == 'submit':
                window_display.close()  # User picked answer, display card
                break
            if event == 'ok':
                break

    def display_answer(self, i):
        window_display = sg.Window('REVISION', self.layout)
        duration_hours_delay = (datetime.datetime.now() - self.user_decks[i][3]).total_seconds()  # Delay between due and now in days
        duration_hours_delay = duration_hours_delay / 3600 # In seconds, so divide by 3600 to get hours
        interval = (self.user_decks[i][3] - self.user_decks[i][2]).total_seconds()
        interval = interval / 3600  # Interval length in hours
        i1 = self.m0 * interval # No recall new interval
        i2 = max(interval + 1, (interval + duration_hours_delay / 64) * 1.2 * self.m) # Hard recall interval
        i3 = max(i2 + 6, (interval + duration_hours_delay / 2) * (self.user_decks[i][4] / 1000) * self.m / 24)  # Ok recall
        i4 = max(i3 + 18, (interval * duration_hours_delay) * (self.user_decks[i][4] / 100) * self.m * self.m4 )  # Easy recall
        self.user_decks[i][2] = datetime.datetime.now()  # Update review time

        while True:
            # Continue checking for any action from user
            event, value = window_display.read()  # Set up the actual window
            if event in ('Exit', None): break  # If clicks 'X', proceed to quit

            if event == 'no_recall':  # User struggles to recall, fetch again soon
                self.user_decks[i][3] = datetime.datetime.now() + datetime.timedelta(hours=i1)  # Update interval
                self.user_decks[i][4] = max(1,self.user_decks[i][4] - 200 ) # Decrement but never below 1
                print(self.user_decks[i])
                window_display.close()  # Exit when done
            if event == 'hard_recall':  # Difficult to recall, but not as much, slightly longer
                self.user_decks[i][3] = datetime.datetime.now() + datetime.timedelta(hours=i2)
                self.user_decks[i][4] = max(1, self.user_decks[i][4] - 150)  # Decrement but never below 1 for factor
                print(self.user_decks[i])
                window_display.close()
            if event == 'ok_recall':  # Recall later since easier
                self.user_decks[i][3] = datetime.datetime.now() + datetime.timedelta(hours=i3)
                print(self.user_decks[i])
                window_display.close() # No factor change
            if event == 'easy_recall':  # Easiest, look later
                self.user_decks[i][3] = datetime.datetime.now() + datetime.timedelta(hours=i4)
                self.user_decks[i][4] = max(1, self.user_decks[i][4] + 50)  # Increase factor
                print(self.user_decks[i])
                window_display.close()

    def run_main(self):
        deck_complete = False  # Set to true since assuming it is incomplete
        while deck_complete == False:
            i = 0  # Counter to track each card
            deck_complete = True  # Assuming that there will be not be a card that needs changing
            while i != len(self.user_decks):
                if self.user_decks[i][3] <= datetime.datetime.now():  # If a card needs to be reviewed
                    deck_complete = False  # Found card that needs reviewing, so change it
                    self.layout = [  # Update layout with question display and button
                        [sg.Text(self.user_decks[i][0])], [sg.Submit('Show answer', key='submit')]
                    ]
                    self.display_question()  # Display with GUI
                    self.layout = [  # User answered, so update layout to show answer
                        [sg.Text(self.user_decks[i][0])],
                        [sg.Text(self.user_decks[i][1])],
                        [sg.Button('No recall', key='no_recall'),
                         sg.Button('Hard', key='hard_recall'),
                         sg.Button('Okay', key='ok_recall'),
                         sg.Button('Easy', key='easy_recall')]
                    ]
                    self.display_answer(i)  # Show answer
                    print(self.user_decks[i][0], self.user_decks[i][2])
                i += 1

        self.layout = [
            [sg.Text('No cards available')],

        ]


    def retrieveDeck(self, deck):
        with open(r'' + deck, 'rb') as file:  # Read file selected by user as file
            item = pickle.load(file)
        return item


if __name__ == "__main__":
    app = Revision()
# 
