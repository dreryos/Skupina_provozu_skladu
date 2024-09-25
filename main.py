from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QTableWidget, QLineEdit, QFormLayout
from PySide6.QtSvgWidgets import QSvgWidget

# Only needed for access to command line arguments
# import sys

# Okno které počítá
class ProcessWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # Určení požárního rizika
        self.riziko_label = QLabel("Požární riziko v požárním úseku určeno pomocí")
        self.riziko_font = self.riziko_label.font()
        self.riziko_font.setBold(True)
        self.riziko_label.setFont(self.riziko_font)
        self.layout.addWidget(self.riziko_label)
        ## Checkboxy
        self.taue = QCheckBox("τe ekvivaletní doby trvání požáru")
        self.layout.addWidget(self.taue)
        self.tau = QCheckBox("τ ekvivaletní doby trvání požáru")
        self.layout.addWidget(self.tau)

        # Vstupní hodnoty pro q
        self.q_label = QLabel("Vstupní hodnoty pro výpočet q")
        self.q_font = self.q_label.font()
        self.q_font.setBold(True)
        self.q_label.setFont(self.q_font)
        self.layout.addWidget(self.q_label)
        ## Tabulka
        self.q_table = QTableWidget(self)
        self.q_table.setRowCount(3)
        self.q_table.setVerticalHeaderLabels(["mᵢ [kg·m⁻²·min⁻¹]", "Hᵢ [MJ·kg⁻¹]", "Mᵢ [kg]"])
        # TODO: přidávání materiálů a zarovnání tabulky na 3x5
        self.layout.addWidget(self.q_table)
        ## Tlačítka
        self.q_butts = QHBoxLayout()
        self.q_butt_plus = QPushButton("Přidat materiál")
        self.q_butt_minus = QPushButton("Odebrat poslední materiál")
        self.q_butts.addWidget(self.q_butt_plus)
        self.q_butts.addWidget(self.q_butt_minus)
        self.layout.addLayout(self.q_butts)

        # Vstupní hodnoty pro p_n
        self.p_label = QLabel("Vstupní hodnoty pro výpočet p<sub>n</sub>")
        self.p_font = self.p_label.font()
        self.p_font.setBold(True)
        self.p_label.setFont(self.p_font)
        self.layout.addWidget(self.p_label)
        ## Tabulka
        self.p_table = QTableWidget(self)
        self.p_table.setRowCount(2)
        self.p_table.setVerticalHeaderLabels(["Mᵢ [kg]", "Kᵢ"])
        # TODO: přidávání materiálů a zarovnání tabulky na 2x5
        self.layout.addWidget(self.p_table)
        ## Tlačítka
        self.p_butts = QHBoxLayout()
        self.p_butt_plus = QPushButton("Přidat materiál")
        self.p_butt_minus = QPushButton("Odebrat poslední materiál")
        self.p_butts.addWidget(self.p_butt_plus)
        self.p_butts.addWidget(self.p_butt_minus)
        self.layout.addLayout(self.p_butts)

        # Plocha
        self.surface_line_edit = QLineEdit()
        self.surface_layout = QFormLayout()
        self.surface_layout.addRow("S [m<sup>2</sup>]:", self.surface_line_edit)
        self.layout.addLayout(self.surface_layout)

        # Tlačítko pro výpočet
        self.calc_butt = QPushButton("Vypočítat")
        self.layout.addWidget(self.calc_butt, alignment=Qt.AlignCenter)

        # Výstupní hodnoty
        self.result_label = QLabel("Výstupní hodnoty")
        self.result_font = self.result_label.font()
        self.result_font.setBold(True)
        self.result_label.setFont(self.result_font)
        self.layout.addWidget(self.result_label)
        ## Výstupní hodnoty text
        self.q_result = QLineEdit()
        self.q_result.setReadOnly(True)
        self.pn_result = QLineEdit()
        self.pn_result.setReadOnly(True)
        self.result_layout = QFormLayout()
        self.result_layout.addRow("q [MW·m<sup>2</sup>]:", self.q_result)
        self.result_layout.addRow("p<sub>n</sub> [kg·m<sup>-2</sup>]:", self.pn_result)
        self.layout.addLayout(self.result_layout)

        # Skupina skladů
        self.skupina_result = QLineEdit()
        self.skupina_result.setReadOnly(True)
        self.skupina_layout = QFormLayout()
        self.skupina_layout.addRow("<b>Skupina provozů skladů:</b>", self.skupina_result)
        self.layout.addLayout(self.skupina_layout)
        
        self.setLayout(self.layout)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Skupina provozu skladů")

        # Horizontální layout
        self.layout = QVBoxLayout()

        # Text v hlavním okne
        ## Titulek
        self.tit_label = QLabel("Skupina provozu skladů")
        self.tit_label.setStyleSheet("QLabel { color: #0065bd; }")
        self.tit_font = self.tit_label.font()
        self.tit_font.setPointSize(30)
        self.tit_font.setBold(True)
        self.tit_label.setFont(self.tit_font)
        self.tit_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.layout.addWidget(self.tit_label)

        ## Info text
        self.info_label = QLabel("Program byl vytvořen v rámci diplomové práce.")
        self.info_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.kat_label = QLabel("České vysoké učení technické v Praze, Fakulta stavební \nKatedra betonových a zděných konstrukcí") # nový řádek pomocí \n
        self.kat_font = self.kat_label.font()
        self.kat_font.setBold(True)
        self.kat_label.setFont(self.kat_font)
        self.kat_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.kat_label)

        ## Logo
        self.logo = QSvgWidget("./symbol_cvut_konturova_verze.svg")
        self.logo.setFixedSize(200, 153.85)
        self.layout.addWidget(self.logo, alignment=Qt.AlignCenter)

        ## Tlačítko
        self.start_butt = QPushButton("Spustit program")
        self.start_butt.clicked.connect(self.show_process_window)
        self.layout.addWidget(self.start_butt, alignment=Qt.AlignCenter)

        ## Autoři
        self.auth_label = QLabel("Autor práce: Bc. Kateřina Kráslová\nVedoucí práce: Ing. Martin Benýšek, Ph.D.\n2024")
        self.auth_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.layout.addWidget(self.auth_label)

        ## Varování
        self.war_tit = QLabel("Autor nenese žádnou odpovědnost za škody plynoucí z použití tohoto programu.")
        self.war_tit.setStyleSheet("QLabel { color: red; }")
        self.war_tit.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.layout.addWidget(self.war_tit)

        ## Knihovny
        self.lib_label = QLabel("Vytvořeno pomocí Python 3.11 a knihoven PySide6 pro PyQt5 a PyQt6.")
        self.lib_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )
        self.layout.addWidget(self.lib_label)

        # Uzamknutá velikost okna
        self.setFixedSize(QSize(495, 460))

        # Set the central widget of the Window.
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    # Funkce otevírající nové okno a zavře hlavní okno    
    def show_process_window(self, checked):
        self.hide()
        self.window = ProcessWindow()
        self.window.show()



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
