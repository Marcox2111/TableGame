import sys
from PyQt6.QtWidgets import QApplication
from src.Player import Player

class Game:
    def __init__(self):
        self.player = Player()
        self.player.show()
        self.used_cards = set()

    def use_card(self, card):
        self.used_cards.add(card.card_id)

    def is_card_used(self, card):
        return card.card_id in self.used_cards


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec())
