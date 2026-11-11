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
        if not letter or len(letter) != 1 or not letter.isalpha():
            return "Enter one letter."
        letter = letter.lower()
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

    def handle_command(self, cmd):
        cmd = cmd.lower().strip()
        if cmd == "/hint":
            hint = self.use_hint()
            if hint:
                return f"Hint: {hint}"
            return "Hint already used for this round."
        elif cmd == "/stats":
            return (
                f"Score: {self.score} | Streak: {self.streak} | "
                f"Rounds: {self.stats.rounds} | Won: {self.stats.wins} | Best streak: {self.stats.best_streak}"
            )
        elif cmd == "/help":
            return "Available commands: /hint (clue), /stats (session stats), /help (commands), /quit (exit)"
        elif cmd == "/quit":
            return "QUIT"
        else:
            return f"Unknown command '{cmd}'. Type /help for available commands."

    def play_round(self):
        self.start_round()
        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print(f"Lives: {self.lives} Score: {self.score} Streak: {self.streak} Diff: {self.difficulty}")
            raw = input("Letter, /hint, or /quit: ").strip()
            if not raw:
                print("Enter one letter.")
                continue
            if raw.startswith("/"):
                result = self.handle_command(raw)
                if result == "QUIT":
                    print("Quitting round.")
                    return False
                print(result)
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

    def select_category(self):
        while True:
            print("\nCategories:", ", ".join(WORDS.keys()))
            print(f"Current category: {self.category}")
            raw = input(f"Choose category [Enter to keep '{self.category}', or 'q' to quit]: ").strip().lower()
            if raw == "q":
                return False
            if not raw:
                print(f"Category preserved: {self.category}")
                return True
            if raw in WORDS:
                if raw == self.category:
                    print(f"Category is already set to '{raw}'.")
                else:
                    self.category = raw
                    print(f"Category set to: {self.category}")
                return True
            print(f"Unknown category '{raw}'. Available: {', '.join(WORDS.keys())}")

    def select_difficulty(self):
        while True:
            diff_list = ", ".join(f"{k} ({v['lives']} lives)" for k, v in DIFFICULTIES.items())
            print(f"Difficulties: {diff_list}")
            print(f"Current difficulty: {self.difficulty}")
            raw = input(f"Choose difficulty [Enter to keep '{self.difficulty}']: ").strip().lower()
            if not raw:
                print(f"Difficulty preserved: {self.difficulty}")
                return True
            if raw in DIFFICULTIES:
                if raw == self.difficulty:
                    print(f"Difficulty is already set to '{raw}'.")
                else:
                    self.difficulty = raw
                    print(f"Difficulty set to: {self.difficulty}")
                return True
            print(f"Unknown difficulty '{raw}'. Available: {', '.join(DIFFICULTIES.keys())}")

    def print_session_stats(self):
        print(f"Rounds played: {self.stats.rounds} | Won: {self.stats.wins} | Best streak: {self.stats.best_streak}")

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")
        if not self.select_category():
            print("Final score:", self.score, " Streak:", self.streak)
            self.print_session_stats()
            return
        self.select_difficulty()

        while True:
            if not self.play_round():
                print("Final score:", self.score, " Streak:", self.streak)
                self.print_session_stats()
                return

            print("Final score:", self.score, " Streak:", self.streak)
            self.print_session_stats()

            while True:
                choice = input("\nPlay another round? [y=yes, n=no, c=change category/difficulty]: ").strip().lower()
                if choice in ("y", ""):
                    break
                elif choice in ("n", "q"):
                    print("Goodbye!")
                    return
                elif choice == "c":
                    if not self.select_category():
                        return
                    self.select_difficulty()
                    break
                else:
                    print("Invalid choice. Please enter 'y', 'n', or 'c'.")
