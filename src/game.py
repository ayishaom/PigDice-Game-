"""PigGame: controller class that ties Menu, Player, DiceHand, Intelligence, Score and Histogram together.
Implements:
- single-player vs AI and two-player modes
- name change (keeps high-score stats via Score.rename_player)
- quit & restart
- cheat (type 'cheat' or 'c' during your turn to gain points)
- AI difficulty adjustable during play
- nice terminal output (UTF-8 dice faces)
"""

from typing import List, Optional
from diceHand import DiceHand
from intelligence import Intelligence
from player import Player
from score import Score
from histogram import Histogram

DICE_FACE_BASE = 0x2680  # ⚀ is U+2680

def dice_face(n: int) -> str:
    if 1 <= n <= 6:
        return chr(DICE_FACE_BASE + n - 1)
    return str(n)

class PigGame:
    def __init__(
        self,
        players: List[Player],
        score_manager: Score,
        winning_score: int = 100,
        dice_hand: Optional[DiceHand] = None,
        ai_agent: Optional[Intelligence] = None
    ):
        if len(players) != 2:
            raise ValueError("PigGame requires exactly two players.")
        self.players = players
        self.score_manager = score_manager
        self.winning_score = winning_score
        self.dice_hand = dice_hand or DiceHand(1)
        # AI agent used for computer decisions (shared agent is fine)
        self.ai_agent = ai_agent or Intelligence()
        self.current_index = 0  # which player's turn is active
        self.turn_total = 0
        self.running = True

    def show_board(self):
        p0, p1 = self.players
        print("\n" + "=" * 36)
        print(f" {p0.name:15} : {p0.total_score:3}    |    {p1.name:15} : {p1.total_score:3}")
        print("=" * 36)

    def play(self):
        """Main game loop (blocking). Accepts player input; returns when game finishes or user quits."""
        self.running = True
        while self.running:
            self.show_board()
            current = self.players[self.current_index]
            opponent = self.players[1 - self.current_index]
            self.turn_total = 0
            print(f"\n--- {current.name}'s turn --- (type 'help' for commands)")
            turn_active = True

            while turn_active and self.running:
                # decide (AI or user)
                if current.is_ai:
                    decision = self.ai_agent.decide(self.turn_total, current.total_score, opponent.total_score)
                    print(f"[AI decides to {decision}]")
                else:
                    raw = input("Enter (r)oll, (h)old, (c)heat, (n)ame, (ai) difficulty, (q)uit, (restart), (help): ").strip().lower()
                    if raw in ("r", "roll"):
                        decision = "roll"
                    elif raw in ("h", "hold"):
                        decision = "hold"
                    elif raw in ("c", "cheat"):
                        decision = "cheat"
                    elif raw in ("n", "name"):
                        decision = "name"
                    elif raw in ("ai", "difficulty"):
                        decision = "ai"
                    elif raw in ("q", "quit"):
                        # quit current game and return to menu without recording final result
                        print("Quitting current game and returning to menu...")
                        self.running = False
                        return
                    elif raw in ("restart",):
                        print("Restarting current match (scores reset).")
                        for p in self.players:
                            p.reset_score()
                        # break out to outer loop (start over)
                        turn_active = False
                        break
                    elif raw in ("help", "?"):
                        print(self._help_text())
                        continue
                    else:
                        print("Unknown command. Type 'help' for allowed commands.")
                        continue

                # handle decision
                if decision == "roll":
                    values = self.dice_hand.roll()
                    roll = values[0] if values else None
                    face = dice_face(roll) if roll is not None else "?"
                    print(f"{current.name} rolled {roll} {face}")
                    if roll == 1:
                        print("Oh no — rolled a 1. Turn lost.")
                        self.turn_total = 0
                        turn_active = False
                    else:
                        self.turn_total += roll
                        print(f"Turn total is now {self.turn_total}. (Hold to bank points)")
                        # automatic win check if adding turn_total would win
                        if current.total_score + self.turn_total >= self.winning_score:
                            current.add_score(self.turn_total)
                            print(f"\n🏆 {current.name} reaches {current.total_score} points and wins!")
                            self.score_manager.record_game(current.name, current.total_score)
                            return
                elif decision == "hold":
                    current.add_score(self.turn_total)
                    print(f"{current.name} banks {self.turn_total} points (total {current.total_score}).")
                    if current.total_score >= self.winning_score:
                        print(f"\n🏆 {current.name} wins with {current.total_score} points!")
                        self.score_manager.record_game(current.name, current.total_score)
                        return
                    turn_active = False
                elif decision == "cheat":
                    # quick cheat: add 50 points to current player
                    cheat_points = 50
                    print(f"Cheat used! Adding {cheat_points} points to {current.name}.")
                    current.add_score(cheat_points)
                    if current.total_score >= self.winning_score:
                        print(f"\n🏆 {current.name} wins by cheat with {current.total_score} points!")
                        self.score_manager.record_game(current.name, current.total_score)
                        return
                    turn_active = False
                elif decision == "name":
                    new_name = input("Enter new name: ").strip()
                    if new_name:
                        old = current.name
                        # preserve stats by renaming in score manager
                        renamed = self.score_manager.rename_player(old, new_name)
                        current.set_name(new_name)
                        if renamed:
                            print(f"Renamed {old} -> {new_name} and preserved stats.")
                        else:
                            print(f"Renamed locally to {new_name}. No previous stats existed for {old}.")
                    else:
                        print("Name change cancelled (empty name).")
                elif decision == "ai":
                    if not current.is_ai and any(p.is_ai for p in self.players):
                        # allow player to adjust AI difficulty
                        level = input("Set AI difficulty (easy, medium, hard): ").strip().lower()
                        try:
                            self.ai_agent.set_difficulty(level)
                            print(f"AI difficulty set to {level}.")
                        except Exception as e:
                            print("Invalid difficulty:", e)
                    else:
                        print("AI difficulty can only be adjusted while human is playing and an AI opponent exists.")
                else:
                    # unknown decision (should not happen)
                    print("Unknown internal decision:", decision)

            # switch player if we didn't restart or quit
            self.current_index = 1 - self.current_index

    def _help_text(self):
        return (
            "Commands during your turn:\n"
            "  r, roll      - roll the die\n"
            "  h, hold      - hold and bank the turn total\n"
            "  c, cheat     - use cheat (gains +50 points)\n"
            "  n, name      - change your player name (stats preserved)\n"
            "  ai           - change AI difficulty (if an AI opponent exists)\n"
            "  q, quit      - quit the current game and return to the menu\n"
            "  restart      - restart the match (reset scores)\n"
        )