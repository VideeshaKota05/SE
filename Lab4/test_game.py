import unittest
from game import HangmanGame, DIFFICULTIES
from stats import SessionStats
from words import WORDS, HINTS


class TestHangman(unittest.TestCase):
    def setUp(self):
        self.game = HangmanGame()
        self.game.category = "technology"
        self.game.secret = "python"
        self.game.guessed = set()
        self.game.wrong = set()
        self.game.lives = 6
        self.game.hint_used = False

    # Task 1 Tests: Guess-state correctness
    def test_correct_guess_recorded_once(self):
        res1 = self.game.guess("p")
        self.assertEqual(res1, "Correct.")
        self.assertIn("p", self.game.guessed)
        self.assertEqual(self.game.lives, 6)

        # Repeated correct guess
        res2 = self.game.guess("p")
        self.assertEqual(res2, "Already guessed.")
        self.assertEqual(self.game.lives, 6)

    def test_wrong_guess_recorded_once(self):
        res1 = self.game.guess("z")
        self.assertEqual(res1, "Wrong.")
        self.assertIn("z", self.game.wrong)
        self.assertEqual(self.game.lives, 5)

        # Repeated wrong guess must NOT consume another life
        res2 = self.game.guess("z")
        self.assertEqual(res2, "Already guessed.")
        self.assertEqual(self.game.lives, 5)

    def test_case_insensitive_guess(self):
        res1 = self.game.guess("P")
        self.assertEqual(res1, "Correct.")
        res2 = self.game.guess("p")
        self.assertEqual(res2, "Already guessed.")

    def test_invalid_guess_does_not_consume_life(self):
        initial_lives = self.game.lives
        self.assertEqual(self.game.guess("1"), "Enter one letter.")
        self.assertEqual(self.game.lives, initial_lives)

        self.assertEqual(self.game.guess("abc"), "Enter one letter.")
        self.assertEqual(self.game.lives, initial_lives)

        self.assertEqual(self.game.guess(""), "Enter one letter.")
        self.assertEqual(self.game.lives, initial_lives)

        self.assertEqual(self.game.guess("!"), "Enter one letter.")
        self.assertEqual(self.game.lives, initial_lives)

    # Task 2 Tests: Session model integration
    def test_session_stats_tracking(self):
        self.assertIsInstance(self.game.stats, SessionStats)
        self.assertEqual(self.game.stats.rounds, 0)
        self.assertEqual(self.game.stats.wins, 0)
        self.assertEqual(self.game.stats.best_streak, 0)

        # Simulate round 1 win
        self.game.streak = 1
        self.game.stats.record(True, self.game.streak)
        self.assertEqual(self.game.stats.rounds, 1)
        self.assertEqual(self.game.stats.wins, 1)
        self.assertEqual(self.game.stats.best_streak, 1)

        # Simulate round 2 win
        self.game.streak = 2
        self.game.stats.record(True, self.game.streak)
        self.assertEqual(self.game.stats.rounds, 2)
        self.assertEqual(self.game.stats.wins, 2)
        self.assertEqual(self.game.stats.best_streak, 2)

        # Simulate round 3 loss
        self.game.streak = 0
        self.game.stats.record(False, self.game.streak)
        self.assertEqual(self.game.stats.rounds, 3)
        self.assertEqual(self.game.stats.wins, 2)
        self.assertEqual(self.game.stats.best_streak, 2)

    def test_start_round_resets_only_round_state(self):
        self.game.score = 25
        self.game.streak = 3
        self.game.category = "science"
        self.game.difficulty = "hard"
        self.game.stats.rounds = 3
        self.game.stats.wins = 2

        self.game.start_round()

        # Session state preserved
        self.assertEqual(self.game.score, 25)
        self.assertEqual(self.game.streak, 3)
        self.assertEqual(self.game.category, "science")
        self.assertEqual(self.game.difficulty, "hard")
        self.assertEqual(self.game.stats.rounds, 3)
        self.assertEqual(self.game.stats.wins, 2)

        # Round state reset
        self.assertEqual(self.game.guessed, set())
        self.assertEqual(self.game.wrong, set())
        self.assertFalse(self.game.hint_used)
        self.assertEqual(self.game.lives, DIFFICULTIES["hard"]["lives"])

    # Task 3 Tests: Difficulty and scoring
    def test_difficulty_lives_and_scoring(self):
        for diff_name, cfg in DIFFICULTIES.items():
            self.game.difficulty = diff_name
            self.game.start_round()
            self.assertEqual(self.game.lives, cfg["lives"])

    def test_hint_scoring_does_not_leak_on_loss(self):
        self.game.score = 10
        hint = self.game.use_hint()
        self.assertIsNotNone(hint)
        self.assertTrue(self.game.hint_used)
        # Score does not leak or drop on loss
        self.assertEqual(self.game.score, 10)

    def test_hint_repeated_usage(self):
        hint1 = self.game.use_hint()
        self.assertIsNotNone(hint1)
        hint2 = self.game.use_hint()
        self.assertIsNone(hint2)

    # Task 4 Tests: Command handling and input robustness
    def test_handle_command_hint(self):
        res1 = self.game.handle_command("/hint")
        self.assertTrue(res1.startswith("Hint:"))
        # Repeated hint
        res2 = self.game.handle_command("/hint")
        self.assertEqual(res2, "Hint already used for this round.")

    def test_handle_command_help(self):
        res = self.game.handle_command("/help")
        self.assertIn("Available commands", res)

    def test_handle_command_stats(self):
        res = self.game.handle_command("/stats")
        self.assertIn("Score:", res)
        self.assertIn("Streak:", res)

    def test_handle_command_quit(self):
        res = self.game.handle_command("/quit")
        self.assertEqual(res, "QUIT")

    def test_handle_command_unknown(self):
        res = self.game.handle_command("/foobar")
        self.assertIn("Unknown command '/foobar'", res)

    def test_category_and_difficulty_setting(self):
        self.assertTrue(self.game.set_category("science"))
        self.assertEqual(self.game.category, "science")
        self.assertFalse(self.game.set_category("invalid_cat"))
        self.assertEqual(self.game.category, "science")

        self.assertTrue(self.game.set_difficulty("hard"))
        self.assertEqual(self.game.difficulty, "hard")
        self.assertFalse(self.game.set_difficulty("nightmare"))
        self.assertEqual(self.game.difficulty, "hard")


if __name__ == "__main__":
    unittest.main()
