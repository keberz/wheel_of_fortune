# About

This project is a simplified version of the game Wheel of Fortune.

# Rules

There are `num_human` human players and `num_computer` computer players.
* Every player has some amount of money ($0 at the start of the game)
* Every player has a set of prizes (none at the start of the game)
* The goal is to accumulate money and prizes.

In each round of the game, the players try to guess a phrase. For example, suppose the phrase is "Whitney Houston's I Will Always Love You". 

Players see the category and an obscured version of the phrase where every alphanumeric character in the phrase starts out as hidden (using underscores: ``_``). For example:
* Category: **Artist & Song**
* Phrase: ``_______ _______'_ _ ____ ______ ____ ___``

Note that case (capitalization) does not matter

During their turn, a player spins the wheel to determine a prize amount and:
* If the wheel lands on a cash square, players may do one of three actions:
    1. **Guess any letter** that hasn't been guessed by typing a letter (a-z)
        * Vowels (a, e, i, o, u) cost $250 to guess and can't be guessed if the player does not have enough money. All other letters are "free" to guess
        * The player can guess any letter that hasn't been guessed and gets that cash amount for *every time* that letter appears in the phrase
        * If there is a prize, the user also gets that prize (in addition to any prizes they already had)
        * **Example: The user lands on $500 and guesses 'W'**
            * There are three W's in the phrase, so the player wins $1500
    2. **Guess the complete phrase** by typing a phrase (anything over one character that isn't *'pass'*)
        * If they are correct, they win the game
        * If they are incorrect, it is the next player's turn
    3. **Pass** their turn by entering `'pass'`
- If the wheel lands on **"lose a turn"**, the player loses their turn and the game moves on to the next player
- If the wheel lands on **"bankrupt"**, the player loses their turn *and* loses their money. However, they keep all the prizes they have won so far.

The round continues until the entire phrase is revealed (or one player guesses the complete phrase)

# Libraries

Python 3.9 or above. Run "game.py" to launch the game. 