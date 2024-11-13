from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, 
    QTableWidget, QLineEdit, QFormLayout, QTableWidgetItem, QHeaderView, QMessageBox, QStyle, 
    QGroupBox, QFrame, QButtonGroup, QRadioButton
)
from PySide6.QtGui import QDoubleValidator, QIcon, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
import qdarktheme
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)
# Apply the complete dark theme to your Qt App.
qdarktheme.setup_theme("auto")

main_icon = QIcon(resource_path("symbol_cvut_konturova_verze.ico"))

# Okno které počítá
class ProcessWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(main_icon)
        self.setWindowTitle("Výpočet skupiny provozů skladů")

        self.layout = QVBoxLayout()

        self._setup_riziko_groupbox()
        self._setup_q_inputs()
        self._setup_p_inputs()
        self._setup_surface_input()
        self._setup_calc_button()
        self._setup_result_groupbox()

        self.setLayout(self.layout)

    def _setup_riziko_groupbox(self):
        self.riziko_groupbox = QGroupBox("Požární riziko v požárním úseku určeno pomocí")
        self.riziko_groupbox.setFont(self._create_bold_font())
        self.riziko_groupbox.setToolTip("U požárních úseků, ve kterých bylo požární riziko určeno pomocí τe,\nse posuzuje jen průměrný tepelný výkon (q). U požárních úseků,\nve kterých bylo požární riziko určeno pomocí τ se posuzují obě kritéria,\npřičemž skupina provozů skladů se určí podle kritéria s nejvyšší skupinou.")
        
        self.riziko_layout = QVBoxLayout()
        self.riziko_layout.addWidget(QLabel("Je potřeba zaškrtnout jednu z možností"))
        
        self.taue = QRadioButton("τe ekvivalentní doby trvání požáru")
        self.tau = QRadioButton("τ pravděpodobné doby trvání požáru")
        
        self.riziko_button_group = QButtonGroup(self)
        self.riziko_button_group.addButton(self.taue)
        self.riziko_button_group.addButton(self.tau)
        
        self.riziko_layout.addWidget(self.taue)
        self.riziko_layout.addWidget(self.tau)
        
        self.riziko_groupbox.setLayout(self.riziko_layout)
        self.layout.addWidget(self.riziko_groupbox)

    def _setup_q_inputs(self):
        #TODO: kouknout jestli jde do setTool jde dát obrázek PNG/SVG
        self.q_label = QLabel("Vstupní hodnoty pro výpočet q")
        self.q_label.setFont(self._create_bold_font())
        self.q_label.setToolTip("Průměrný tepelný výkon q v MW∙m⁻² odpovídá průměrnému tepelnému výkonu dosaženému hořením skladovaného materiálu na 1 m² odhořívané plochy. V případě výskytu různých materiálů, se stanoví průměrné hodnoty v závislosti na jejich hmotnosti podle rovnice: <b>q=(((∑Mᵢ∙mᵢ)/∑Mᵢ)∙((∑Mᵢ∙kₚ₁ᵢ∙Hᵢ)/∑Mᵢ))/60</b>.")
        self.layout.addWidget(self.q_label)

        self.q_layout = QHBoxLayout()
        self.q_form_layout = QFormLayout()
        self.mi_input = self._create_double_line_edit("Hmotnost odhořelá z 1 m² povrchu za 1 minutu i-tého materiálu podle\npřílohy D ČSN 73 0804 a pro obalové materiály podle přílohy C ČSN 73 0845.")
        self.hi_input = self._create_double_line_edit("Normová hodnota výhřevnosti i-té hořlavé látky podle ČSN 73 0824.")
        self.kp1_input = self._create_double_line_edit("Součinitel vyjadřující podíl požární výhřevnosti Hₚ a výhřevnosti H téže i-té hořlavé látky, podle ČSN 73 0824.")
        self.mi2_input = self._create_double_line_edit("Hmotnost i-té hořlavé látky.")
        self.q_form_layout.addRow("mᵢ [kg·m⁻²·min⁻¹]:", self.mi_input)
        self.q_form_layout.addRow("Hᵢ [MJ·kg⁻¹]:", self.hi_input)
        self.q_form_layout.addRow("kₚ₁ᵢ [-]:", self.kp1_input)
        self.q_form_layout.addRow("Mᵢ [kg]:", self.mi2_input)
        self.q_layout.addLayout(self.q_form_layout)

        self.q_table = self._create_table(["mᵢ", "Hᵢ", "kₚ₁", "Mᵢ"], 4)
        self.q_layout.addWidget(self.q_table)
        self.layout.addLayout(self.q_layout)

        self._setup_q_buttons()

    def _setup_q_buttons(self):
        self.q_butts = QHBoxLayout()
        self.q_butt_plus = QPushButton("Přidat materiál")
        self.q_butt_minus = QPushButton("Odebrat poslední materiál")
        self.q_butts.addWidget(self.q_butt_plus)
        self.q_butts.addWidget(self.q_butt_minus)
        self.layout.addLayout(self.q_butts)

        self.q_butt_plus.clicked.connect(self.add_material_q)
        self.q_butt_minus.clicked.connect(self.remove_material_q)

    def _setup_p_inputs(self):
        self.layout.addWidget(self._create_divider())

        self.p_label = QLabel("Vstupní hodnoty pro výpočet p<sub>n</sub>")
        self.p_label.setFont(self._create_bold_font())
        self.p_label.setToolTip("Nahodilé požární zatížení p<sub>n</sub> v kg·m⁻² určené podle rovnice <b>p<sub>n</sub>=(∑Mᵢ∙Kᵢ)/S</b>, která odpovídá rovnici (5) ČSN 73 0804")
        self.layout.addWidget(self.p_label)
        
        self.p_layout = QHBoxLayout()
        self.p_form_layout = QFormLayout()
        self.m_input = self._create_double_line_edit("Hmotnost i-té hořlavé látky.")
        self.k_input = self._create_double_line_edit("Součinitel ekvivalentního množství dřeva i-tého druhu hořlavé látky podle ČSN 73 0824.")
        self.p_form_layout.addRow("Mᵢ [kg]:", self.m_input)
        self.p_form_layout.addRow("Kᵢ [-]:", self.k_input)
        self.p_layout.addLayout(self.p_form_layout)
        
        self.p_table = self._create_table(["Mᵢ", "Kᵢ"], 2)
        self.p_layout.addWidget(self.p_table)
        self.layout.addLayout(self.p_layout)
        
        self._setup_p_buttons()

    def _setup_p_buttons(self):
        self.p_butts = QHBoxLayout()
        self.p_butt_plus = QPushButton("Přidat materiál")
        self.p_butt_minus = QPushButton("Odebrat poslední materiál")
        self.p_butts.addWidget(self.p_butt_plus)
        self.p_butts.addWidget(self.p_butt_minus)
        self.layout.addLayout(self.p_butts)
        
        self.p_butt_plus.clicked.connect(self.add_material_p)
        self.p_butt_minus.clicked.connect(self.remove_material_p)

    def _setup_surface_input(self):
        self.layout.addWidget(self._create_divider())

        self.surface_line_edit = self._create_double_line_edit("Celková půdorysná plocha požárního úseku.")
        self.surface_layout = QFormLayout()
        self.surface_layout.addRow("S [m<sup>2</sup>]:", self.surface_line_edit)
        self.layout.addLayout(self.surface_layout)

    def _setup_calc_button(self):
        self.calc_butt = QPushButton("Vypočítat")
        self.calc_butt.setFont(self._create_bold_font())
        self.layout.addWidget(self.calc_butt, alignment=Qt.AlignCenter)
        self.calc_butt.clicked.connect(self.on_calc_butt_clicked)

    def _setup_result_groupbox(self):
        self.result_groupbox = QGroupBox("Výstupní hodnoty")
        self.result_groupbox.setFont(self._create_bold_font())
        
        self.result_layout = QVBoxLayout()
        
        self.q_result = self._create_readonly_line_edit()
        self.pn_result = self._create_readonly_line_edit()
        self.result_form_layout = QFormLayout()
        self.result_form_layout.addRow("q [MW·m<sup>-2</sup>]:", self.q_result)
        self.result_form_layout.addRow("p<sub>n</sub> [kg·m<sup>-2</sup>]:", self.pn_result)
        self.result_layout.addLayout(self.result_form_layout)
        
        self.skupina_result = self._create_readonly_line_edit()
        self.skupina_layout = QFormLayout()
        self.skupina_layout.addRow("<b>Skupina provozů skladů:</b>", self.skupina_result)
        self.result_layout.addLayout(self.skupina_layout)
        
        self.result_groupbox.setLayout(self.result_layout)
        self.layout.addWidget(self.result_groupbox)

    def _create_bold_font(self):
        font = self.font()
        font.setBold(True)
        return font

    def _create_double_line_edit(self, tooltip):
        line_edit = QLineEdit()
        line_edit.setValidator(QDoubleValidator())
        line_edit.setToolTip(tooltip)
        return line_edit

    def _create_readonly_line_edit(self):
        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        return line_edit

    def _create_table(self, headers, column_count):
        table = QTableWidget(self)
        table.setColumnCount(column_count)
        table.setHorizontalHeaderLabels(headers)
        for i in range(column_count):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        return table

    def _create_divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        return divider

    def add_material_q(self):
        self._add_material(self.q_table, [self.mi_input, self.hi_input, self.kp1_input, self.mi2_input])

    def remove_material_q(self):
        self._remove_material(self.q_table)

    def add_material_p(self):
        self._add_material(self.p_table, [self.m_input, self.k_input])

    def remove_material_p(self):
        self._remove_material(self.p_table)

    def _add_material(self, table, inputs):
        values = [input.text() for input in inputs]
        if all(values):
            self._insert_row_into_table(table, values)
            for input in inputs:
                input.clear()
        else:
            self._show_error("Chybějící hodnoty", "Všechny hodnoty musí být vyplněny.")

    def _insert_row_into_table(self, table, values):
        row_position = table.rowCount()
        table.insertRow(row_position)
        for i, value in enumerate(values):
            table.setItem(row_position, i, QTableWidgetItem(value))

    def _remove_material(self, table):
        row_position = table.rowCount()
        if row_position > 0:
            table.removeRow(row_position - 1)

    def _show_error(self, title, text):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setText(title)
        error_dialog.setInformativeText(text)
        error_dialog.setWindowTitle("Chyba")
        error_dialog.setWindowIcon(main_icon)
        error_dialog.exec()

    def on_calc_butt_clicked(self):
        self.calculate_q()
        try:
            self.calculate_p()
        except Exception:
            self.pn_result.setText("N/A")
        
        if self.taue.isChecked() or self.tau.isChecked():
            self.calculate_skupina_skladu()
        else:
            self._show_error("Chybějící určení požárního rizika", "Musí být zaškrtnuto alespoň jedno určení požárního rizika.")

    def calculate_q(self):
        mi2_sum = sum(float(self.q_table.item(row, 3).text().replace(',', '.')) for row in range(self.q_table.rowCount()))
        mi2_mi_sum = sum(float(self.q_table.item(row, 3).text().replace(',', '.')) * float(self.q_table.item(row, 0).text().replace(',', '.')) for row in range(self.q_table.rowCount()))
        mi2_kp1_Hi_sum = sum(float(self.q_table.item(row, 3).text().replace(',', '.')) * float(self.q_table.item(row, 2).text().replace(',', '.')) * float(self.q_table.item(row, 1).text().replace(',', '.')) for row in range(self.q_table.rowCount()))

        if mi2_sum != 0:
            q_value = (mi2_mi_sum/mi2_sum) * (mi2_kp1_Hi_sum/mi2_sum) / 60
            self.q_result.setText(f"{q_value:.3f}".replace('.', ','))
        else:
            self.q_result.setText("0")

    def calculate_p(self):
        surface_value = self.surface_line_edit.text().replace(',', '.')

        try:
            S = float(surface_value)
        except ValueError:
            if self.tau.isChecked():
                self._show_error("Chybějící hodnoty", "Všechny hodnoty musí být vyplněny.")
            else:
                self.pn_result.setText("N/A")
            return

        if self.p_table.rowCount() == 0:
            if self.tau.isChecked():
                self._show_error("Chybějící hodnoty", "Všechny hodnoty musí být vyplněny.")
            else:
                self.pn_result.setText("N/A")
            return

        pn_value = sum(float(self.p_table.item(row, 0).text().replace(',', '.')) * 
                       float(self.p_table.item(row, 1).text().replace(',', '.')) 
                       for row in range(self.p_table.rowCount())) / S

        self.pn_result.setText(f"{pn_value:.3f}".replace('.', ','))

    def calculate_skupina_skladu(self):
        if not (self.taue.isChecked() or self.tau.isChecked()):
            self._show_error("Chybějící určení požárního rizika", "Musí být zaškrtnuto alespoň jedno určení požárního rizika.")
            return

        q_value = float(self.q_result.text().replace(',', '.'))
        pn_value = float(self.pn_result.text().replace(',', '.')) if self.pn_result.text() != "N/A" else 0

        if self.taue.isChecked():
            self.skupina_result.setText(self._determine_skupina_taue(q_value))
        elif self.tau.isChecked():
            self.skupina_result.setText(self._determine_skupina_tau(q_value, pn_value))

    def _determine_skupina_taue(self, q_value):
        if q_value <= 0.05:
            return "I"
        elif q_value <= 0.1:
            return "II"
        elif q_value <= 0.2:
            return "III"
        elif q_value <= 0.4:
            return "IV"
        elif q_value <= 0.7:
            return "V"
        elif q_value <= 0.9:
            return "VI"
        elif q_value > 0.9:
            return "VII"
        return "N/A"

    def _determine_skupina_tau(self, q_value, pn_value):
        if q_value <= 0.05 and pn_value <= 90:
            return "I"
        elif q_value <= 0.1 and pn_value <= 180:
            return "II"
        elif q_value <= 0.2 and pn_value <= 270:
            return "III"
        elif q_value <= 0.4:
            return "IV"
        elif q_value <= 0.7:
            return "V"
        elif q_value <= 0.9:
            return "VI"
        elif q_value > 0.9:
            return "VII"
        return "N/A"

# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(main_icon)
        self.setWindowTitle("Skupina provozů skladů")

        # Main layout
        self.layout = QVBoxLayout()

        # Title
        self.tit_label = QLabel("Skupina provozů skladů")
        self.tit_label.setStyleSheet("QLabel { color: #0065bd; }")
        self.tit_label.setFont(self._create_font(30, True))
        self.tit_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.tit_label)

        # Info text
        self.info_label = QLabel("Program byl vytvořen v rámci diplomové práce.")
        self.info_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.info_label)

        # Department info
        self.kat_label = QLabel("České vysoké učení technické v Praze, Fakulta stavební \nKatedra betonových a zděných konstrukcí")
        self.kat_label.setFont(self._create_font(bold=True))
        self.kat_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.kat_label)

        # Logo
        self.logo = QSvgWidget(resource_path("symbol_cvut_konturova_verze.svg"))
        self.logo.setFixedSize(200, 153.85)
        self.layout.addWidget(self.logo, alignment=Qt.AlignCenter)

        # Start button
        self.start_butt = QPushButton("Spustit program")
        self.start_butt.clicked.connect(self.show_process_window)
        self.layout.addWidget(self.start_butt, alignment=Qt.AlignCenter)

        # Authors
        self.auth_label = QLabel("Autor práce: Bc. Kateřina Kráslová\nVedoucí práce: Ing. Martin Benýšek, Ph.D.\n2024")
        self.auth_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.auth_label)

        # Warning
        self.war_tit = QLabel("Autor nenese žádnou odpovědnost za škody plynoucí z použití tohoto programu.")
        self.war_tit.setStyleSheet("QLabel { color: red; }")
        self.war_tit.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.war_tit)

        # Libraries info
        self.lib_label = QLabel("Vytvořeno pomocí Python 3.11 a knihoven PySide6 pro PyQt5 a PyQt6.")
        self.lib_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout.addWidget(self.lib_label)

        # Fixed window size
        self.setFixedSize(QSize(495, 460))

        # Set the central widget of the Window.
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def _create_font(self, size=10, bold=False):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def show_process_window(self):
        self.hide()
        self.window = ProcessWindow()
        self.window.show()

# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.
