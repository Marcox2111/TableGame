from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from config import CardFolder


class Card(QWidget):
    def __init__(self, parent, context, card_id):
        super().__init__()
        self.parent = parent
        self.context = context
        self.card_id = card_id
        self.image_path=f"{CardFolder}/Card_{self.card_id}.png"
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
        self.button.clicked.connect(self.on_use_clicked)
        self.layout.addWidget(self.button)

        self.equip_button = QPushButton('Equip', self)
        self.equip_button.clicked.connect(self.on_equip_clicked)
        self.layout.addWidget(self.equip_button)

        if self.context == 'ground':
            self.equip_button.setEnabled(False)  # Disable the equip button

    def get_image(self):
        return QPixmap(self.image_path)
    
    def on_use_clicked(self):
        self.parent.on_card_used(self)
        self.close()

    def on_equip_clicked(self):
        self.parent.on_card_equip(self)
        self.close()
    
    def show_card(self):
        """Display the card."""
        if not self.isVisible():
            self.show()
    