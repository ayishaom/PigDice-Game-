class Menu:

    def __init__(self):
        self.running = True

    def run(self):
        """Run the main menu loop."""
        while self.running:
            self.display_options()
            choice = input("Enter your choice: ").strip()
            self.handle_choice(choice)

    def display_options(self):
        print("\n--- MENU ---")
        print("1. Play single-player game")
        print("2. Play two-player game")
        print("3. View high scores")
        print("4. View rules")
        print("5. Quit")

    def handle_choice(self, choice):
        """Execute menu selection."""
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

    # ----------------- Placeholder Methods -----------------

    def start_single_player(self):
        """Placeholder for starting a single-player game."""
        print("[Placeholder] start_single_player() would be called here.")

    def start_two_player(self):
        """Placeholder for starting a two-player game."""
        print("[Placeholder] start_two_player() would be called here.")

    def show_high_scores(self):
        """Placeholder for showing high scores."""
        print("[Placeholder] show_high_scores() would be called here.")

    def show_rules(self):
        """Placeholder for showing rules."""
        print("[Placeholder] show_rules() would be called here.")
