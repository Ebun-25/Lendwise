from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QHBoxLayout, QFrame, QDialog
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from logic.checkout import checkout_item
from logic.returns import return_item
from logic.fines import list_fines
from logic.overdue import check_overdue
from logic.search import find_items
from logic.reports import view_reports
from gui.register_user_dialog import RegisterUserDialog


class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("📚 LendWise Library System")
        self.setGeometry(100, 100, 480, 400)
        self.setStyleSheet(self.dark_theme())

        # ===== Layouts =====
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # ===== Header =====
        title = QLabel("📘 LendWise System")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        main_layout.addWidget(title)

        subtitle = QLabel("Manage Checkouts, Returns & Fines Easily")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setFont(QFont("Segoe UI", 10))
        main_layout.addWidget(subtitle)

        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(divider)

        # ===== Input Fields =====
        patron_layout = QHBoxLayout()
        patron_label = QLabel("Patron ID:")
        patron_label.setFont(QFont("Segoe UI", 10))
        self.patron_input = QLineEdit()
        self.patron_input.setPlaceholderText("Enter Patron ID")
        patron_layout.addWidget(patron_label)
        patron_layout.addWidget(self.patron_input)
        main_layout.addLayout(patron_layout)

        item_layout = QHBoxLayout()
        item_label = QLabel("Item ID:")
        item_label.setFont(QFont("Segoe UI", 10))
        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Enter Item ID or Keyword")
        item_layout.addWidget(item_label)
        item_layout.addWidget(self.item_input)
        main_layout.addLayout(item_layout)

        # ===== Buttons =====
        buttons = [
            ("Checkout Item", self.checkout),
            ("Return Item", self.return_item_action),
            ("View Fines", self.show_fines),
            ("Check Overdue Loans", self.check_overdue),
            ("Search Items", self.search_items),
            ("View Reports", self.view_reports),
        ]

        for text, action in buttons:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(action)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
            """)
            main_layout.addWidget(btn)

        # ===== Librarian-Only Features =====
        if self.user.role == "librarian":
            btn_register = QPushButton("➕ Register Patron")
            btn_register.setCursor(Qt.PointingHandCursor)
            btn_register.clicked.connect(self.open_register_dialog)
            btn_register.setStyleSheet("""
                QPushButton {
                    background-color: #16a34a;
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #15803d;
                }
            """)
            main_layout.addWidget(btn_register)

        # ===== Result Label =====
        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("color: #fbbf24; font-size: 13px;")
        main_layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # ===== Helper Functions =====
    def open_register_dialog(self):
        dlg = RegisterUserDialog(self)
        dlg.exec()

    # ===== Functional Logic =====
    def checkout(self):
        patron_id = self.patron_input.text().strip()
        item_id = self.item_input.text().strip()
        if not patron_id or not item_id:
            self.result_label.setText("⚠️ Please enter both Patron ID and Item ID.")
            return
        result = checkout_item(int(patron_id), int(item_id))
        self.result_label.setText(result)

    def return_item_action(self):
        item_id = self.item_input.text().strip()
        if not item_id:
            self.result_label.setText("⚠️ Please enter the Loan/Item ID to return.")
            return
        result = return_item(int(item_id))
        self.result_label.setText(result)

    def search_items(self):
        keyword = self.item_input.text().strip()
        if not keyword:
            self.result_label.setText("⚠️ Please enter a search keyword.")
            return
        results = find_items(keyword)
        self.result_label.setText("\n".join(results))

    def view_reports(self):
        reports = view_reports()
        self.result_label.setText("\n".join(reports))

    def show_fines(self):
        fines = list_fines()
        self.result_label.setText("\n".join(fines) if fines else "No fines found.")

    def check_overdue(self):
        result = check_overdue()
        self.result_label.setText(result)

    def dark_theme(self):
        return """
        QWidget {
            background-color: #1e293b;
            color: #e2e8f0;
        }
        QLineEdit {
            background-color: #334155;
            color: #f8fafc;
            border: 1px solid #475569;
            border-radius: 4px;
            padding: 6px;
        }
        QLabel {
            color: #e2e8f0;
        }
        """


if __name__ == "__main__":
    from gui.login_dialog import LoginDialog

    app = QApplication([])

    dlg = LoginDialog()
    if dlg.exec() == QDialog.Accepted:
        user = dlg.user
        window = MainWindow(user)
        window.setWindowTitle(f"📚 LendWise - Logged in as {user.name} ({user.role})")
        window.show()
        app.exec()
