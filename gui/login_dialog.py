from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton
from backend.repository import authenticate

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LendWise Login")
        layout = QVBoxLayout()

        # Input fields
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        # Status + button
        self.status = QLabel("")
        btn = QPushButton("Login")
        btn.clicked.connect(self.try_login)

        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(btn)
        layout.addWidget(self.status)
        self.setLayout(layout)

        self.user = None

    def try_login(self):
        """Attempt login using email and password."""
        u = authenticate(self.email.text().strip(), self.password.text().strip())
        if u:
            self.user = u
            self.accept()
        else:
            self.status.setText("❌ Invalid credentials.")
