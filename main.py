from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QLabel
from PySide6.QtSvgWidgets import QSvgWidget

# Only needed for access to command line arguments
# import sys

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Skupina provozu skladů")

        # Horizontální layout
        layout = QVBoxLayout()

        # Text v hlavním okne
        ## Titulek
        tit_label = QLabel("Skupina provozu skladů")
        tit_label.setStyleSheet("QLabel { color: #007ac3; }")
        tit_font = tit_label.font()
        tit_font.setPointSize(30)
        tit_font.setBold(True)
        tit_label.setFont(tit_font)
        tit_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(tit_label)

        ## Info text
        info_label = QLabel("Program byl vytvořen v rámci diplomové práce.")
        info_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        kat_label = QLabel("České vysoké učení technické v Praze, Fakulta stavební \nKatedra betonových a zděných konstrukcí") # nový řádek pomocí \n
        kat_font = kat_label.font()
        kat_font.setBold(True)
        kat_label.setFont(kat_font)
        kat_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(info_label)
        layout.addWidget(kat_label)

        ## Logo
        logo = QSvgWidget("./symbol_cvut_konturova_verze.svg")
        logo.setFixedSize(200, 153.85)
        layout.addWidget(logo, alignment=Qt.AlignCenter)

        ## Tlačítko
        start_but = QPushButton("Spustit program")
        layout.addWidget(start_but, alignment=Qt.AlignCenter)

        ## Autoři
        auth_label = QLabel("Autor práce: Bc. Kateřina Kráslová\nVedoucí práce: Ing. Martin Benýšek, Ph.D.\n2024")
        auth_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(auth_label)

        ## Varování
        war_tit = QLabel("Autor nenese žádnou odpovědnost za škody plynoucí z použití tohoto programu.")
        war_tit.setStyleSheet("QLabel { color: red; }")
        war_tit.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(war_tit)

        ## Knihovny
        lib_label = QLabel("Vytvořeno pomocí Python 3.11 a knihoven PySide6 pro PyQt5 a PyQt6.")
        lib_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(lib_label)

        # Uzamknutá velikost okna
        self.setFixedSize(QSize(495, 460))

        # Set the central widget of the Window.
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication([])

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
