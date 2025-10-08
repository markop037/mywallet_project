from PySide6.QtCore import Qt
from matplotlib.figure import Figure
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ChartDialog(QDialog):
    def __init__(self, categories, amounts, title, total_amount):
        super().__init__()
        self.setWindowTitle(title)
        self.resize(600, 500)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Figure with automatic layout adjustment
        fig = Figure(constrained_layout=True, facecolor="#2E2E2E")
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)

        ax = fig.add_subplot(111)

        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            amounts,
            labels=None,  # don't display labels directly
            autopct=lambda pct: f"{pct:.1f}%",  # percentage inside each segment
            startangle=90,
            textprops={'fontsize': 10}
        )
        ax.axis('equal')  # make it a perfect circle

        # Prepare legend: "Name: amount (percentage%)"
        total = sum(amounts)
        legend_labels = [
            f"{cat}: {amt}$ ({amt/total*100:.1f}%)" for cat, amt in zip(categories, amounts)
        ]

        # Add legend below the pie chart
        ax.legend(
            wedges,
            legend_labels,
            title="Categories",
            loc="upper center",
            bbox_to_anchor=(0.5, -0.05),  # below the chart
            ncol=1,  # one column
            frameon=True,
            fontsize=10
        )

        self.canvas.draw()

        total_label = QLabel(f"Total: {total_amount}$")
        total_label.setStyleSheet("color: white; font-weight: bold; font-size: 13pt;")
        total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(total_label)
