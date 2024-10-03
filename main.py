from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QTableWidget, QLineEdit, QFormLayout, QTableWidgetItem
from PySide6.QtGui import QDoubleValidator
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

        # Formulář pro vstupní hodnoty a tabulka vedle sebe
        self.q_layout = QHBoxLayout()

        # Formulář pro vstupní hodnoty
        self.q_form_layout = QFormLayout()
        self.mi_input = QLineEdit()
        self.hi_input = QLineEdit()
        self.mi2_input = QLineEdit()
        self.mi_input.setValidator(QDoubleValidator())
        self.hi_input.setValidator(QDoubleValidator())
        self.mi2_input.setValidator(QDoubleValidator())
        self.q_form_layout.addRow("mᵢ [kg·m⁻²·min⁻¹]:", self.mi_input)
        self.q_form_layout.addRow("Hᵢ [MJ·kg⁻¹]:", self.hi_input)
        self.q_form_layout.addRow("Mᵢ [kg]:", self.mi2_input)
        self.q_layout.addLayout(self.q_form_layout)

        # Tabulka
        self.q_table = QTableWidget(self)
        self.q_table.setRowCount(0)
        self.q_table.setColumnCount(3)
        self.q_table.setHorizontalHeaderLabels(["mᵢ", "Hᵢ", "Mᵢ"])
        self.q_layout.addWidget(self.q_table)

        self.layout.addLayout(self.q_layout)

        # Tlačítka
        self.q_butts = QHBoxLayout()
        self.q_butt_plus = QPushButton("Přidat materiál")
        self.q_butt_minus = QPushButton("Odebrat poslední materiál")
        self.q_butts.addWidget(self.q_butt_plus)
        self.q_butts.addWidget(self.q_butt_minus)
        self.layout.addLayout(self.q_butts)

        # Přidání materiálu do tabulky
        self.q_butt_plus.clicked.connect(self.add_material_q)
        self.q_butt_minus.clicked.connect(self.remove_material_q)


        # Vstupní hodnoty pro p_n
        self.p_label = QLabel("Vstupní hodnoty pro výpočet p<sub>n</sub>")
        self.p_font = self.p_label.font()
        self.p_font.setBold(True)
        self.p_label.setFont(self.p_font)
        self.layout.addWidget(self.p_label)
        
        # Formulář pro vstupní hodnoty a tabulka vedle sebe
        self.p_layout = QHBoxLayout()
        
        # Formulář pro vstupní hodnoty
        self.p_form_layout = QFormLayout()
        self.m_input = QLineEdit()
        self.k_input = QLineEdit()
        self.m_input.setValidator(QDoubleValidator())
        self.k_input.setValidator(QDoubleValidator())
        self.p_form_layout.addRow("Mᵢ [kg]:", self.m_input)
        self.p_form_layout.addRow("Kᵢ:", self.k_input)
        self.p_layout.addLayout(self.p_form_layout)
        
        # Tabulka
        #TODO: aby tabulka nevypadala jako tak divně
        self.p_table = QTableWidget(self)
        self.p_table.setRowCount(0)
        self.p_table.setColumnCount(2)
        self.p_table.setHorizontalHeaderLabels(["Mᵢ", "Kᵢ"])
        self.p_layout.addWidget(self.p_table)
        
        self.layout.addLayout(self.p_layout)
        
        # Tlačítka
        self.p_butts = QHBoxLayout()
        self.p_butt_plus = QPushButton("Přidat materiál")
        self.p_butt_minus = QPushButton("Odebrat poslední materiál")
        self.p_butts.addWidget(self.p_butt_plus)
        self.p_butts.addWidget(self.p_butt_minus)
        self.layout.addLayout(self.p_butts)
        
        # Přidání materiálu do tabulky
        self.p_butt_plus.clicked.connect(self.add_material_p)
        self.p_butt_minus.clicked.connect(self.remove_material_p)
        

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

    def add_material_q(self):
        mi_value = self.mi_input.text().replace(",", ".")
        hi_value = self.hi_input.text().replace(",", ".")
        mi2_value = self.mi2_input.text().replace(",", ".")
        if mi_value and hi_value and mi2_value:
            self._insert_row_into_q_table(mi_value, hi_value, mi2_value)

    def _insert_row_into_q_table(self, mi_value, hi_value, mi2_value):
        row_position = self.q_table.rowCount()
        self.q_table.insertRow(row_position)
        self.q_table.setItem(row_position, 0, QTableWidgetItem(mi_value))
        self.q_table.setItem(row_position, 1, QTableWidgetItem(hi_value))
        self.q_table.setItem(row_position, 2, QTableWidgetItem(mi2_value))
        self.mi_input.clear()
        self.hi_input.clear()
        self.mi2_input.clear()

    def remove_material_q(self):
        row_position = self.q_table.rowCount()
        if row_position > 0:
            self.q_table.removeRow(row_position - 1)

    def add_material_p(self):
        m_value = self.m_input.text().replace(",", ".")
        k_value = self.k_input.text().replace(",", ".")
        if m_value and k_value:
            row_position = self.p_table.rowCount()
            self.p_table.insertRow(row_position)
            self.p_table.setItem(row_position, 0, QTableWidgetItem(m_value))
            self.p_table.setItem(row_position, 1, QTableWidgetItem(k_value))
            self.m_input.clear()
            self.k_input.clear()
        
    def remove_material_p(self):
        row_position = self.p_table.rowCount()
        if row_position > 0:
            self.p_table.removeRow(row_position - 1)


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
