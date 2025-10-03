import sys
from PySide6.QtWidgets import QApplication
from gui.login import Login

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = Login()
    login_window.show()
    sys.exit(app.exec())
