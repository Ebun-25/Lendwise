from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from backend.repository import create_user

class RegisterUserDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("➕ Register Patron")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Full Name:"))
        self.name = QLineEdit()
        layout.addWidget(self.name)

        layout.addWidget(QLabel("Email:"))
        self.email = QLineEdit()
        layout.addWidget(self.email)

        layout.addWidget(QLabel("Phone:"))
        self.phone = QLineEdit()
        layout.addWidget(self.phone)

        btn_register = QPushButton("Register Patron")
        btn_register.clicked.connect(self.register_user)
        layout.addWidget(btn_register)

        self.setLayout(layout)

    def register_user(self):
        name = self.name.text().strip()
        email = self.email.text().strip()
        phone = self.phone.text().strip()

        if not all([name, email]):
            QMessageBox.warning(self, "Error", "Name and Email are required.")
            return

        try:
            create_user(name, email, phone, role="patron")
            QMessageBox.information(self, "Success", f"Patron '{name}' registered successfully!")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to register user.\n{e}")
