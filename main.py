import sys
import shutil
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from PIL import ImageGrab

from hand_layout import Ui_HandWidget

class Card(QWidget):
    def __init__(self, hand, name, label):
        super().__init__()
        self.hand = hand
        self.name = name
        self.label = label
        self.hand.destroyed.connect(self.close)
        self.init_ui()

    def init_ui(self):
        """Initialize the UI components for the Card."""
        self.setWindowTitle(self.name)
        self.layout = QVBoxLayout(self)

        # Create a QLabel to display the image
        self.image_label = QLabel(self)
        pixmap = QPixmap(f"{HandFolder}/{self.name}")
        self.image_label.setPixmap(pixmap)
        self.layout.addWidget(self.image_label)

        self.button = QPushButton('Use', self)
        self.button.clicked.connect(self.use_card)
        self.layout.addWidget(self.button)

    def use_card(self):
        """Use the card and move its file to the discard folder."""
        try:
            shutil.move(f"{HandFolder}/{self.name}", f"{DiscardFolder}/{self.name}")
        except Exception as e:
            print(f"Error moving card: {e}")
        self.hand.use_card(self)
        self.close()

    def is_visible(self):
        """Check if the card widget is currently visible."""
        return self.isVisible()




class Hand(QWidget):
    def __init__(self, player):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

         # Initialize attributes
        self.player = player
        self.numberofcards=0
        self.cards = []  # List to store Card objects
        self.image_labels = []

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Hand')

        # Layout
        self.layout = QVBoxLayout(self)
        self.image_layout = QHBoxLayout()
        self.layout.addLayout(self.image_layout)
    
        # Button
        self.button = QPushButton('Draw', self)
        self.button.clicked.connect(self.draw_card)
        self.layout.addWidget(self.button)

        
    def draw_card(self):
        """Draw a card and display its preview."""
        self.numberofcards += 1

        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        cardname = f"Card_{self.numberofcards}.png"
        location = f"{HandFolder}/{cardname}"
        screenshot.save(location)

        pixmap = QPixmap(location).scaled(int(width/3), int(height/3), Qt.AspectRatioMode.KeepAspectRatio)
        label = QLabel(self)
        label.setPixmap(pixmap)

        card = Card(hand=self, name=cardname, label=label)
        self.show_card(card)
        self.cards.append(card) # Add the card to the list

        label.mousePressEvent = lambda event, card=card: self.on_preview_clicked(event, card)
        self.image_labels.append(label)
        self.image_layout.addWidget(label)

    def use_card(self, card):
        # Remove the QLabel from the layout and list
        self.image_layout.removeWidget(card.label)
        self.image_labels.remove(card.label)
        card.label.deleteLater()

        # Remove the Card instance
        self.cards.remove(card)

    def show_card(self, card):
        """Display a specific card."""
        card.show()

    def on_preview_clicked(self, event, card):
        """Handle the click event on a card's preview."""
        if not card.is_visible():
            self.show_card(card)
    


class Ground(QWidget):
    def __init__(self, player):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.player = player
        self.numberofcards=0
        self.cards = []  # List to store Card objects

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Ground')

        # Layout
        self.layout = QVBoxLayout(self)

        
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


HandFolder = "HandCards"
DiscardFolder = "DiscardCards"
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
