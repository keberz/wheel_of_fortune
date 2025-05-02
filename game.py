import json
import random
import time

vowel_cost = 250
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
vowels = 'AEIOU'

class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []
        
    def add_money(self, amt):
        self.prizeMoney += amt        
    
    def go_bankrupt(self):
        self.prizeMoney = 0

    def add_prize(self, prize):
        self.prizes.append(prize)
        
    def __str__(self):
        return f'{self.name} (${self.prizeMoney})'
    
class WOFHumanPlayer(WOFPlayer):
    def get_move(self, guessed):
        s = input(f"{self.name} has ${self.prizeMoney}\n\nGuess a letter, phrase, or type 'exit' or 'pass': ")
        return s

class WOFComputerPlayer(WOFPlayer):
    sorted_frequencies = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'
    
    def __init__(self, name, lvl):
        super().__init__(name)
        self.level = lvl
        
    def smart_coin_flip(self):
        if random.randint(1, 10) > self.level:
            return False
        else:
            return True
        
    def get_possible_letters(self, guessed):
        possible_letters = [char for char in letters if char not in guessed]
        if self.prizeMoney < vowel_cost:
            possible_letters = [char for char in possible_letters if char not in vowels]
        return possible_letters
    
    def get_move(self, guessed):
        print(f'{self.name} has ${self.prizeMoney}\n')

        possible_letters = self.get_possible_letters(guessed)
        index_letters = [char for char in self.sorted_frequencies if char in possible_letters]
        if not possible_letters:
            return 'pass'
        elif self.smart_coin_flip():
            return index_letters[-1]
        else:
            return random.choice(index_letters)

# Repeatedly asks the user for a number between min_value & max_value (inclusive)
def get_number_between(prompt, min_value, max_value):
    user_input = input(prompt) # ask the first time

    while True:
        try:
            n = int(user_input) # try casting to an integer
            if n < min_value:
                error_message = 'Must be at least {}'.format(min_value)
            elif n > max_value:
                error_message = 'Must be at most {}'.format(max_value)
            else:
                return n
        except ValueError: # The user didn't enter a number
            error_message = '{} is not a number.'.format(user_input)

        # If we haven't gotten a number yet, add the error message and ask again
        user_input = input('{}\n{}'.format(error_message, prompt))

