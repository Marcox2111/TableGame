from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PIL import ImageGrab
from src.Card import Card
from ui.hand_layout import Ui_Hand
from config import CardFolder, x1, x2, y1, y2, width, height


class Hand(QWidget, Ui_Hand):
    card_counter=0

    def __init__(self, player):
        super().__init__()
         # Initialize attributes
        self.player = player
        self.cards = []  # List to store Card objects
        self.card_id_to_label = {}  # Dictionary to map card IDs to labels

        self.setupUi(self)

        self.pushButton.clicked.connect(self.draw_card)


        
    def draw_card(self):
        """Draw a card and display its preview."""
        Hand.card_counter += 1
        card_id = Hand.card_counter

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        location = f"{CardFolder}/Card_{card_id}.png"
        screenshot.save(location)

        card = Card(parent=self, card_id=card_id, context='hand')

        pixmap = QPixmap(location).scaled(int(width/3), int(height/3), Qt.AspectRatioMode.KeepAspectRatio)
        label = QLabel(self)
        label.setPixmap(pixmap)

        self.card_id_to_label[card.card_id] = label

        self.cards.append(card) # Add the card to the list

        label.mousePressEvent = lambda event, card=card: self.on_preview_clicked(event, card)
        self.horizontalLayout.addWidget(label)

    def on_card_used(self, card):
        """Handle the event when a card is used."""
        label_to_remove = self.card_id_to_label.get(card.card_id)

        # Remove the QLabel from the layout and list
        self.horizontalLayout.removeWidget(label_to_remove)
        label_to_remove.deleteLater()
        del self.card_id_to_label[card.card_id]  # Remove the entry from the dictionary


        # Remove the Card instance
        self.cards.remove(card)
    
    def on_card_equip(self, card):
        """Handle the event when a card is equipped."""
        # Remove the card from the hand
        self.on_card_used(card)

        # Add the card to the ground
        self.player.ground.on_card_equip(card)

    def on_preview_clicked(self, event, card):
        """Handle the click event on a card's preview."""
        card.show_card()
    
