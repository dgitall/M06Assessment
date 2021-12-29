# M06Assessment

## Gameplay for Wheel of Fortune
The main point of the game is to make as much money as you can while guessing letters that make up a word or phrase that fall under a specific category. The category is shared with players at the beginning of each round and may be as general as "A Thing" or as specific as "Shakespearean Quote".

Players are able to make money by spinning a wheel. The section of wheel they land on determines how much money they can get for each of their consonant guesses. Below are the possible outcomes of spinning the wheel.

   The wheel lands on a number:
   * Player guesses a consonant that is in the puzzle: consonant (s) are revealed and they get the money on the wheel (Note: It does not matter how many times the consonant appears in the word. As long as the consonant appears at least once, they get the entire value of their wheel spin.)
   * Player guesses a consonant that is NOT in the puzzle: their turn ends and they get no money
   The wheel lands on BANKRUPT:
   * Player's bank goes to 0 and their turn ends

If a player successfully guesses a consonant, they also get an opportunity to "buy a vowel", which costs $250. They can continue to buy vowels as long as the vowels appear. If a word is down to vowels, each round is played with players being able to buy vowels.

At any point, a player can guess the answer. For this particular turn-based approach, a player should only attempt to guess the answer on their turn. If they successfully guess the answer, they win the round. If they do not successfully guess the answer, that consumes their turn.

For our game, there are 2 rounds with 3 players. The player with the most money at the end of round 2 goes on to round 3.

For our rounds, the round is over when the answer is guessed.

Round 3 is a single player guessing, with R-S-T-L-N-E all revealed at the beginning. The player can guess 3 more consonants and 1 more vowel - at no cost. For the game, they have 5 seconds to guess the final round's answer. For our solution, they have one guess. Have them win a cash prize - to be determined by you.

## Setting Up the Game
* There are three players - no more and no less.
* The first two rounds are played with three players. These round ends when the answer is guessed.
* Final round with player with highest bank
* Game is over after all three rounds.
## Player's Gameplay
* Spin the wheel
* If the wheel selection is Lose a Turn, end the player's turn.
* If the wheel selection is BANKRUPT, reset the player's bank to 0 and end their turn.
* If the wheel selection is a dollar value, they can guess a consonant.
* If they successfully guess a consonant, they have the opportunity to buy vowels.
* Vowels take money out of the player's bank.
* If the player still has options to play, they may guess the word. Otherwise, end their turn.
## Final Round
* 1 final round with the person with the highest bank.
* Final round starts with R-S-T-L-N-E revealed.
* In the final round, the player can pick 3 more consonants and 1 more vowel.
* The final round should have a timer of 5 or more seconds for the player to guess that answer.
* If they get the final answer, show them the cash prize that they won.
## The Wheel
The wheel is broken up in 24 segments with the following guidelines:

* One segment is labeled BANKRUPT. This will cause the player's bank to go to 0. They will also end their turn.
* Many segments have cash values rounded to the $50 between $100-$900.
* One segment is Lose a Turn. This causes the player's turn to end.
* Each player spins the wheel as part of their turn to determine how much they might make from a correct guess.

## How to Run:
1. Clone the repository pulling in at least the files:
   * Wheeloffortune.py
   * phrases.json
   * stringfile.json
   * All three need to be in the same directory
2. Run Wheeloffortune.py in python
 
webscrapper.py written by Scott Partacz to gather the phrases and clues from https://wheeloffortuneanswer.com.