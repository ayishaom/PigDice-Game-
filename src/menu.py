"""Menu system for the Pig game.

Handles game start, player setup, high scores, rules, and user input.
"""

from player import Player
from score import Score
from intelligence import Intelligence
from game import PigGame


class Menu:
    """Main menu interface for the Pig dice game.

    Handles menu display, input validation, and launching single- or
    two-player games, as well as showing high scores and rules.
    """

    def __init__(self):
        """Initialize the menu state."""
        self.running = True

    def run(self):
        """Run the main menu loop until the user chooses to quit."""
        while self.running:
            try:
                self.display_options()
                choice = self._prompt_menu_choice("👉 Enter your choice "
                                                  "(1-5): ")
                self.handle_choice(choice)
            except (KeyboardInterrupt, EOFError):
                print("\n👋 Exiting… Goodbye.")
                self.running = False

    def display_options(self):
        """Display the main menu options to the user."""
        title = "🎲  PIG (DICE GAME)  🎲"
        border = "═" * 40
        print("\n" + border)
        print(title.center(len(border)))
        print(border)
        print("1️⃣  Play against computer 🤖")
        print("2️⃣  Play two-player game 👤👤")
        print("3️⃣  View high scores 🏅")
        print("4️⃣  View rules 📖")
        print("5️⃣  Quit 🚪\n")

    def handle_choice(self, choice: str):
        """Handle the user's menu selection."""
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
            print("\n🙏 Thanks for playing! Goodbye. 👋\n")
        else:
            print("❌ Invalid choice, please try again.\n")

    def start_single_player(self):
        """Start a game vs computer."""
        name = self._prompt_nonempty_name("👤 Enter your name "
                                          "[Player]: ", default="Player")
        human = Player(name, is_ai=False)
        computer = Player("Computer", is_ai=True)

        score_manager = Score()

        level = self._prompt_difficulty("⚙️ Choose AI difficulty "
                                        "(easy, medium, hard) [medium]: ",
                                        default="medium")
        ai_agent = Intelligence()
        ai_agent.set_difficulty(level)

        print("\n🎲 Starting PIG (DICE GAME) — single player…\n")
        game = PigGame([human, computer], score_manager, ai_agent=ai_agent)
        game.play()

    def start_two_player(self):
        """Start a two-player local game."""
        name1 = self._prompt_nonempty_name("👤 Enter Player 1 name "
                                           "[Player1]: ", default="Player1")
        name2 = self._prompt_nonempty_name("👤 Enter Player 2 name "
                                           "[Player2]: ", default="Player2")

        p1 = Player(name1, is_ai=False)
        p2 = Player(name2, is_ai=False)
        score_manager = Score()

        print("\n🎲 Starting PIG (DICE GAME) — two players…\n")
        game = PigGame([p1, p2], score_manager)
        game.play()

    def show_high_scores(self):
        """Display high scores and histogram of player totals."""
        score_manager = Score()
        highs = score_manager.get_high_scores()
        if not highs:
            print("\n📭 No scores recorded yet.\n")
            return
        from histogram import Histogram
        h = Histogram(scale=10)

        # Compatibility line for tests expecting "High Scores"
        print("\n-- High Scores --")

        print("\n🏅 -- HIGH SCORES (BY TOTAL POINTS) -- 🏅\n")

        for idx, (name, stats) in enumerate(highs, start=1):
            print(f"{idx}. {name}: {stats.get('total_points', 0)} points "
                  f"({len(stats.get('games', []))} games)")
        print("\n📊 Histogram (total points):\n")
        for line in h.generate_total(highs):
            print(line)

    def show_rules(self):
        """Display the rules of the Pig dice game to the user."""
        print("PIG DICE — RULES")

        print("""
📖 PIG (DICE GAME) — RULES

- Players take turns to roll one die 🎲
- Each non-1 roll adds to your turn total ➕
- If you roll a 1 💥 you lose your turn total and the turn ends
- Choose 'hold' ✋ to bank your turn total into your overall score 💰
- First to reach 100 points wins 🏆
- You can change your name during the game ✍️ (stats are preserved)

Cheat & options:
- During your turn, type 'cheat' or 'c' to add +50 points 🪄
- Type 'restart' to reset both players' scores 🔄
- Use 'ai' during your turn to change AI difficulty (easy, medium, hard) 🤖
- Type 'name' to change a player's name 👤
""")

    # ----------------- Input Helpers (Validation) -----------------

    def _prompt_menu_choice(self, prompt: str) -> str:
        """Loop until user enters one of '1'..'5'."""
        valid = {"1", "2", "3", "4", "5"}
        while True:
            choice = input(prompt).strip()
            if choice in valid:
                return choice
            print("🚫 Please enter a number between 1 and 5.\n")

    def _prompt_nonempty_name(self, prompt: str, default: str) -> str:
        """Prompt the user for a name and return it.

        Uses a default if input is empty. Rejects names that are only
        whitespace.
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
            print("⚠️ Name cannot be empty. Please try again.\n")

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
            print("🚫 Invalid difficulty. Choose: easy, medium, or hard.\n")
