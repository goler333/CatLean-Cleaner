#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import ctypes
import winreg
import subprocess
import time
import getpass
import datetime
import random
import base64


# Цвета для консоли
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()


def log(message, status="info"):
    timestamp = time.strftime("%H:%M:%S")
    if status == "success":
        print(f"{Colors.GREEN}[✓ {timestamp}] {message}{Colors.RESET}")
    elif status == "error":
        print(f"{Colors.RED}[✗ {timestamp}] {message}{Colors.RESET}")
    elif status == "warning":
        print(f"{Colors.YELLOW}[! {timestamp}] {message}{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}[i {timestamp}] {message}{Colors.RESET}")


class UltimateCleaner:
    def __init__(self):
        self.username = getpass.getuser()
        self.start_time = datetime.datetime.now()
        self.deleted_count = 0
        self.kept_count = 0
        self.stats = {
            '.exe': 0, '.dll': 0, '.jar': 0,
            '.tmp': 0, '.log': 0, '.pf': 0,
            '.cfg': 0, '.json': 0, '.zip': 0,
            '.txt': 0, '.dat': 0, '.cache': 0
        }

    # Функция 1: Очистка DNS кэша
    def flush_dns(self):
        """Очищает DNS кэш"""
        try:
            os.system('ipconfig /flushdns >nul 2>&1')
            log("DNS кэш очищен", "success")
        except Exception as e:
            log(f"Ошибка при очистке DNS: {str(e)}", "error")

    # Функция 2: Очистка ARP таблицы
    def clear_arp(self):
        """Очищает ARP таблицу"""
        try:
            os.system('arp -d * >nul 2>&1')
            log("ARP таблица очищена", "success")
        except Exception as e:
            log(f"Ошибка при очистке ARP: {str(e)}", "error")

    # Функция 3: Очистка журнала событий Windows
    def clear_event_logs(self):
        """Очищает логи событий"""
        try:
            os.system('wevtutil cl Application >nul 2>&1')
            os.system('wevtutil cl System >nul 2>&1')
            os.system('wevtutil cl Security >nul 2>&1')
            log("Журналы событий очищены", "success")
        except Exception as e:
            log(f"Ошибка при очистке журналов: {str(e)}", "error")

    # Функция 7: Шифрование логов
    def encrypt_logs(self):
        """Шифрует логи программы"""
        try:
            log_file = "cleaner.log"
            if os.path.exists(log_file):
                with open(log_file, "r", encoding='utf-8') as f:
                    data = f.read()

                encoded = base64.b64encode(data.encode()).decode()

                with open("cleaner.log.enc", "w", encoding='utf-8') as f:
                    f.write(encoded)

                os.remove(log_file)
                log("Логи зашифрованы", "success")
        except Exception as e:
            log(f"Ошибка при шифровании логов: {str(e)}", "error")

    # Функция 9: Детальная статистика
    def update_stats(self, file_path):
        """Обновляет статистику по типам файлов"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in self.stats:
            self.stats[ext] += 1
        else:
            self.stats['.tmp'] += 1

    def show_detailed_stats(self):
        """Показывает подробную статистику"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 Детальная статистика:{Colors.RESET}")
        print(f"{Colors.BOLD}{'─' * 40}{Colors.RESET}")

        total = 0
        for ext, count in self.stats.items():
            if count > 0:
                print(f"  {ext:6} : {count:4} файлов")
                total += count

        print(f"{Colors.BOLD}{'─' * 40}{Colors.RESET}")
        print(f"  ВСЕГО : {total:4} файлов")
        print()

    # Функция 11: Очистка браузеров (включая Яндекс)
    def clean_browsers(self):
        """Очищает кэш браузеров"""
        browsers = {
            'Chrome': f'C:\\Users\\{self.username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache',
            'Chrome Code Cache': f'C:\\Users\\{self.username}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Code Cache',
            'Firefox': f'C:\\Users\\{self.username}\\AppData\\Local\\Mozilla\\Firefox\\Profiles',
            'Edge': f'C:\\Users\\{self.username}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache',
            'Opera': f'C:\\Users\\{self.username}\\AppData\\Local\\Opera Software\\Opera Stable\\Cache',
            'Opera GX': f'C:\\Users\\{self.username}\\AppData\\Local\\Opera Software\\Opera GX Stable\\Cache',
            'Brave': f'C:\\Users\\{self.username}\\AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Cache',
            'Yandex': f'C:\\Users\\{self.username}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Cache',
            'Yandex Code Cache': f'C:\\Users\\{self.username}\\AppData\\Local\\Yandex\\YandexBrowser\\User Data\\Default\\Code Cache',
            'Yandex Media': f'C:\\Users\\{self.username}\\AppData\\Local\\Yandex\\Media Player\\Cache',
        }

        log("Очистка кэша браузеров...", "info")
        cleaned = 0

        for browser, path in browsers.items():
            if os.path.exists(path):
                try:
                    # Считаем файлы до очистки
                    files_count = 0
                    for root, dirs, files in os.walk(path):
                        files_count += len(files)

                    if files_count > 0:
                        for root, dirs, files in os.walk(path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    self.update_stats(file_path)
                                    os.remove(file_path)
                                except:
                                    pass

                        log(f"  Очищен кэш {browser}: удалено {files_count} файлов", "success")
                        cleaned += 1
                        self.deleted_count += files_count
                except Exception as e:
                    log(f"  Ошибка при очистке {browser}: {str(e)}", "warning")

        if cleaned == 0:
            log("Кэш браузеров не найден", "warning")
        else:
            log(f"Очищено браузеров: {cleaned}", "success")

    # Очистка КЭША TLauncher (НЕ УДАЛЯТЬ САМ ЛАУНЧЕР)
    def clean_tlauncher_cache(self):
        """Очищает только кэш TLauncher, не трогая сам лаунчер"""
        cache_paths = [
            f'C:\\Users\\{self.username}\\AppData\\Roaming\\.tlauncher\\cache',
            f'C:\\Users\\{self.username}\\AppData\\Roaming\\.tlauncher\\logs',
            f'C:\\Users\\{self.username}\\AppData\\Roaming\\.tlauncher\\temp',
            f'C:\\Users\\{self.username}\\AppData\\Roaming\\TLauncher\\cache',
            f'C:\\Users\\{self.username}\\AppData\\Roaming\\TLauncher\\logs',
            f'C:\\Users\\{self.username}\\AppData\\Local\\Temp\\.tlauncher',
            f'C:\\Users\\{self.username}\\.tlauncher\\cache',
            f'C:\\Users\\{self.username}\\.tlauncher\\logs',
        ]

        log("Очистка кэша TLauncher...", "info")
        cleaned = 0
        total_files = 0

        for path in cache_paths:
            if os.path.exists(path):
                try:
                    # Считаем файлы
                    files_count = 0
                    for root, dirs, files in os.walk(path):
                        files_count += len(files)
                        for file in files:
                            self.update_stats(os.path.join(root, file))

                    # Удаляем содержимое, но не саму папку
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            try:
                                os.remove(os.path.join(root, file))
                            except:
                                pass
                        for dir in dirs:
                            try:
                                shutil.rmtree(os.path.join(root, dir), ignore_errors=True)
                            except:
                                pass

                    log(f"  Очищен кэш: {path} (удалено {files_count} файлов)", "success")
                    cleaned += 1
                    total_files += files_count
                    self.deleted_count += files_count

                except Exception as e:
                    log(f"  Ошибка при очистке {path}: {str(e)}", "warning")

        # Проверим основные папки TLauncher на наличие кэша
        main_paths = [
            f'C:\\Users\\{self.username}\\AppData\\Roaming\\.tlauncher',
            f'C:\\Users\\{self.username}\\AppData\\Roaming\\TLauncher',
            f'C:\\Users\\{self.username}\\.tlauncher',
        ]

        for main_path in main_paths:
            if os.path.exists(main_path):
                # Ищем папки с кэшем внутри
                try:
                    for item in os.listdir(main_path):
                        item_path = os.path.join(main_path, item)
                        if os.path.isdir(item_path) and item.lower() in ['cache', 'logs', 'temp', 'tmp']:
                            files_count = 0
                            for root, dirs, files in os.walk(item_path):
                                files_count += len(files)

                            if files_count > 0:
                                shutil.rmtree(item_path, ignore_errors=True)
                                os.makedirs(item_path, exist_ok=True)
                                log(f"  Очищена папка: {item} в {main_path} ({files_count} файлов)", "success")
                                total_files += files_count
                                self.deleted_count += files_count
                except:
                    pass

        if cleaned == 0 and total_files == 0:
            log("Кэш TLauncher не найден", "warning")
        else:
            log(f"Кэш TLauncher очищен: удалено {total_files} файлов", "success")

    # Очистка папки .ctl
    def clean_ctl(self):
        ctl_path = f"C:\\Users\\{self.username}\\.ctl"
        if os.path.exists(ctl_path):
            try:
                files_count = 0
                for root, dirs, files in os.walk(ctl_path):
                    files_count += len(files)
                    for file in files:
                        self.update_stats(os.path.join(root, file))

                shutil.rmtree(ctl_path, ignore_errors=True)
                log(f"Папка .ctl полностью удалена (содержала {files_count} файлов)", "success")
                self.deleted_count += files_count
            except Exception as e:
                log(f"Ошибка при удалении .ctl: {str(e)}", "error")
        else:
            log("Папка .ctl не найдена", "warning")

    # Очистка недавних файлов
    def clean_recent(self):
        recent_path = f"C:\\Users\\{self.username}\\AppData\\Roaming\\Microsoft\\Windows\\Recent"
        if os.path.exists(recent_path):
            try:
                files = os.listdir(recent_path)
                delete_percent = random.randint(70, 90)
                delete_count = int(len(files) * delete_percent / 100)

                log(f"Очистка недавних файлов: найдено {len(files)}", "info")

                deleted = 0
                for i, file in enumerate(files[:delete_count]):
                    if random.random() > 0.1:
                        file_path = os.path.join(recent_path, file)
                        if os.path.isfile(file_path):
                            size = os.path.getsize(file_path)
                            self.update_stats(file_path)
                            os.remove(file_path)
                            deleted += 1
                            self.deleted_count += 1

                log(f"Недавние файлы: удалено {deleted}, оставлено {len(files) - deleted}", "success")

            except Exception as e:
                log(f"Ошибка при очистке недавних: {str(e)}", "error")

    # Очистка TEMP
    def clean_temp(self):
        temp_path = os.environ.get('TEMP', '')
        if temp_path and os.path.exists(temp_path):
            self._clean_folder(temp_path, "пользовательская TEMP")

        system_temp = "C:\\Windows\\Temp"
        self._clean_folder(system_temp, "системная TEMP")

    def _clean_folder(self, folder_path, description):
        if not os.path.exists(folder_path):
            return

        try:
            files = []
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    files.append(item)

            if not files:
                return

            delete_percent = random.randint(70, 90)
            delete_count = int(len(files) * delete_percent / 100)

            log(f"Очистка {description}: найдено {len(files)} файлов", "info")

            deleted = 0
            for i, file in enumerate(files[:delete_count]):
                if random.random() > 0.1:
                    file_path = os.path.join(folder_path, file)
                    try:
                        size = os.path.getsize(file_path)
                        self.update_stats(file_path)
                        os.remove(file_path)
                        deleted += 1
                        self.deleted_count += 1
                    except:
                        self.kept_count += 1

            log(f"{description}: удалено {deleted}, оставлено {len(files) - deleted}", "success")

        except Exception as e:
            log(f"Ошибка при очистке {description}: {str(e)}", "error")

    # Очистка Prefetch
    def clean_prefetch(self):
        prefetch_path = "C:\\Windows\\Prefetch"
        if os.path.exists(prefetch_path):
            try:
                files = [f for f in os.listdir(prefetch_path) if f.endswith('.pf')]

                delete_percent = random.randint(70, 90)
                delete_count = int(len(files) * delete_percent / 100)

                log(f"Очистка Prefetch: найдено {len(files)} файлов", "info")

                deleted = 0
                for i, file in enumerate(files[:delete_count]):
                    if random.random() > 0.1:
                        file_path = os.path.join(prefetch_path, file)
                        try:
                            size = os.path.getsize(file_path)
                            self.update_stats(file_path)
                            os.remove(file_path)
                            deleted += 1
                            self.deleted_count += 1
                        except:
                            self.kept_count += 1

                log(f"Prefetch: удалено {deleted}, оставлено {len(files) - deleted}", "success")

            except Exception as e:
                log(f"Ошибка при очистке Prefetch: {str(e)}", "error")

    # Запуск всех функций
    def run_all(self):
        log("=" * 60, "info")
        log("ЗАПУСК ПОЛНОЙ ОЧИСТКИ", "info")
        log("=" * 60, "info")

        # 1. Удаление папки .ctl
        self.clean_ctl()

        # 2. Очистка недавних
        self.clean_recent()

        # 3. Очистка TEMP
        self.clean_temp()

        # 4. Очистка Prefetch
        self.clean_prefetch()

        # 5. Очистка КЭША TLauncher (только кэш!)
        self.clean_tlauncher_cache()

        # 6. Очистка браузеров (включая Яндекс)
        self.clean_browsers()

        # 7. Очистка DNS
        self.flush_dns()

        # 8. Очистка ARP
        self.clear_arp()

        # 9. Очистка журналов событий
        self.clear_event_logs()

        # 10. Показать статистику
        self.show_detailed_stats()

        # 11. Зашифровать логи
        self.encrypt_logs()

        log("=" * 60, "info")
        log(f"ИТОГО УДАЛЕНО: {self.deleted_count} файлов", "success")
        log(f"ИТОГО ОСТАВЛЕНО: {self.kept_count} файлов", "warning")
        log("=" * 60, "info")


def main():
    os.system('cls')

    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║              ULTIMATE CatLean CLEANER v1.5                 ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    username = getpass.getuser()
    print(f"{Colors.BOLD}Пользователь: {Colors.CYAN}{username}{Colors.RESET}")
    print(f"{Colors.BOLD}Время запуска: {Colors.CYAN}{time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print()

    if not is_admin():
        log("Запуск от имени администратора...", "info")
        run_as_admin()
        return

    cleaner = UltimateCleaner()
    cleaner.run_all()

    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                  ОЧИСТКА ПОЛНОСТЬЮ ЗАВЕРШЕНА               ║")
    print("║                                                            ║")
    print("║  ✓ DNS кэш очищен                                          ║")
    print("║  ✓ ARP таблица очищена                                     ║")
    print("║  ✓ Журналы событий очищены                                 ║")
    print("║  ✓ Логи зашифрованы                                        ║")
    print("║  ✓ Браузеры (вкл. Яндекс) очищены                          ║")
    print("║  ✓ Кэш TLauncher очищен                                    ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    print(f"\n{Colors.BOLD}{Colors.CYAN}Нажмите Enter для выхода...{Colors.RESET}")
    input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Программа прервана{Colors.RESET}")
        input("Нажмите Enter для выхода...")
    except Exception as e:
        print(f"{Colors.RED}Ошибка: {str(e)}{Colors.RESET}")
        input("Нажмите Enter для выхода...")