# Spins the wheel of fortune wheel to give a random prize
def spin_wheel():
    with open("assets/wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)

# Returns a category & phrase (as a tuple) to guess
def get_random_category_and_phrase():
    with open("assets/phrases.json", 'r') as f:
        phrases = json.loads(f.read())

        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        return category, phrase.upper()

def obscure_phrase(phrase, guessed):
    """
    Given a phrase and a list of guessed letters, returns an obscured version
    Example:
        guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
        phrase:  "GLACIER NATIONAL PARK"
        returns> "_L___ER N____N_L P_RK"
    """
    rv = ''
    for s in phrase:
        if (s in letters) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv

def show_board(category, obscured_phrase, guessed):
    """Returns a string representing the current state of the game"""
    return """
Category: {}
Phrase:   {}
Guessed:  {}""".format(category, obscured_phrase, ', '.join(sorted(guessed)))

def request_player_move(player, guessed):
    while True: # we're going to keep asking the player for a move until they give a valid one
        time.sleep(0.1) # added so that any feedback is printed out before the next prompt

        move = player.get_move(guessed)
        move = move.upper() # convert whatever the player entered to UPPERCASE
        if move == 'EXIT' or move == 'PASS':
            return move
        elif len(move) == 1: # they guessed a character
            if move not in letters: # the user entered an invalid letter (such as @, #, or $)
                print('Guesses should be letters. Try again.')
                continue
            elif move in guessed: # this letter has already been guessed
                print('{} has already been guessed. Try again.'.format(move))
                continue
            elif move in vowels and player.prizeMoney < vowel_cost: # if it's a vowel, we need to be sure the player has enough
                    print('Need ${} to guess a vowel. Try again.'.format(vowel_cost))
                    continue
            else:
                return move
        else: # they guessed the phrase
            return move
       
def main(): 
    # Set up the game
    num_human = get_number_between('How many human players? ', 0, 10)
    
    # Create the human player instances
    human_players = [WOFHumanPlayer(input('Enter the name for human player #{} '.format(i+1))) for i in range(num_human)]
    num_computer = get_number_between('How many computer players? ', 0, 10)
    
    # If there are computer players, ask what level they should be. Create list of players
    if num_computer >= 1:
        level = get_number_between('What level for the computers? (1-10) ', 1, 10)
        computer_players = [WOFComputerPlayer('Computer {}'.format(i + 1), level) for i in range(num_computer)]
        players = human_players + computer_players
    else:
        players = human_players
    
    if len(players) == 0: # No players, no game :(
        print('We need players to play!')
        raise Exception('Not enough players')
    
    # GAME LOGIC CODE
    print('='*15)
    print('WHEEL OF PYTHON')
    print('='*15)
    print('')
    
    # category and phrase are strings.
    category, phrase = get_random_category_and_phrase()
    # guessed is a list of the letters that have been guessed
    guessed = []
    
    # player_index keeps track of the index (0 to len(players)-1) of the player whose turn it is
    player_index = 0
    
    # will be set to the player instance when/if someone wins
    winner = False
    
    while True:
        player = players[player_index]
        wheel_prize = spin_wheel()
    
        print('')
        print('-'*15)
        print(show_board(category, obscure_phrase(phrase, guessed), guessed))
        print('')
        print('{} spins...'.format(player.name))
        # time.sleep(1) # pause for dramatic effect!
        print('{}!'.format(wheel_prize['text']))
        # time.sleep(1) # pause again for more dramatic effect!
    
        if wheel_prize['type'] == 'bankrupt':
            player.go_bankrupt()
        elif wheel_prize['type'] == 'loseturn':
            pass # do nothing; just move on to the next player
        elif wheel_prize['type'] == 'cash':
            move = request_player_move(player, guessed)
            if move == 'EXIT': # leave the game
                print('Until next time!')
                break
            elif move == 'PASS': # will just move on to next player
                print('{} passes'.format(player.name))
            elif len(move) == 1: # they guessed a letter
                guessed.append(move)
    
                print('{} guesses "{}"'.format(player.name, move))
    
                count = phrase.count(move) # returns an integer with how many times this letter appears
                if count > 0:
                    if count == 1:
                        print("There is one {}".format(move))
                    else:
                        print("There are {} {}'s".format(count, move))
    
                    # Give them the money and the prizes
    
                    if move in vowels:
                        player.prizeMoney -= vowel_cost
    
                    else:  
                        player.add_money(count * wheel_prize['value'])
                        if wheel_prize['prize']:
                            player.add_prize(wheel_prize['prize'])
    
                    # check if all the letters have been guessed
                    if obscure_phrase(phrase, guessed) == phrase:
                        winner = player
                        break
    
                    continue # this player gets to go again
    
                else: # count == 0
                    print("There is no {}".format(move))
    
            else: # they guessed the whole phrase
                if move == phrase: # they guessed the full phrase correctly
                    winner = player
    
                    # Give them the money and the prizes
                    player.add_money(wheel_prize['value'])
                    if wheel_prize['prize']:
                        player.add_prize(wheel_prize['prize'])
    
                    break
                else:
                    print('{} was not the phrase'.format(move))
    
        # Move on to the next player (or go back to player[0] if we reached the end)
        player_index = (player_index + 1) % len(players)
    
    if winner:
        # In your head, you should hear this as being announced by a game show host
        print('{} wins! The phrase was {}'.format(winner.name, phrase))
        print('{} won ${}'.format(winner.name, winner.prizeMoney))
        if len(winner.prizes) > 0:
            print('{} also won:'.format(winner.name))
            for prize in winner.prizes:
                print('    - {}'.format(prize))
    else:
        print('Nobody won. The phrase was {}'.format(phrase))
        
main()