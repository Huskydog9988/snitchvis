from PyQt6.QtWidgets import (QFrame, QGridLayout, QLabel, QVBoxLayout)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from snitchvis.utils import resource_path
from snitchvis.widgets import JumpSlider, PushButton

class VisualizerControls(QFrame):

    def __init__(self, speed):
        super().__init__()
        self.time_slider = JumpSlider(Qt.Orientation.Horizontal)
        self.time_slider.setValue(0)
        self.time_slider.setFixedHeight(20)
        self.time_slider.setStyleSheet("outline: none;")

        self.play_reverse_button = PushButton()
        self.play_reverse_button.setIcon(QIcon(resource_path("play_reverse.png")))
        self.play_reverse_button.setFixedSize(20, 20)
        self.play_reverse_button.setToolTip("Play in reverse")

        self.play_normal_button = PushButton()
        self.play_normal_button.setIcon(QIcon(resource_path("play_normal.png")))
        self.play_normal_button.setFixedSize(20, 20)
        self.play_normal_button.setToolTip("Play normally")

        self.next_frame_button = PushButton()
        self.next_frame_button.setIcon(QIcon(resource_path("frame_next.png")))
        self.next_frame_button.setFixedSize(20, 20)
        self.next_frame_button.setToolTip("Move forward one frame")

        self.previous_frame_button = PushButton()
        self.previous_frame_button.setIcon(QIcon(resource_path("frame_back.png")))
        self.previous_frame_button.setFixedSize(20, 20)
        self.previous_frame_button.setToolTip("Move backward one frame")

        self.pause_button = PushButton()
        self.pause_button.setIcon(QIcon(resource_path("pause.png")))
        self.pause_button.setFixedSize(20, 20)
        self.pause_button.setToolTip("Pause / Play")

        self.speed_label = QLabel(f"{speed}x")
        self.speed_label.setFixedSize(40, 20)
        self.speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        self.settings_button = PushButton()
        self.settings_button.setIcon(QIcon(resource_path("settings_wheel.png")))
        self.settings_button.setFixedSize(20, 20)
        self.settings_button.setToolTip("Open settings")
        self.settings_button.clicked.connect(self.settings_button_clicked)

        self.settings_popup = SettingsPopup(self)

        self.speed_up_button = PushButton()
        self.speed_up_button.setIcon(QIcon(resource_path("speed_up.png")))
        self.speed_up_button.setFixedSize(20, 20)
        self.speed_up_button.setToolTip("Increase speed")

        self.speed_down_button = PushButton()
        self.speed_down_button.setIcon(QIcon(resource_path("speed_down.png")))
        self.speed_down_button.setFixedSize(20, 20)
        self.speed_down_button.setToolTip("Decrease speed")

        layout = QGridLayout()
        layout.addWidget(self.play_reverse_button, 16, 0, 1, 1)
        layout.addWidget(self.previous_frame_button, 16, 1, 1, 1)
        layout.addWidget(self.pause_button, 16, 2, 1, 1)
        layout.addWidget(self.next_frame_button, 16, 3, 1, 1)
        layout.addWidget(self.play_normal_button, 16, 4, 1, 1)
        layout.addWidget(self.speed_down_button, 16, 5, 1, 1)
        layout.addWidget(self.speed_up_button, 16, 6, 1, 1)
        layout.addWidget(self.speed_label, 16, 7, 1, 1)
        layout.addWidget(self.time_slider, 16, 8, 1, 9)
        layout.addWidget(self.settings_button, 16, 18, 1, 1)
        layout.setContentsMargins(5, 0, 5, 5)
        self.setLayout(layout)
        self.setFixedHeight(25)

    def set_paused_state(self, paused):
        icon = "play.png" if paused else "pause.png"
        self.pause_button.setIcon(QIcon(resource_path(icon)))

    def settings_button_clicked(self):
        # have to show before setting its geometry because it has some default
        # geometry that doesn't reflect its actual proportions until it's shown
        self.settings_popup.show()
        global_pos = self.mapToGlobal(self.settings_button.pos())
        popup_height = self.settings_popup.size().height()
        popup_width = self.settings_popup.size().width()

        # `x - 44` to not make the popup hang over the right side of the window
        # (aftering centering it horizontally), and `y - 6` to account for the
        # space between the button and the top of the controls row
        self.settings_popup.setGeometry(int(global_pos.x() - (popup_width / 2) - 44),\
            int(global_pos.y() - popup_height - 6), popup_width, popup_height)

class SettingsPopup(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        # we're technically a window, but we don't want to be shown as such to
        # the user, so hide our window features (like the top bar)
        self.setWindowFlags(Qt.WindowType.Popup)

        self.setMaximumWidth(300)
        self.setMaximumHeight(100)

        layout = QVBoxLayout()
        self.setLayout(layout)
