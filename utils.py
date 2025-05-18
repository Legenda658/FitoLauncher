import json
import os
import subprocess
import winreg
import sys
from datetime import datetime
from typing import Dict, List, Optional
CONFIG_FILE = "config.json"
def load_config() -> Dict:
    """Загрузка конфигурации из JSON файла"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "categories": ["Работа", "Игры", "Развлечения", "Другое"],
        "applications": [],
        "groups": [],
        "autostart": {
            "enabled": False,
            "applications": []
        },
        "history": {}
    }
def save_config(config: Dict) -> None:
    """Сохранение конфигурации в JSON файл"""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise Exception(f"Не удалось сохранить конфигурацию: {str(e)}")
def launch_application(path: str) -> bool:
    """Запуск приложения"""
    try:
        if path.startswith(('http://', 'https://')):
            os.startfile(path)
        else:
            subprocess.Popen(path)
        return True
    except Exception:
        return False
def update_history(app_name: str) -> None:
    """Обновление истории запусков"""
    try:
        config = load_config()
        if app_name not in config["history"]:
            config["history"][app_name] = []
        config["history"][app_name].append({
            "timestamp": datetime.now().isoformat(),
            "count": len(config["history"][app_name]) + 1
        })
        save_config(config)
    except Exception:
        pass
def get_most_used_apps(limit: int = 5) -> List[Dict]:
    """Получение списка наиболее часто используемых приложений"""
    try:
        config = load_config()
        apps = []
        for app_name, history in config["history"].items():
            if history:
                apps.append({
                    "name": app_name,
                    "count": history[-1]["count"]
                })
        return sorted(apps, key=lambda x: x["count"], reverse=True)[:limit]
    except Exception:
        return []
def setup_autostart(enable: bool) -> None:
    """Настройка автозапуска лаунчера"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        if enable:
            exe_path = os.path.abspath("dist/FitoLauncher.exe")
            if not os.path.exists(exe_path):
                raise Exception("FitoLauncher.exe не найден. Сначала соберите приложение.")
            winreg.SetValueEx(
                key, "FitoLauncher", 0, winreg.REG_SZ,
                exe_path
            )
        else:
            try:
                winreg.DeleteValue(key, "FitoLauncher")
            except WindowsError:
                pass
        winreg.CloseKey(key)
        config = load_config()
        config["autostart"]["enabled"] = enable
        save_config(config)
    except Exception as e:
        raise Exception(f"Не удалось настроить автозапуск: {str(e)}") 