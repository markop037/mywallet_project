from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ChartDialog(QDialog):
    def __init__(self, categories, amounts, title, total_amount):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(600, 500)  # početna veličina dijaloga

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Figure sa automatskim rasporedom
        fig = Figure(constrained_layout=True, facecolor="#2E2E2E")
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)

        ax = fig.add_subplot(111)

        # Napravi pie chart
        wedges, texts, autotexts = ax.pie(
            amounts,
            labels=None,  # ne stavljamo labels direktno
            autopct=lambda pct: f"{pct:.1f}%",  # procenat unutar segmenta
            startangle=90,
            textprops={'fontsize': 10}
        )
        ax.axis('equal')  # da bude krug

        # Pripremi legendu: "Naziv: iznos (procenat%)"
        total = sum(amounts)
        legend_labels = [
            f"{cat}: {amt}$ ({amt/total*100:.1f}%)" for cat, amt in zip(categories, amounts)
        ]

        # Dodaj legendu ispod pie charta
        ax.legend(
            wedges,
            legend_labels,
            title="Categories",
            loc="upper center",
            bbox_to_anchor=(0.5, -0.05),  # ispod charta
            ncol=1,  # jedna kolona
            frameon=True,
            fontsize=10
        )

        self.canvas.draw()

        total_label = QLabel(f"Total: {total_amount}$")
        total_label.setStyleSheet("color: white; font-weight: bold; font-size: 13pt;")
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(total_label)
