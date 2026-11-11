import random
from words import WORDS, HINTS
from stats import SessionStats

DIFFICULTIES = {
    "easy": {"lives": 8, "base_score": 3, "hint_penalty": 1},
    "medium": {"lives": 6, "base_score": 5, "hint_penalty": 2},
    "hard": {"lives": 4, "base_score": 8, "hint_penalty": 3},
}


class HangmanGame:
    def __init__(self):
        self.score = 0
        self.streak = 0
        self.category = "technology"
        self.difficulty = "medium"
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False
        self.stats = SessionStats()

    def set_difficulty(self, diff):
        diff = diff.lower().strip()
        if diff in DIFFICULTIES:
            self.difficulty = diff
            return True
        return False

    def set_category(self, cat):
        cat = cat.lower().strip()
        if cat in WORDS:
            self.category = cat
            return True
        return False

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(ch if ch in self.guessed else "_" for ch in self.secret)

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        letter = letter.lower()
        if len(letter) != 1 or not letter.isalpha():
            return "Enter one letter."
        if letter in self.guessed or letter in self.wrong:
            return "Already guessed."
        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."
        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        if self.hint_used:
            return None
        self.hint_used = True
        return HINTS.get(self.secret, "No hint available.")

    def play_round(self):
        self.start_round()
        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print(f"Lives: {self.lives} Score: {self.score} Streak: {self.streak} Diff: {self.difficulty}")
            raw = input("Letter, /hint, or /quit: ").strip().lower()
            if raw == "/quit":
                return False
            if raw == "/hint":
                hint = self.use_hint()
                print(hint if hint else "Hint already used.")
                continue
            print(self.guess(raw))

        if self.won():
            self.streak += 1
            diff_cfg = DIFFICULTIES[self.difficulty]
            penalty = diff_cfg["hint_penalty"] if self.hint_used else 0
            earned = max(1, diff_cfg["base_score"] + self.streak - penalty)
            self.score += earned
            print(f"Solved: {self.secret} (+{earned} points)")
            self.stats.record(True, self.streak)
            return True

        self.streak = 0
        print("Out of lives. The word was:", self.secret)
        self.stats.record(False, self.streak)
        return True

    def print_session_stats(self):
        print(f"Rounds played: {self.stats.rounds} | Won: {self.stats.wins} | Best streak: {self.stats.best_streak}")

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")
        while True:
            print("\nCategories:", ", ".join(WORDS))
            print(f"Current category: {self.category} | Difficulty: {self.difficulty}")
            raw = input(f"Choose category [Enter to keep '{self.category}', or 'q' to quit]: ").strip().lower()
            if raw == "q":
                print("Final score:", self.score, " Streak:", self.streak)
                self.print_session_stats()
                return
            if raw:
                if not self.set_category(raw):
                    print("Unknown category.")
                    continue

            diff_raw = input(f"Choose difficulty (easy, medium, hard) [Enter to keep '{self.difficulty}']: ").strip().lower()
            if diff_raw:
                if not self.set_difficulty(diff_raw):
                    print("Unknown difficulty. Keeping current.")

            if not self.play_round():
                print("Final score:", self.score, " Streak:", self.streak)
                self.print_session_stats()
                return
            again = input("Another round? [y/n]: ").strip().lower()
            if again != "y":
                print("Final score:", self.score, " Streak:", self.streak)
                self.print_session_stats()
                return
