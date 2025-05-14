import random
import json
from collections import Counter


class GameManager:

    def __init__(self):
        self.max_fails = 6
        self.reset_game()
        self.score_file = "scoreboard.json"
        self.load_scores()

    def load_words(self):
        with open("words.txt", "r", encoding="utf-8") as f:
            self.words = [
                w.strip().lower() for w in f.readlines() if w.strip()
            ]

    def reset_game(self):
        self.load_words()
        self.word = random.choice(self.words)
        self.visible = ["_" for _ in self.word]
        self.guessed_letters = []
        self.fails = 0
        self.letters_votes = []
        self.word_guesses = {}
        self.finished = False
        self.result_message = ""

    def vote_letter(self, user, letter):
        if not self.finished and len(letter) == 1 and letter.isalpha():
            self.letters_votes.append(letter.lower())

    def vote_word(self, user, word):
        if not self.finished and word.isalpha():
            self.word_guesses[user] = word.lower()

    def apply_voted_letter(self):
        if not self.letters_votes:
            return

        count = Counter(self.letters_votes)
        top_votes = count.most_common()
        if not top_votes:
            return
        top_letter = top_votes[0][0]
        top_count = top_votes[0][1]
        # comprobar empates
        tied = [l for l, c in top_votes if c == top_count]
        chosen_letter = random.choice(tied) if len(tied) > 1 else top_letter

        if chosen_letter in self.word:
            for i, l in enumerate(self.word):
                if l == chosen_letter:
                    self.visible[i] = l
        else:
            self.fails += 1

        self.guessed_letters.append(chosen_letter)
        self.letters_votes.clear()

        if "_" not in self.visible:
            self.finished = True
            self.result_message = "¡El chat ha ganado! La palabra era: " + self.word
        elif self.fails >= self.max_fails:
            self.finished = True
            self.result_message = "Has perdido. La palabra era: " + self.word

    def check_word_guesses(self):
        winners = []
        for user, guess in self.word_guesses.items():
            if guess == self.word:
                winners.append(user)
        if winners:
            for user in winners:
                self.scores[user] = self.scores.get(user, 0) + 1
            self.save_scores()
            self.visible = list(self.word)
            self.finished = True
            self.result_message = f"¡{', '.join(winners)} han ganado! La palabra era: {self.word}"
        self.word_guesses.clear()

    def get_visible_word(self):
        return " ".join(self.visible)

    def save_scores(self):
        with open(self.score_file, "w", encoding="utf-8") as f:
            json.dump(self.scores, f)

    def load_scores(self):
        try:
            with open(self.score_file, "r", encoding="utf-8") as f:
                self.scores = json.load(f)
        except:
            self.scores = {}

    def get_scores(self):
        return sorted(self.scores.items(), key=lambda x: -x[1])
