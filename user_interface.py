from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QWidget, QVBoxLayout, QHBoxLayout

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fruit Video Recognition - Login')
        self.setGeometry(100, 100, 400, 200)

        self.user_data = None

        # Login layout

        self.email_entry = QLineEdit(self)
        self.email_entry.setPlaceholderText('name@example.com')

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText('Password')
        self.password_entry.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.store_login)

        self.login_layout = QVBoxLayout()
        self.login_layout.addWidget(self.email_entry)
        self.login_layout.addWidget(self.password_entry)
        self.login_layout.addWidget(self.login_button)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.login_layout)
        self.setCentralWidget(self.central_widget)

    def store_login(self):
        email = self.email_entry.text()
        password = self.password_entry.text()
        assert (len(email) > 0) and (len(password) > 0), 'Empty email or password'
        self.user_data = (email, password)

    def retrieve_user_data(self):
        if not self.user_data:
            return None
        if not self.user_data[0] or not self.user_data[1]:
            return None
        return self.user_data

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Fruit Video Recognition - Video')

        # Layout to input a video file

        self.file_entry = QLineEdit(self)
        self.file_entry.setPlaceholderText('Example.avi')