from PyQt6.QtWidgets import QWidget
from src.Hand import Hand
from src.Ground import Ground
from ui.player_layout import Ui_Player

class Player(QWidget,Ui_Player):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.hand = Hand(player=self)
        self.ground = Ground(player=self)  # Each player has their own ground
       
        self.pushButton.clicked.connect(self.show_hand)
        self.pushButton1.clicked.connect(self.show_ground)

    def show_hand(self):
        if not self.hand.isVisible():
            self.hand.show()

    def show_ground(self):
        if not self.ground.isVisible():
            self.ground.show()