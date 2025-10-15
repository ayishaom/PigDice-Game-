from player import Player
from score import Score
from intelligence import Intelligence
from game import PigGame


class Menu:
    def __init__(self):
        self.running = True

    # ----------------- Public API -----------------

    def run(self):
        """Main menu loop with resilient input handling."""
        while self.running:
            try:
                self.display_options()
                choice = self._prompt_menu_choice("Enter your choice (1-5): ")
                self.handle_choice(choice)
            except (KeyboardInterrupt, EOFError):
                print("\nExiting… Goodbye.")
                self.running = False

    def display_options(self):
        print("\n--- MENU ---")
        print("1. Play against computer")
        print("2. Play two-player game")
        print("3. View high scores")
        print("4. View rules")
        print("5. Quit")

    def handle_choice(self, choice: str):
        if choice == "1":
            self.start_single_player()
        elif choice == "2":
            self.start_two_player()
        elif choice == "3":
            self.show_high_scores()
        elif choice == "4":
            self.show_rules()
        elif choice == "5":
            self.running = False
            print("Thanks for playing! Goodbye.")
        else:
            # This should not happen because _prompt_menu_choice validates,
            # but we keep a fallback just in case.
            print("Invalid choice, please try again.")

    # ----------------- Game-launching Methods -----------------

    def start_single_player(self):
        """Start a game vs computer (with validated inputs)."""
        name = self._prompt_nonempty_name("Enter your name [Player]: ", default="Player")
        human = Player(name, is_ai=False)
        computer = Player("Computer", is_ai=True)

        score_manager = Score()

        level = self._prompt_difficulty("Choose AI difficulty (easy, medium, hard) [medium]: ", default="medium")
        ai_agent = Intelligence()
        ai_agent.set_difficulty(level)

        game = PigGame([human, computer], score_manager, ai_agent=ai_agent)
        game.play()

    def start_two_player(self):
        """Start a two-player local game (with validated inputs)."""
        name1 = self._prompt_nonempty_name("Enter Player 1 name [Player1]: ", default="Player1")
        name2 = self._prompt_nonempty_name("Enter Player 2 name [Player2]: ", default="Player2")

        p1 = Player(name1, is_ai=False)
        p2 = Player(name2, is_ai=False)
        score_manager = Score()
        game = PigGame([p1, p2], score_manager)
        game.play()

    def show_high_scores(self):
        """Show saved high scores using Score and Histogram."""
        score_manager = Score()
        highs = score_manager.get_high_scores()
        if not highs:
            print("No scores recorded yet.")
            return
        from histogram import Histogram
        h = Histogram(scale=10)
        print("\n-- High Scores (by total points) --")
        for idx, (name, stats) in enumerate(highs, start=1):
            print(f"{idx}. {name}: {stats.get('total_points', 0)} points ({len(stats.get('games', []))} games)")
        print("\nHistogram (total points):")
        for line in h.generate_total(highs):
            print(line)

    def show_rules(self):
        print("""
🎲 PIG DICE — RULES 🎲

- Players take turns to roll one die.
- On your turn you may roll as many times as you like.
- Each non-1 roll adds to your turn total.
- If you roll a 1 you lose your turn total and the turn ends.
- You may 'hold' to bank the turn total into your overall score.
- First to reach 100 points wins.
- You may change your name during the game; stats are preserved in high scores.

Cheat instructions:
- During your turn, type 'cheat' or 'c' to add +50 points to the current player.
- You can also type 'restart' during a game to reset both players' scores to zero.
- Use 'ai' during your turn to change AI difficulty (easy, medium, hard).
- Type 'name' to change a player's name.
""")

    # ----------------- Input Helpers (Validation) -----------------

    def _prompt_menu_choice(self, prompt: str) -> str:
        """Loop until user enters one of '1'..'5'."""
        valid = {"1", "2", "3", "4", "5"}
        while True:
            choice = input(prompt).strip()
            if choice in valid:
                return choice
            print("Please enter a number between 1 and 5.")

    def _prompt_nonempty_name(self, prompt: str, default: str) -> str:
        """
        Ask for a name; accept default on empty input.
        Reject names that are only whitespace.
        """
        while True:
            raw = input(prompt)
            if raw is None:
                return default
            name = raw.strip()
            if name:
                return name
            # Allow user to accept default by pressing Enter explicitly
            if raw == "":
                return default
            print("Name cannot be empty. Please try again.")

    def _prompt_difficulty(self, prompt: str, default: str = "medium") -> str:
        """Ask for difficulty; allow Enter for default; validate choice."""
        valid = {"easy", "medium", "hard"}
        while True:
            raw = input(prompt)
            if raw is None or raw.strip() == "":
                return default
            level = raw.strip().lower()
            if level in valid:
                return level
            print("Invalid difficulty. Choose: easy, medium, or hard.")
