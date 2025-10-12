from player import Player
from score import Score
from intelligence import Intelligence
from game import PigGame

class Menu:

    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            self.display_options()
            choice = input("Enter your choice: ").strip()
            self.handle_choice(choice)

    def display_options(self):
        print("\n--- MENU ---")
        print("1. Play against computer")
        print("2. Play two-player game")
        print("3. View high scores")
        print("4. View rules")
        print("5. Quit")

    def handle_choice(self, choice):
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
            print("Invalid choice, please try again.")

    # ----------------- Game-launching Methods -----------------

    def start_single_player(self):
        """Start a game vs computer."""
        name = input("Enter your name: ").strip()
        if not name:
            name = "Player"
        human = Player(name, is_ai=False)
        computer = Player("Computer", is_ai=True)

        score_manager = Score()
        # let user pick AI difficulty
        level = input("Choose AI difficulty (easy, medium, hard) [medium]: ").strip().lower()
        if level not in ("easy", "medium", "hard"):
            level = "medium"
        ai_agent = Intelligence()
        ai_agent.set_difficulty(level)

        game = PigGame([human, computer], score_manager, ai_agent=ai_agent)
        game.play()

    def start_two_player(self):
        """Start a two-player local game."""
        name1 = input("Enter Player 1 name: ").strip()
        if not name1:
            name1 = "Player1"
        name2 = input("Enter Player 2 name: ").strip()
        if not name2:
            name2 = "Player2"

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