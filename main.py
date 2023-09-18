import sys
import shutil
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from PIL import ImageGrab

from hand_layout import Ui_Hand
from bang_ground_layout import Ui_Bang_Ground


class Card(QWidget):
    def __init__(self, context, card_id):
        super().__init__()
        self.context = context
        self.card_id = card_id
        self.image_path=f"CardFolder/Card_{self.card_id}.png"
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components for the Card."""
        self.setWindowTitle(f"Card_{self.card_id}")
        self.layout = QVBoxLayout(self)

        # Create a QLabel to display the image
        self.image_label = QLabel(self)
        pixmap = self.get_image()
        self.image_label.setPixmap(pixmap)
        self.layout.addWidget(self.image_label)

        self.button = QPushButton('Use', self)
        self.button.clicked.connect(self.use_card)
        self.layout.addWidget(self.button)

        self.equip_button = QPushButton('Equip', self)
        self.equip_button.clicked.connect(self.equip_card)
        self.layout.addWidget(self.equip_button)

        if self.context == 'ground':
            self.equip_button.setEnabled(False)  # Disable the equip button

    def get_image(self):
        return QPixmap(self.image_path)

    def use_card(self):
        """Use the card and move its file to the discard folder."""
        self.close()

    def equip_card(self):
        
        self.close()
    
    def show_card(self):
        """Display the card."""
        if not self.isVisible():
            self.show()
    

 

class Hand(QWidget, Ui_Hand):
    card_counter=0

    def __init__(self, player):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

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

        card = Card(card_id=card_id, context='hand')
        card.button.clicked.connect(lambda: self.on_card_used(card))  # Connect the use_card button click to on_card_used
        card.equip_button.clicked.connect(lambda: self.on_card_equip(card))  # Connect the equip button click to on_card_equip

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
    


class Ground(QWidget,Ui_Bang_Ground):
    def __init__(self, player):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
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
        card.equip_button.setEnabled(False)  # Disable the equip button
        card.button.clicked.connect(lambda: self.on_card_used(card))  # Connect the use_card button click to on_card_used

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

# TODO Il metodo on card used applicarlo alla classe game piuttosto che ai singoli environment
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

        
class Player:
    def __init__(self):
        self.hand = Hand(player=self)
        self.ground = Ground(player=self)  # Each player has their own ground
        self.show_hand()
        self.show_ground()        

    def show_hand(self):
        self.hand.show()

    def show_ground(self):
        self.ground.show()


class Game:
    def __init__(self):
        self.player = Player()
        self.used_cards = set()

    def use_card(self, card):
        self.used_cards.add(card.card_id)

    def is_card_used(self, card):
        return card.card_id in self.used_cards


CardFolder = "CardFolder"
width=300
height=500
x1=0
y1=0
x2=width+x1
y2=height+y1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec())
