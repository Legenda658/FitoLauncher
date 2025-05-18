import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QComboBox, QCheckBox,
                            QFileDialog, QListWidget, QListWidgetItem, QMessageBox, QStackedWidget, QWidget)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices
class BaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowIcon(QIcon("FitoLauncher.ico"))
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
            QLineEdit {
                padding: 8px;
                border: 2px solid #666;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #888;
            }
            QComboBox {
                padding: 8px;
                border: 2px solid #666;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 12px;
            }
            QComboBox:hover {
                border-color: #888;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
            QCheckBox {
                color: #ffffff;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #666;
                border-radius: 3px;
                background-color: #2d2d2d;
            }
            QCheckBox::indicator:checked {
                background-color: #888;
            }
            QPushButton {
                padding: 8px 16px;
                border: 2px solid #666;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #888;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
            QListWidget {
                border: 2px solid #666;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 12px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #666;
            }
            QListWidget::item:selected {
                background-color: #3d3d3d;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
class ApplicationDialog(BaseDialog):
    def __init__(self, parent=None, app_data=None):
        super().__init__(parent)
        self.app_data = app_data
        self.setWindowTitle("Добавить приложение" if not app_data else "Редактировать приложение")
        self.setMinimumWidth(400)
        self.setup_ui()
        if app_data:
            self.load_data(app_data)
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        name_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        path_layout = QHBoxLayout()
        path_label = QLabel("Путь:")
        self.path_input = QLineEdit()
        browse_btn = QPushButton("Обзор")
        browse_btn.clicked.connect(self.browse_file)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)
        category_layout = QHBoxLayout()
        category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Работа", "Игры", "Развлечения", "Другое"])
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        icon_layout = QHBoxLayout()
        icon_label = QLabel("Иконка:")
        self.icon_input = QLineEdit()
        icon_browse_btn = QPushButton("Обзор")
        icon_browse_btn.clicked.connect(self.browse_icon)
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.icon_input)
        icon_layout.addWidget(icon_browse_btn)
        layout.addLayout(icon_layout)
        self.autostart_check = QCheckBox("Запускать при старте")
        layout.addWidget(self.autostart_check)
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
    def load_data(self, app_data):
        self.name_input.setText(app_data["name"])
        self.path_input.setText(app_data["path"])
        self.category_combo.setCurrentText(app_data["category"])
        if "icon" in app_data:
            self.icon_input.setText(app_data["icon"])
        self.autostart_check.setChecked(app_data.get("autostart", False))
    def browse_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите приложение", "",
                "Все файлы (*.*);;Исполняемые файлы (*.exe)"
            )
            if file_path:
                self.path_input.setText(file_path)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось выбрать файл: {str(e)}")
    def browse_icon(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите иконку", "",
                "Изображения (*.png *.jpg *.ico);;Все файлы (*.*)"
            )
            if file_path:
                self.icon_input.setText(file_path)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось выбрать иконку: {str(e)}")
    def validate_and_accept(self):
        try:
            name = self.name_input.text().strip()
            path = self.path_input.text().strip()
            if not name or not path:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля")
                return
            if not os.path.exists(path):
                QMessageBox.warning(self, "Ошибка", "Указанный путь не существует")
                return
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")
    def get_data(self):
        return {
            "name": self.name_input.text().strip(),
            "path": self.path_input.text().strip(),
            "category": self.category_combo.currentText(),
            "icon": self.icon_input.text().strip(),
            "autostart": self.autostart_check.isChecked(),
        }
class AddAppToGroupDialog(BaseDialog):
    def __init__(self, parent=None, app_data=None):
        super().__init__(parent)
        self.app_data = app_data
        self.setWindowTitle("Добавить приложение в группу" if not app_data else "Редактировать приложение в группе")
        self.setMinimumWidth(400)
        self.setup_ui()
        if app_data:
            self.load_data(app_data)
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        name_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        path_layout = QHBoxLayout()
        path_label = QLabel("Путь:")
        self.path_input = QLineEdit()
        browse_btn = QPushButton("Обзор")
        browse_btn.clicked.connect(self.browse_file)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
    def load_data(self, app_data):
        self.name_input.setText(app_data["name"])
        self.path_input.setText(app_data["path"])
    def browse_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите приложение", "",
                "Все файлы (*.*);;Исполняемые файлы (*.exe)"
            )
            if file_path:
                self.path_input.setText(file_path)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось выбрать файл: {str(e)}")
    def validate_and_accept(self):
        try:
            name = self.name_input.text().strip()
            path = self.path_input.text().strip()
            if not name or not path:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля")
                return
            if not os.path.exists(path):
                QMessageBox.warning(self, "Ошибка", "Указанный путь не существует")
                return
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")
    def get_data(self):
        return {
            "type": "app",
            "name": self.name_input.text().strip(),
            "path": self.path_input.text().strip(),
        }
