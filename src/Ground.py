from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from src.Card import Card
from ui.bang_ground_layout import Ui_Bang_Ground
from config import CardFolder,width, height

class Ground(QWidget,Ui_Bang_Ground):
    def __init__(self, player):
        super().__init__()
        self.setupUi(self)
        self.player = player
        self.cards = []  # List to store Card objects
        self.card_id_to_label = {}  # Dictionary to map card IDs to labels
        
        self.start_hp()

    def start_hp(self):
        self.heart_image = QPixmap("resources/LifePoints.png")
        self.hp_labels = [self.hpLabel1, self.hpLabel2, self.hpLabel3, self.hpLabel4, self.hpLabel5]

        for label in self.hp_labels:
            label.setPixmap(self.heart_image)
            label.mousePressEvent = lambda event, label=label: self.toggle_hp(event, label)



    def toggle_hp(self, event, label):
        """Toggle the visibility of the clicked QLabel."""
        if isinstance(label, QLabel):
            if label.pixmap() and not label.pixmap().isNull():  # If the label currently has a pixmap
                print(f"Sender: {self}")
                label.setPixmap(QPixmap())  # Set an empty pixmap
            else:
                label.setPixmap(self.heart_image)  # Set the original pixmap

    def on_card_equip(self, card):
        location = f"{CardFolder}/Card_{card.card_id}.png"
        card.context = 'ground'
        card.parent = self
        card.equip_button.setEnabled(False)  # Disable the equip button

        pixmap = QPixmap(location).scaled(int(width/3), int(height/3), Qt.AspectRatioMode.KeepAspectRatio)
        label = QLabel(self)
        label.setPixmap(pixmap)

        self.card_id_to_label[card.card_id] = label

        self.cards.append(card) # Add the card to the list

        label.mousePressEvent = lambda event, card=card: self.on_preview_clicked(event, card)
        if card.card_id == 1:
            self.charLayout.addWidget(label)
            label.setPixmap(QPixmap(location).scaled(int(width/2), int(height/2), Qt.AspectRatioMode.KeepAspectRatio))
        else:
            self.equipLayout.addWidget(label)


    def on_card_used(self, card):
        """Handle the event when a card is used."""
        label_to_remove = self.card_id_to_label.get(card.card_id)

        # Remove the QLabel from the layout and list
        self.equipLayout.removeWidget(label_to_remove)
        label_to_remove.deleteLater()
        del self.card_id_to_label[card.card_id]  # Remove the entry from the dictionary
        # Remove the Card instance
        self.cards.remove(card)

    def on_preview_clicked(self, event, card):
        """Handle the click event on a card's preview."""
        card.show_card()