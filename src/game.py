from typing import List, Optional
from diceHand import DiceHand
from intelligence import Intelligence
from player import Player
from score import Score

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
        ai_agent: Optional[Intelligence] = None,
    ):
        if len(players) != 2:
            raise ValueError("PigGame requires exactly two players.")
        self.players = players
        self.score_manager = score_manager
        self.winning_score = winning_score
        self.dice_hand = dice_hand or DiceHand(1)
        self.ai_agent = ai_agent or Intelligence()
        self.current_index = 0
        self.turn_total = 0
        self.running = True

    # ----------------- UI helpers -----------------

    def show_board(self):
        p0, p1 = self.players
        a0 = "🤖" if p0.is_ai else "👤"
        a1 = "🤖" if p1.is_ai else "👤"

        title = "🎲  PIG (DICE GAME)  🎲"
        border = "═" * 60

        print("\n" + border)
        print(title.center(len(border)))
        print(border)
        print(f"  {a0} {p0.name:15} : {p0.total_score:3}    |    {a1} {p1.name:15} : {p1.total_score:3}")
        print("═" * 60)

    def _prompt_cmd(self) -> str:
        valid = {
            "r": "roll", "roll": "roll",
            "h": "hold", "hold": "hold",
            "c": "cheat", "cheat": "cheat",
            "n": "name", "name": "name",
            "ai": "ai",
            "q": "quit", "quit": "quit",
            "restart": "restart",
            "help": "help", "?": "help",
        }
        while True:
            try:
                raw = input(
                    "➤ (r)oll 🎲, (h)old ✋, (c)heat 🪄, (n)ame ✍️, (ai) 🔧, "
                    "(q)uit 👋, (restart) 🔄, (help) 🆘 : "
                )
            except (EOFError, KeyboardInterrupt):
                print("\n👋 Exiting turn…")
                return "quit"
            choice = (raw or "").strip().lower()
            if choice in valid:
                return valid[choice]
            print("⚠️  Unknown command. Type 'help' for allowed commands.")

    def _prompt_ai_level(self) -> Optional[str]:
        valid = {"easy", "medium", "hard"}
        while True:
            try:
                raw = input("➤ Set AI difficulty (easy, medium, hard) [Enter to cancel]: ")
            except (EOFError, KeyboardInterrupt):
                print("\n❌ Cancelled.")
                return None
            choice = (raw or "").strip().lower()
            if choice == "":
                return None
            if choice in valid:
                return choice
            print("⚠️  Invalid difficulty. Choose: easy, medium, or hard.")

    def _help_text(self):
        return (
            "\n🆘 HELP\n"
            "Commands during your turn:\n"
            "  r, roll      - roll the die 🎲\n"
            "  h, hold      - bank the turn total ✋\n"
            "  c, cheat     - add +50 points 🪄\n"
            "  n, name      - change your player name ✍️ (stats preserved)\n"
            "  ai           - change AI difficulty 🔧 (if an AI opponent exists)\n"
            "  q, quit      - quit current game and return to the menu 👋\n"
            "  restart      - reset both players' scores 🔄\n"
        )

    # ----------------- Main loop -----------------

    def play(self):
        self.running = True
        while self.running:
            self.show_board()
            current = self.players[self.current_index]
            opponent = self.players[1 - self.current_index]
            self.turn_total = 0

            turn_header = "🤖  " + current.name if current.is_ai else "👤  " + current.name
            print(f"\n--- {turn_header}'s turn ---  (type 'help' for commands)\n")

            turn_active = True

            while turn_active and self.running:
                if current.is_ai:
                    decision = self.ai_agent.decide(self.turn_total, current.total_score, opponent.total_score)
                    print(f"[🤖 AI decides to {decision}]")
                else:
                    cmd = self._prompt_cmd()
                    decision = cmd
                    if decision == "help":
                        print(self._help_text())
                        continue
                    if decision == "quit":
                        print("\n👋 Quitting current game and returning to menu...\n")
                        self.running = False
                        return
                    if decision == "restart":
                        print("\n🔄 Restarting current match (scores reset).\n")
                        for p in self.players:
                            p.reset_score()
                        turn_active = False
                        break
                    if decision == "ai":
                        if any(p.is_ai for p in self.players):
                            level = self._prompt_ai_level()
                            if level:
                                try:
                                    self.ai_agent.set_difficulty(level)
                                    print(f"🔧 AI difficulty set to {level}.")
                                except Exception as e:
                                    print("⚠️  Invalid difficulty:", e)
                        else:
                            print("ℹ️  AI difficulty can only be changed when an AI opponent exists.")
                        continue
                    if decision == "name":
                        try:
                            new_name = input("➤ Enter new name [Enter to cancel]: ")
                        except (EOFError, KeyboardInterrupt):
                            print("\n❌ Name change cancelled.")
                            continue
                        new_name = (new_name or "").strip()
                        if not new_name:
                            print("❌ Name change cancelled.")
                            continue
                        old = current.name
                        renamed = self.score_manager.rename_player(old, new_name)
                        current.set_name(new_name)
                        if renamed:
                            print(f"✍️  Renamed {old} → {new_name} and preserved stats.")
                        else:
                            print(f"✍️  Renamed locally to {new_name}. No previous stats existed for {old}.")
                        continue

                # Handle roll/hold/cheat
                if decision == "roll":
                    values = self.dice_hand.roll()
                    roll = values[0] if values else None
                    face = dice_face(roll) if roll is not None else "?"
                    print(f"🎲 {current.name} rolled {roll} {face}")

                    if roll is None:
                        print("Invalid roll. Turn lost.")
                        self.turn_total = 0
                        turn_active = False
                        continue

                    if roll == 1:
                        print("💥  Oh no — rolled a 1. Turn lost.")
                        self.turn_total = 0
                        turn_active = False
                    else:
                        self.turn_total += roll
                        print(f"➕ Turn total is now {self.turn_total}. (Hold to bank points)")
                        if current.total_score + self.turn_total >= self.winning_score:
                            current.add_score(self.turn_total)
                            print(f"\n🏆 {current.name} reaches {current.total_score} points and wins!\n")
                            self.score_manager.record_game(current.name, current.total_score)
                            return

                elif decision == "hold":
                    current.add_score(self.turn_total)
                    print(f"💰 {current.name} banks {self.turn_total} points (total {current.total_score}).")
                    if current.total_score >= self.winning_score:
                        print(f"\n🏆 {current.name} wins with {current.total_score} points!\n")
                        self.score_manager.record_game(current.name, current.total_score)
                        return
                    turn_active = False

                elif decision == "cheat":
                    cheat_points = 50
                    print(f"🪄 Cheat used! Adding {cheat_points} points to {current.name}.")
                    current.add_score(cheat_points)
                    if current.total_score >= self.winning_score:
                        print(f"\n🏆 {current.name} wins by cheat with {current.total_score} points!\n")
                        self.score_manager.record_game(current.name, current.total_score)
                        return
                    turn_active = False

            self.current_index = 1 - self.current_index
