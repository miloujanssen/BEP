"""The main application"""
from PySide6.QtCore import Slot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QMessageBox
from project.ui.output_BEP import Ui_Form
from project.back_end.functies import Functies
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import ScalarFormatter
matplotlib.use('Qt5Agg')


class Application(QMainWindow):
    """Main application"""
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        #Stel de layout van de 4 frames in
        self.frame_1_layout = QVBoxLayout()
        self.ui.frame_1.setLayout(self.frame_1_layout)
        self.frame_3_layout = QVBoxLayout()
        self.ui.frame_3.setLayout(self.frame_3_layout)
        self.frame_4_layout = QVBoxLayout()
        self.ui.frame_4.setLayout(self.frame_4_layout)
        self.frame_5_layout = QVBoxLayout()
        self.ui.frame_5.setLayout(self.frame_5_layout)

        #Plot de grafieken als er op PLOT geklikt wordt
        self.ui.pushButton_start.clicked.connect(self.plot_turbines)
        self.ui.pushButton_start.clicked.connect(self.plot_zeta_z)
        self.ui.pushButton_start.clicked.connect(self.plot_debiet)
        self.ui.pushButton_start.clicked.connect(self.plot_vermogen)
        self.ui.pushButton_start.clicked.connect(self.aanbeveling_turbines)

        #Opent een nieuwe window als er op de betreffende knop wordt geklikt
        self.ui.pushButton_start_2.clicked.connect(self.open_turbines)
        self.ui.pushButton_start_4.clicked.connect(self.open_zeta_z)
        self.ui.pushButton_start_3.clicked.connect(self.open_debiet)
        self.ui.pushButton_start_5.clicked.connect(self.open_vermogen)

    def open_turbines(self):
        """Functie voor het groter laten zien van de turbine grafiek"""
        A_t = float(self.ui.A_t.text())
        A_b = float(self.ui.A_b.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        g = 9.81
        rho = 1000
        xi_v = float(self.ui.xi_v.text())
        xi_t = float(self.ui.xi_t.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        a_rel = a_M2 / a_S2
        periode = 29.53 * 24 * 3600
        energie_per_turbine = []
        tijd = np.linspace(0, periode, 10000)

        F = float(Functies.bereken_F(self, a_rel))
        range_kijken = self.ui.spinBox.value()

        for i in range(1, range_kijken + 1):
            lmbda = Functies.lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, i)
            mu_M2 = float(Functies.bereken_mu_M2(self, omega_M2, a_M2, lmbda, F))
            mu_S2 = float(Functies.bereken_mu_S2(self, omega_S2, lmbda, F, a_M2))

            theta_M2 = float(Functies.bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F))
            theta_S2 = float(Functies.bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2))

            delta_h = Functies.bereken_delta_h(self, tijd, mu_M2, mu_S2, a_M2, a_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2)

            energie_turb = Functies.energie_berekenen(self, delta_h, rho, g, A_t, xi_v, xi_t, i)
            energie_per_turbine.append(energie_turb)
        
        plt.bar(range(1, range_kijken + 1), energie_per_turbine, align='center', edgecolor='black')
        plt.xlabel('Aantal turbines')
        plt.ylabel('Totale energie opgewekt (Joule)')
        plt.title('Energie opbrengst per aantal turbines')
        plt.xticks(range(1, range_kijken + 1))
        plt.grid(True)
        plt.show()

    @Slot()
    def plot_turbines(self):
        """Plot de turbine grafiek in de frame"""
        A_t = float(self.ui.A_t.text())
        A_b = float(self.ui.A_b.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        g = 9.81
        rho = 1000
        xi_v = float(self.ui.xi_v.text())
        xi_t = float(self.ui.xi_t.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        a_rel = a_M2 / a_S2
        periode = 29.53 * 24 * 3600
        energie_per_turbine = []
        tijd = np.linspace(0, periode, 10000)

        F = float(Functies.bereken_F(self, a_rel))
        range_kijken = self.ui.spinBox.value()

        layout = self.ui.frame_1.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        for i in range(1, range_kijken + 1):
            lmbda = Functies.lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, i)
            mu_M2 = float(Functies.bereken_mu_M2(self, omega_M2, a_M2, lmbda, F))
            mu_S2 = float(Functies.bereken_mu_S2(self, omega_S2, lmbda, F, a_M2))
            theta_M2 = float(Functies.bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F))
            theta_S2 = float(Functies.bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2))
            delta_h = Functies.bereken_delta_h(self, tijd, mu_M2, mu_S2, a_M2, a_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2)

            energie_turb = Functies.energie_berekenen(self, delta_h, rho, g, A_t, xi_v, xi_t, i)
            energie_per_turbine.append(energie_turb)

        fig = plt.figure(figsize=(2,2))
        ax = fig.add_subplot(111)
        ax.bar(range(1, range_kijken + 1), energie_per_turbine, align='center', edgecolor='black')

        plt.subplots_adjust(left=0.15, right=0.85, top=0.8, bottom=0.2)
        ax.set_xlabel('Aantal turbines')
        ax.set_ylabel('Energie (Joule)')
        ax.set_title("Energie opbrengst per aantal turbines")
        canvas = FigureCanvas(fig)
       
        layout.addWidget(canvas)
        self.ui.frame_1.setLayout(layout)
        plt.close(fig)
  
    def open_zeta_z(self):
        """Functie voor het groter laten zien van de waterstand grafiek"""
        A0 = float(self.ui.A_0.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        periode = 29.53 * 24 * 3600
        tijd = np.linspace(0, periode, 10000)

        self.zeta_z = Functies.bereken_zeta_z(self, tijd, A0, a_M2, omega_M2, phi_M2, a_S2, omega_S2, phi_S2)

        plt.plot(tijd, self.zeta_z)
        plt.xlabel('Tijd (seconden)')
        plt.ylabel('Waterhoogte (meter)')
        plt.title('Waterhoogte op zee over een periode van 14.77 dagen')
        plt.grid(True)
        plt.show()

    @Slot()
    def plot_zeta_z(self):
        """Plot de waterstand op zee in de frame"""
        A0 = float(self.ui.A_0.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        periode = 29.53 * 24 * 3600
        tijd = np.linspace(0, periode, 10000)

        layout = self.ui.frame_4.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        self.zeta_z = Functies.bereken_zeta_z(self, tijd, A0, a_M2, omega_M2, phi_M2, a_S2, omega_S2, phi_S2)

        fig = plt.figure(figsize=(2,2))
        ax = fig.add_subplot(111)
        ax.plot(tijd, self.zeta_z)
        plt.subplots_adjust(left=0.15, right=0.85, top=0.8, bottom=0.2)
        ax.set_xlabel('Tijd (seconden)')
        ax.set_ylabel('Waterhoogte op zee (meter)')
        ax.set_title("Waterhoogte op zee over een periode van 14.77 dagen")
        canvas = FigureCanvas(fig)

        layout.addWidget(canvas)
        self.ui.frame_4.setLayout(layout)
        plt.close(fig)


    def open_debiet(self):
        """Functie voor het groter laten zien van de debiet grafiek"""
        periode = 29.53 * 24 * 3600
        A_t = float(self.ui.A_t.text())
        A_b = float(self.ui.A_b.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        tijd = np.linspace(0, periode, 10000)
        g = 9.81
        xi_v = float(self.ui.xi_v.text())
        xi_t = float(self.ui.xi_t.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        a_rel = a_M2 / a_S2

        lmbda = Functies.lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, 1)
        F = float(Functies.bereken_F(self, a_rel))
        mu_M2 = float(Functies.bereken_mu_M2(self, omega_M2, a_M2, lmbda, F))
        mu_S2 = float(Functies.bereken_mu_S2(self, omega_S2, lmbda, F, a_M2))

        theta_M2 = float(Functies.bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F))
        theta_S2 = float(Functies.bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2))

        term = Functies.delta_h_over_sqrt_delta_h(self, tijd, F, a_M2, mu_M2, a_S2, mu_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2) 
        debiet = Functies.bereken_debiet(self, A_t, g, xi_v, xi_t, 1, term)
        plt.plot(tijd, debiet)
        plt.xlabel('Tijd (seconden)')
        plt.ylabel('Debiet (meter^3/s)')
        plt.title('Debiet voor 1 turbine over een periode van 14.77 dagen')
        plt.grid(True)
        plt.show()

    @Slot()
    def plot_debiet(self):
        """Plot het debiet in de frame"""
        periode = 29.53 * 24 * 3600
        A_t = float(self.ui.A_t.text())
        A_b = float(self.ui.A_b.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        tijd = np.linspace(0, periode, 10000)
        g = 9.81
        xi_v = float(self.ui.xi_v.text())
        xi_t = float(self.ui.xi_t.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        a_rel = a_M2 / a_S2

        layout = self.ui.frame_3.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        lmbda = Functies.lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, 1)
        F = float(Functies.bereken_F(self, a_rel))
        mu_M2 = float(Functies.bereken_mu_M2(self, omega_M2, a_M2, lmbda, F))
        mu_S2 = float(Functies.bereken_mu_S2(self, omega_S2, lmbda, F, a_M2))

        theta_M2 = float(Functies.bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F))
        theta_S2 = float(Functies.bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2))

        term = Functies.delta_h_over_sqrt_delta_h(self, tijd, F, a_M2, mu_M2, a_S2, mu_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2) 
        debiet = Functies.bereken_debiet(self, A_t, g, xi_v, xi_t, 1, term)
        fig = plt.figure(figsize=(2,2))

        ax = fig.add_subplot(111)
        ax.plot(tijd, debiet)
        plt.subplots_adjust(left=0.15, right=0.85, top=0.8, bottom=0.2)
        ax.set_xlabel('Tijd (seconden)')
        ax.set_ylabel('Debiet (meter^3/s)')
        ax.set_title("Debiet over een periode van 14.77 dagen")
        canvas = FigureCanvas(fig)

        layout.addWidget(canvas)
        self.ui.frame_3.setLayout(layout)
        plt.close(fig)

    def open_vermogen(self):
        """Functie voor het groter laten zien van de vermogen grafiek"""
        periode = 29.53 * 24 * 3600
        A_t = float(self.ui.A_t.text())
        A_b = float(self.ui.A_b.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        tijd = np.linspace(0, periode, 10000)
        g = 9.81
        xi_v = float(self.ui.xi_v.text())
        xi_t = float(self.ui.xi_t.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        a_rel = a_M2 / a_S2
        rho = 1000

        lmbda = Functies.lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, 1)
        F = float(Functies.bereken_F(self, a_rel))
        mu_M2 = float(Functies.bereken_mu_M2(self, omega_M2, a_M2, lmbda, F))
        mu_S2 = float(Functies.bereken_mu_S2(self, omega_S2, lmbda, F, a_M2))

        theta_M2 = float(Functies.bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F))
        theta_S2 = float(Functies.bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2))

        verval = Functies.bereken_delta_h(self, tijd, mu_M2, mu_S2, a_M2, a_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2)
        vermogen = Functies.bereken_vermogen(self, rho, g, A_t, xi_v, xi_t, verval, 1)

        plt.plot(tijd, vermogen)
        plt.xlabel('Tijd (seconden)')
        plt.ylabel('Vermogen (Watt)')
        plt.title('Vermogen van 1 turbine over een periode van 14.77 dagen')
        plt.grid(True)
        plt.show()


    @Slot()
    def plot_vermogen(self):
        """Plot het vermogen in de frame"""
        periode = 29.53 * 24 * 3600
        A_t = float(self.ui.A_t.text())
        A_b = float(self.ui.A_b.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        tijd = np.linspace(0, periode, 10000)
        g = 9.81
        xi_v = float(self.ui.xi_v.text())
        xi_t = float(self.ui.xi_t.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        a_rel = a_M2 / a_S2
        rho = 1000

        layout = self.ui.frame_5.layout()
        if layout:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        lmbda = Functies.lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, 1)
        F = float(Functies.bereken_F(self, a_rel))
        mu_M2 = float(Functies.bereken_mu_M2(self, omega_M2, a_M2, lmbda, F))
        mu_S2 = float(Functies.bereken_mu_S2(self, omega_S2, lmbda, F, a_M2))

        theta_M2 = float(Functies.bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F))
        theta_S2 = float(Functies.bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2))

        verval = Functies.bereken_delta_h(self, tijd, mu_M2, mu_S2, a_M2, a_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2)
        vermogen = Functies.bereken_vermogen(self, rho, g, A_t, xi_v, xi_t, verval, 1)

        fig = plt.figure(figsize=(2,2))
        ax = fig.add_subplot(111)
        ax.plot(tijd, vermogen)
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)
        ax.set_xlabel('Tijd (seconden)')
        ax.set_ylabel('Vermogen (Watt)')
        ax.set_title("Vermogen over een periode van 14.77 dagen")
        ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True, useOffset=False))
        canvas = FigureCanvas(fig)

        layout.addWidget(canvas)
        self.ui.frame_5.setLayout(layout)
        plt.close(fig)

    def aanbeveling_turbines(self):
        """Functie voor de popup die aanbeveelt wat het beste aantal turbines is"""
        A_t = float(self.ui.A_t.text())
        A_b = float(self.ui.A_b.text())
        omega_M2 = float(self.ui.omega_M2.text())
        phi_M2 = float(self.ui.phi_M2.text())
        omega_S2 = float(self.ui.omega_S2.text())
        phi_S2 = float(self.ui.phi_S2.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        g = 9.81
        rho = 1000
        xi_v = float(self.ui.xi_v.text())
        xi_t = float(self.ui.xi_t.text())
        a_M2 = float(self.ui.a_M2.text())
        a_S2 = float(self.ui.a_S2.text())
        a_rel = a_M2 / a_S2
        periode = 29.53 * 24 * 3600
        energie_per_turbine = []
        tijd = np.linspace(0, periode, 10000)

        F = float(Functies.bereken_F(self, a_rel))
        range_kijken = self.ui.spinBox.value()

        for i in range(1, range_kijken + 1):
            lmbda = Functies.lambda_berekenen(self, A_t, A_b, g, xi_v, xi_t, i)
            mu_M2 = float(Functies.bereken_mu_M2(self, omega_M2, a_M2, lmbda, F))
            mu_S2 = float(Functies.bereken_mu_S2(self, omega_S2, lmbda, F, a_M2))
            theta_M2 = float(Functies.bereken_theta_M2(self, mu_M2, omega_M2, a_M2, lmbda, F))
            theta_S2 = float(Functies.bereken_theta_S2(self, mu_S2, lmbda, F, omega_S2, a_M2))

            delta_h = Functies.bereken_delta_h(self, tijd, mu_M2, mu_S2, a_M2, a_S2, omega_M2, phi_M2, theta_M2, omega_S2, phi_S2, theta_S2)
            energie_turb = Functies.energie_berekenen(self, delta_h, rho, g, A_t, xi_v, xi_t, i)
            energie_per_turbine.append(energie_turb)

        beste_aantal =  energie_per_turbine.index(max(energie_per_turbine)) + 1
        QMessageBox.information(self.ui.pushButton_start, 'Aanbeveling', f"{beste_aantal} is het beste aantal turbines")