class AddUrlToGroupDialog(BaseDialog):
    def __init__(self, parent=None, url_data=None):
        super().__init__(parent)
        self.url_data = url_data
        self.setWindowTitle("Добавить URL в группу" if not url_data else "Редактировать URL в группе")
        self.setMinimumWidth(400)
        self.setup_ui()
        if url_data:
            self.load_data(url_data)
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        name_layout = QHBoxLayout()
        name_label = QLabel("Название:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
    def load_data(self, url_data):
        self.name_input.setText(url_data.get("name", ""))
        self.url_input.setText(url_data.get("url", ""))
    def validate_and_accept(self):
        try:
            name = self.name_input.text().strip()
            url = self.url_input.text().strip()
            if not name or not url:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните название и URL")
                return
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")
    def get_data(self):
        return {
            "type": "url",
            "name": self.name_input.text().strip(),
            "url": self.url_input.text().strip()
        }
class GroupDialog(BaseDialog):
    def __init__(self, parent=None, group_data=None, available_apps=None):
        super().__init__(parent)
        self.group_data = group_data
        self.setWindowTitle("Добавить группу" if not group_data else "Редактировать группу")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setup_ui()
        if group_data:
            self.load_data(group_data)
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        name_layout = QHBoxLayout()
        name_label = QLabel("Название группы:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        icon_layout = QHBoxLayout()
        icon_label = QLabel("Иконка группы:")
        self.icon_input = QLineEdit()
        icon_browse_btn = QPushButton("Обзор")
        icon_browse_btn.clicked.connect(self.browse_icon)
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.icon_input)
        icon_layout.addWidget(icon_browse_btn)
        layout.addLayout(icon_layout)
        category_layout = QHBoxLayout()
        category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Работа", "Игры", "Развлечения", "Другое"])
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        self.autostart_check = QCheckBox("Запускать при старте лаунчера")
        layout.addWidget(self.autostart_check)
        items_label = QLabel("Элементы группы:")
        layout.addWidget(items_label)
        self.items_list = QListWidget()
        layout.addWidget(self.items_list)
        items_buttons_layout = QHBoxLayout()
        add_app_btn = QPushButton("Добавить приложение")
        add_url_btn = QPushButton("Добавить URL")
        remove_item_btn = QPushButton("Удалить элемент")
        add_app_btn.clicked.connect(self.add_application_to_group)
        add_url_btn.clicked.connect(self.add_url_to_group)
        remove_item_btn.clicked.connect(self.remove_item)
        items_buttons_layout.addWidget(add_app_btn)
        items_buttons_layout.addWidget(add_url_btn)
        items_buttons_layout.addWidget(remove_item_btn)
        layout.addLayout(items_buttons_layout)
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.validate_and_accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
    def load_data(self, group_data):
        self.name_input.setText(group_data["name"])
        self.category_combo.setCurrentText(group_data["category"])
        if "icon" in group_data:
            self.icon_input.setText(group_data["icon"])
        self.autostart_check.setChecked(group_data.get("autostart", False))
        for item in group_data["items"]:
            display_name = item["name"]
            if item["type"] == "url":
                display_name = f"🌐 {display_name}"
            elif item["type"] == "app":
                display_name = f"📱 {display_name}"
            list_item = QListWidgetItem(display_name)
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.items_list.addItem(list_item)
    def browse_icon(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите иконку", "",
                "Изображения (*.png *.jpg *.ico);;Все файлы (*.*)"
            )
            if file_path:
                self.icon_input.setText(file_path)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось выбрать иконку: {str(e)}")
    def add_application_to_group(self):
        """Открывает диалог для добавления приложения в группу"""
        try:
            dialog = AddAppToGroupDialog(self)
            if dialog.exec():
                item_data = dialog.get_data()
                display_name = f"📱 {item_data['name']}"
                list_item = QListWidgetItem(display_name)
                list_item.setData(Qt.ItemDataRole.UserRole, item_data)
                self.items_list.addItem(list_item)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить приложение: {str(e)}")
    def add_url_to_group(self):
        """Открывает диалог для добавления URL в группу"""
        try:
            dialog = AddUrlToGroupDialog(self)
            if dialog.exec():
                item_data = dialog.get_data()
                display_name = f"🌐 {item_data['name']}"
                list_item = QListWidgetItem(display_name)
                list_item.setData(Qt.ItemDataRole.UserRole, item_data)
                self.items_list.addItem(list_item)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить URL: {str(e)}")
    def remove_item(self):
        try:
            selected_items = self.items_list.selectedItems()
            if not selected_items:
                return
            for item in selected_items:
                self.items_list.takeItem(self.items_list.row(item))
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить элемент: {str(e)}")
    def validate_and_accept(self):
        try:
            name = self.name_input.text().strip()
            if not name:
                QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите название группы")
                return
            if self.items_list.count() == 0:
                QMessageBox.warning(self, "Ошибка", "Добавьте хотя бы один элемент в группу")
                return
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить данные: {str(e)}")
    def get_data(self):
        items = []
        for i in range(self.items_list.count()):
            item = self.items_list.item(i).data(Qt.ItemDataRole.UserRole)
            items.append(item)
        return {
            "name": self.name_input.text().strip(),
            "category": self.category_combo.currentText(),
            "icon": self.icon_input.text().strip(),
            "items": items,
            "autostart": self.autostart_check.isChecked()
        }
class SettingsDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки")
        self.setup_ui()
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        self.launcher_autostart = QCheckBox("Запускать лаунчер при старте Windows")
        layout.addWidget(self.launcher_autostart)
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
    def get_data(self):
        return {
            "launcher_autostart": self.launcher_autostart.isChecked()
        } 