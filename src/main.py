"""Menu logic.
- Show menu, read choices, print results.
- Create Game/Dice/Players and run the loop.
- All rules are in other classes; this is UI only."""

from menu import Menu

def main():
    """Run the menu."""
    menu = Menu()
    menu.run()

if __name__ == "__main__":
    main()
