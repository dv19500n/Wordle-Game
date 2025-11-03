import json
import random
import pandas as pd
from datetime import datetime
f=open('wordle_no_dupes.json')
info= json.load(f)
f.close()
black= '\033[40m'
green = '\033[42m'
yellow = '\033[43m'
game_data={'timestamp':[],'guess':[],'attempt_number':[],'correct_letters':[],'is_correct':[]}
def record_guess(guess, attempt,target):
    game_data['timestamp'].append(datetime.now())
    game_data['guess'].append(guess)
    game_data['attempt_number'].append(attempt)
    game_data['correct_letters'].append(sum(1 for g in guess if g in target))
    game_data['is_correct'].append(guess==target)
def save_analytics():
    df=pd.DataFrame(game_data)
    df.to_csv('wordle_analytics.csv', index=False)
    print("\nGame data saved to wordle_analytics.csv")
word= random.choice(info)
tries=0
while tries !=6:
    def background(word):
        for letters in word:
            for letter in letters:
                print(letter, end='')
    word_guess=[]
    guess=input(f'\nGuess: ')
    if guess not in info:
        print("Word not found")
    elif guess == word:
        for i in range(5):
            if guess[i] ==word[i]:
                word_guess.append([green, guess[i]])
        word_guess.append([black])
        record_guess(guess,tries+1, word)
        background(word_guess)
        print('\nYou got it')
        save_analytics()
        break
    elif guess in info:
        for i in range(5):
            if guess[i] ==word[i]:
                word_guess.append([green, guess[i]])
            elif guess[i] in word:
                word_guess.append([yellow, guess[i]])
            else:
                word_guess.append([black,guess[i]])
        word_guess.append([black])
        record_guess(guess,tries+1, word)
        tries+=1
        background(word_guess)
if tries == 6:
    record_guess("", 6,word)
    save_analytics()
    print(f'\nThe word was: {word}')
