import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLineEdit, QTabWidget,
                            QLabel, QMenu, QMessageBox, QGridLayout, QScrollArea, QButtonGroup)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QPalette, QColor
from utils import load_config, save_config, launch_application, update_history, setup_autostart
from dialogs import ApplicationDialog, GroupDialog, SettingsDialog, AddAppToGroupDialog, AddUrlToGroupDialog
class AppButton(QPushButton):
    def __init__(self, name, icon_path=None, is_group=False, parent=None):
        super().__init__(parent)
        self.setFixedSize(150, 150)  
        self.setToolTip(name)
        layout = QVBoxLayout(self) 
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setFixedSize(64, 64) 
        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setWordWrap(True) 
        self.name_label.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label)
        self.setIconSize(QSize(64, 64)) 
        if icon_path and os.path.exists(icon_path):
            pixmap = QIcon(icon_path).pixmap(64, 64)
            self.icon_label.setPixmap(pixmap)
        elif is_group:
            pixmap = QIcon.fromTheme("folder").pixmap(64, 64) 
            if pixmap.isNull():
                 pixmap = QIcon("icons/default_group.png").pixmap(64, 64) 
            self.icon_label.setPixmap(pixmap)
        else:
            pixmap = QIcon.fromTheme("application-x-executable").pixmap(64, 64) 
            if pixmap.isNull():
                 pixmap = QIcon("icons/default_app.png").pixmap(64, 64) 
            self.icon_label.setPixmap(pixmap)
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #666;
                border-radius: 10px;
                padding: 5px; /* Уменьшил padding, чтобы текст и иконка были ближе */
                background-color: #2d2d2d;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #888;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
            QPushButton:checked { /* Стиль для выбранной кнопки */
                background-color: #555; 
                border-color: #bbb;
            }
        """)
class FitoLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ФитоЛаунчер")
        self.setMinimumSize(1000, 700)  
        self.setWindowIcon(QIcon("FitoLauncher.ico"))
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTabWidget::pane {
                border: 1px solid #666;
                background-color: #2d2d2d;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #ffffff;
                padding: 8px 16px;
                border: 1px solid #666;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3d3d3d;
                border-bottom: 2px solid #888;
            }
            QTabBar::tab:hover {
                background-color: #3d3d3d;
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
            QPushButton {
                padding: 8px 16px;
                border: 2px solid #666;
                border-radius: 5px;
                background-color: #2d2d2d;
                color: #ffffff;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-color: #888;
            }
            QPushButton:pressed {
                background-color: #4d4d4d;
            }
            QPushButton:checked { /* Стиль для выбранной кнопки */
                background-color: #555; 
                border-color: #bbb;
            }
            QScrollArea {
                border: none;
                background-color: #2d2d2d;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #2d2d2d;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #666;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #888;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                border: none;
                background-color: #2d2d2d;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background-color: #666;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #888;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QMenu {
                background-color: #2d2d2d;
                border: 1px solid #666;
                color: #ffffff;
            }
            QMenu::item {
                padding: 8px 16px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
            QMessageBox {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QMessageBox QPushButton {
                min-width: 80px;
            }
        """)
        try:
            self.config = load_config()
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)
            main_layout.setSpacing(10)
            main_layout.setContentsMargins(10, 10, 10, 10)
            filter_layout = QHBoxLayout() 
            self.filter_buttons = {
                "all": QPushButton("Все"),
                "apps": QPushButton("Приложения"),
                "groups": QPushButton("Группы")
            }
            self.filter_button_group = QButtonGroup(self)
            self.filter_button_group.setExclusive(True)
            for key, btn in self.filter_buttons.items():
                filter_layout.addWidget(btn)
                btn.setCheckable(True)
                btn.clicked.connect(self.filter_applications)
                self.filter_button_group.addButton(btn) 
            self.filter_buttons["all"].setChecked(True)
            main_layout.addLayout(filter_layout) 
            self.tabs = QTabWidget()
            self.tab_contents = {}  
            for category in self.config["categories"]:
                scroll = QScrollArea()
                scroll.setWidgetResizable(True)
                scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                content = QWidget()
                self.tab_contents[category] = content
                grid = QGridLayout(content)
                grid.setSpacing(20)  
                grid.setContentsMargins(20, 20, 20, 20)  
                scroll.setWidget(content)
                self.tabs.addTab(scroll, category)
            main_layout.addWidget(self.tabs)
            buttons_layout = QHBoxLayout()
            add_app_btn = QPushButton("Добавить приложение")
            add_group_btn = QPushButton("Добавить группу")
            settings_btn = QPushButton("Настройки")
            buttons_layout.addWidget(add_app_btn)
            buttons_layout.addWidget(add_group_btn)
            buttons_layout.addWidget(settings_btn)
            main_layout.addLayout(buttons_layout)
            add_app_btn.clicked.connect(self.add_application)
            add_group_btn.clicked.connect(self.add_group)
            settings_btn.clicked.connect(self.show_settings)
            self.load_applications()
            if self.config["autostart"]["enabled"]:
                self.autostart_applications()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось инициализировать приложение: {str(e)}")
            sys.exit(1)
    def load_applications(self):
        """Загрузка приложений в соответствующие категории"""
        try:
            for category in self.config["categories"]:
                content = self.tab_contents[category]
                while content.layout().count():
                    item = content.layout().takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()
            for app in self.config["applications"]:
                if not isinstance(app, dict) or "name" not in app or "category" not in app:
                    continue
                category = app.get("category", "Другое")
                content = self.tab_contents.get(category)
                if not content:
                     continue 
                grid = content.layout()
                btn = AppButton(app["name"], icon_path=app.get("icon"), is_group=False)
                btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                btn.customContextMenuRequested.connect(
                    lambda pos, a=app: self.show_context_menu(pos, a)
                )
                btn.clicked.connect(lambda checked, a=app: self.launch_item(a))
                count = grid.count()
                row = count // 4
                col = count % 4
                grid.addWidget(btn, row, col)
            for group in self.config["groups"]:
                if not isinstance(group, dict) or "name" not in group or "category" not in group:
                    continue
                category = group.get("category", "Другое")
                content = self.tab_contents.get(category)
                if not content:
                    continue 
                grid = content.layout()
                btn = AppButton(group["name"], icon_path=group.get("icon"), is_group=True)
                btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                btn.customContextMenuRequested.connect(
                    lambda pos, g=group: self.show_context_menu(pos, g, is_group=True)
                )
                btn.clicked.connect(lambda checked, g=group: self.launch_item(g, is_group=True))
                count = grid.count()
                row = count // 4
                col = count % 4
                grid.addWidget(btn, row, col)
            self.filter_applications()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить приложения: {str(e)}")
    def filter_applications(self):
        """Фильтрация приложений по типу"""
        try:
            current_filter = next(k for k, v in self.filter_buttons.items() if v.isChecked())
            for category in self.config["categories"]:
                content = self.tab_contents.get(category)
                if not content:
                    continue
                grid = content.layout()
                for i in range(grid.count()):
                    item = grid.itemAt(i)
                    if not item:
                        continue
                    btn = item.widget()
                    if not btn:
                        continue
                    app_data = None
                    is_group = False
                    for app in self.config["applications"]:
                        if app["name"] == btn.name_label.text(): 
                            app_data = app
                            break
                    if not app_data:
                        for group in self.config["groups"]:
                            if group["name"] == btn.name_label.text(): 
                                app_data = group
                                is_group = True
                                break
                    if not app_data:
                        btn.setVisible(False) 
                        continue
                    if current_filter == "all":
                        btn.setVisible(True)
                    elif current_filter == "apps" and not is_group:
                        btn.setVisible(True)
                    elif current_filter == "groups" and is_group:
                        btn.setVisible(True)
                    else:
                        btn.setVisible(False)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось отфильтровать приложения: {str(e)}")
    def show_context_menu(self, position, item_data, is_group=False):
        """Показ контекстного меню"""
        try:
            menu = QMenu()
            if not is_group:
                edit_action = QAction("Редактировать", self)
                edit_action.triggered.connect(lambda checked=False, data=item_data: self.edit_application(data))
                menu.addAction(edit_action)
                delete_action = QAction("Удалить", self)
                delete_action.triggered.connect(lambda checked=False, data=item_data: self.delete_application(data))
                menu.addAction(delete_action)
            else:
                edit_action = QAction("Редактировать группу", self)
                edit_action.triggered.connect(lambda checked=False, data=item_data: self.edit_group(data))
                menu.addAction(edit_action)
                delete_action = QAction("Удалить группу", self)
                delete_action.triggered.connect(lambda checked=False, data=item_data: self.delete_group(data))
                menu.addAction(delete_action)
            menu.exec(self.sender().mapToGlobal(position))
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось показать контекстное меню: {str(e)}")
    def launch_item(self, item_data, is_group=False):
        """Запуск приложения или группы"""
        try:
            if not is_group:
                if launch_application(item_data["path"]):
                    update_history(item_data["name"])
            else:
                for item in item_data["items"]:
                    if item["type"] == "app":
                        if launch_application(item["path"]):
                            update_history(item["name"])
                    elif item["type"] == "url":
                        import webbrowser
                        webbrowser.open(item["url"])
                        update_history(item["name"])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось запустить элемент: {str(e)}")
    def add_application(self):
        """Добавление нового приложения"""
        try:
            dialog = ApplicationDialog(self)
            if dialog.exec():
                app_data = dialog.get_data()
                if any(app["path"] == app_data["path"] for app in self.config["applications"]):
                    QMessageBox.warning(self, "Предупреждение", "Приложение с таким путем уже существует!")
                    return
                self.config["applications"].append(app_data)
                save_config(self.config)
                self.load_applications()
                if app_data.get("autostart", False):
                    if app_data["path"] not in self.config["autostart"]["applications"]:
                         self.config["autostart"]["applications"].append(app_data["path"])
                         save_config(self.config) 
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить приложение: {str(e)}")
    def add_group(self):
        """Добавление новой группы"""
        try:
            dialog = GroupDialog(self, available_apps=self.config["applications"])
            if dialog.exec():
                group_data = dialog.get_data()
                if any(group["name"] == group_data["name"] for group in self.config["groups"]):
                    QMessageBox.warning(self, "Предупреждение", "Группа с таким названием уже существует!")
                    return
                self.config["groups"].append(group_data)
                save_config(self.config)
                self.load_applications()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось добавить группу: {str(e)}")
    def show_settings(self):
        """Показ окна настроек"""
        try:
            dialog = SettingsDialog(self)
            dialog.launcher_autostart.setChecked(self.config.get("launcher_autostart_enabled", False))
            if dialog.exec():
                settings = dialog.get_data()
                self.config["launcher_autostart_enabled"] = settings["launcher_autostart"]
                save_config(self.config)
                setup_autostart(settings["launcher_autostart"])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось открыть настройки: {str(e)}")
    def edit_application(self, app_data):
        """Редактирование приложения"""
        try:
            original_app_data = app_data.copy()
            dialog = ApplicationDialog(self, app_data)
            if dialog.exec():
                new_data = dialog.get_data()
                for i, app in enumerate(self.config["applications"]):
                    if app.get("path") == original_app_data.get("path"):
                        self.config["applications"][i] = new_data
                        break
                original_autostart = original_app_data.get("autostart", False)
                new_autostart = new_data.get("autostart", False)
                original_path = original_app_data.get("path")
                new_path = new_data.get("path")
                if original_path != new_path:
                    if original_autostart and original_path in self.config["autostart"]["applications"]:
                        self.config["autostart"]["applications"].remove(original_path)
                    if new_autostart and new_path not in self.config["autostart"]["applications"]:
                         self.config["autostart"]["applications"].append(new_path)
                elif original_autostart != new_autostart:
                    if new_autostart and new_path not in self.config["autostart"]["applications"]:
                        self.config["autostart"]["applications"].append(new_path)
                    elif not new_autostart and new_path in self.config["autostart"]["applications"]:
                        self.config["autostart"]["applications"].remove(new_path)
                save_config(self.config)
                self.load_applications()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось отредактировать приложение: {str(e)}")
    def edit_group(self, group_data):
        """Редактирование группы"""
        try:
            original_group_data = group_data.copy()
            dialog = GroupDialog(self, group_data, self.config["applications"])
            if dialog.exec():
                new_data = dialog.get_data()
                for i, group in enumerate(self.config["groups"]):
                    if group.get("name") == original_group_data.get("name"):
                        self.config["groups"][i] = new_data
                        break
                save_config(self.config)
                self.load_applications()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось отредактировать группу: {str(e)}")
    def delete_application(self, app_data):
        """Удаление приложения"""
        try:
            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Вы уверены, что хотите удалить приложение {app_data.get('name', 'Без названия')}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.config["applications"] = [app for app in self.config["applications"] 
                                             if app.get("path") != app_data.get("path")]
                if app_data.get("path") in self.config["autostart"]["applications"]:
                    self.config["autostart"]["applications"].remove(app_data.get("path"))
                save_config(self.config)
                self.load_applications()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить приложение: {str(e)}")
    def delete_group(self, group_data):
        """Удаление группы"""
        try:
            reply = QMessageBox.question(
                self, "Подтверждение",
                f"Вы уверены, что хотите удалить группу {group_data.get('name', 'Без названия')}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.config["groups"] = [group for group in self.config["groups"] 
                                       if group.get("name") != group_data.get("name")]
                save_config(self.config)
                self.load_applications()
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось удалить группу: {str(e)}")
    def autostart_applications(self):
        """Автозапуск отмеченных приложений и групп"""
        try:
            for app_path in self.config["autostart"]["applications"]:
                app_data = next((app for app in self.config["applications"] if app.get("path") == app_path), None)
                if app_data:
                     launch_application(app_data["path"])
            for group in self.config["groups"]:
                if group.get("autostart", False):
                    for item in group["items"]:
                        if item["type"] == "app":
                            if launch_application(item["path"]):
                                update_history(item["name"])
                        elif item["type"] == "url":
                            import webbrowser
                            webbrowser.open(item["url"])
                            update_history(item["name"])
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось запустить элементы при старте: {str(e)}")
if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = FitoLauncher()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Критическая ошибка", f"Не удалось запустить приложение: {str(e)}")
        sys.exit(1) 