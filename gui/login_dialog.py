from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from backend.repository import authenticate


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 LendWise Login")
        self.setFixedSize(350, 280)
        self.setStyleSheet(self.dark_theme())

        # ==== Layout ====
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(15)

        # ==== Title ====
        title = QLabel("🔐 LendWise Login")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #93c5fd;")
        layout.addWidget(title)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        layout.addWidget(divider)

        # ==== Input Fields ====
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email Address")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(self.email)
        layout.addWidget(self.password)

        # ==== Login Button ====
        btn = QPushButton("Login")
        btn.clicked.connect(self.try_login)
        layout.addWidget(btn)

        # ==== Status Label ====
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet("color: #fbbf24; font-size: 13px;")
        layout.addWidget(self.status)

        self.setLayout(layout)
        self.user = None

    # ==== Login Function ====
    def try_login(self):
        u = authenticate(self.email.text().strip(), self.password.text().strip())
        if u:
            self.user = u
            self.accept()
        else:
            self.status.setText("❌ Invalid credentials.")

    # ==== Theme ====
    def dark_theme(self):
        return """
        QDialog {
            background-color: #1e293b;
            color: #e2e8f0;
            border-radius: 10px;
        }
        QLineEdit {
            background-color: #334155;
            color: #f8fafc;
            border: 1px solid #475569;
            border-radius: 5px;
            padding: 8px;
        }
        QPushButton {
            background-color: #3b82f6;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            padding: 8px 16px;
        }
        QPushButton:hover {
            background-color: #2563eb;
        }
        QLabel {
            color: #e2e8f0;
        }
        """
