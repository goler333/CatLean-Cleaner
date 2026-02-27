#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import ctypes
import time
import getpass
import datetime
import random


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


class StealthCleaner:
    def __init__(self):
        self.username = getpass.getuser()
        self.start_time = datetime.datetime.now()
        self.deleted_count = 0
        self.kept_count = 0

    # Пункт 2: Оставляем "невинные" файлы
    def create_innocent_files(self, folder_path):
        """Создает случайные 'мусорные' файлы, чтобы не было пустоты"""
        innocent_names = [
            "temp_log.txt",
            "cache.dat",
            "browser_cache.tmp",
            "system_scan.log",
            "update_temp.bin",
            "installer_temp.exe",
            "dxdiag_output.txt",
            "msconfig_backup.log",
            "defender_scan.tmp",
            "windows_update.cab"
        ]

        # Создаем 2-3 случайных файла
        created = 0
        for _ in range(random.randint(2, 3)):
            name = random.choice(innocent_names)
            path = os.path.join(folder_path, name)
            if not os.path.exists(path):
                try:
                    with open(path, 'w') as f:
                        f.write(f"Generated at {datetime.datetime.now()}\n")
                        f.write("x" * random.randint(100, 1000))
                    log(f"Создан системный файл: {name}", "warning")
                    created += 1
                except:
                    pass

        if created > 0:
            log(f"Создано {created} служебных файлов для естественности", "success")

    # Пункт 3: Очистка с "шумом" (не все файлы)
    def noisy_cleanup(self, folder_path, description):
        """Удаляет не все файлы, а большинство"""
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

            # Перемешиваем
            random.shuffle(files)

            # Удаляем 70-90% файлов, оставляя остальные
            delete_percent = random.randint(70, 90)
            delete_count = int(len(files) * delete_percent / 100)

            log(f"Обработка {description}: найдено {len(files)} файлов", "info")

            deleted = 0
            kept = 0

            for i, file in enumerate(files[:delete_count]):
                # 10% шанс пропустить файл даже если он должен быть удален
                if random.random() > 0.1:
                    file_path = os.path.join(folder_path, file)
                    try:
                        size = os.path.getsize(file_path)
                        os.remove(file_path)
                        log(f"  Удален: {file} ({size} байт)", "success")
                        deleted += 1
                        self.deleted_count += 1
                    except:
                        log(f"  Не удалось удалить: {file}", "warning")
                        kept += 1
                else:
                    log(f"  Пропущен (случайно): {file}", "warning")
                    kept += 1
                    self.kept_count += 1

            # Оставшиеся файлы (которые не попали в список на удаление)
            kept += len(files) - delete_count
            self.kept_count += len(files) - delete_count

            log(f"{description}: удалено {deleted}, оставлено {kept}", "success")

        except Exception as e:
            log(f"Ошибка при очистке {description}: {str(e)}", "error")

    # Пункт 4: Изменяем даты файлов
    def randomize_file_dates(self, folder_path, description):
        """Меняет даты создания файлов на случайные в пределах недели"""
        if not os.path.exists(folder_path):
            return

        try:
            changed = 0
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    # Случайная дата в пределах последних 7 дней
                    random_days = random.randint(1, 7)
                    random_hours = random.randint(0, 23)
                    random_minutes = random.randint(0, 59)

                    random_time = datetime.datetime.now() - datetime.timedelta(
                        days=random_days,
                        hours=random_hours,
                        minutes=random_minutes
                    )

                    try:
                        # Меняем время модификации
                        os.utime(item_path, (random_time.timestamp(), random_time.timestamp()))
                        changed += 1
                    except:
                        pass

            if changed > 0:
                log(f"{description}: обновлены даты у {changed} файлов", "success")

        except Exception as e:
            log(f"Ошибка при изменении дат {description}: {str(e)}", "error")

    # Пункт 6: Создание "ложных следов"
    def create_fake_traces(self):
        """Создает старые записи в недавних документах"""
        recent_path = f"C:\\Users\\{self.username}\\AppData\\Roaming\\Microsoft\\Windows\\Recent"

        if not os.path.exists(recent_path):
            return

        fake_programs = [
            "Google Chrome",
            "Microsoft Edge",
            "Notepad++",
            "7-Zip",
            "WinRAR",
            "Adobe Reader",
            "Microsoft Word",
            "Excel",
            "PowerPoint",
            "Paint"
        ]

        fake_files = [
            "document.txt",
            "image.jpg",
            "presentation.pptx",
            "spreadsheet.xlsx",
            "archive.zip",
            "report.pdf",
            "notes.txt",
            "backup.rar"
        ]

        created = 0

        # Создаем 3-5 ложных следов
        for _ in range(random.randint(3, 5)):
            prog = random.choice(fake_programs)
            file_name = random.choice(fake_files)

            # Создаем уникальное имя
            fake_file = f"{prog.replace(' ', '_')}_{random.randint(100, 999)}_{file_name}"
            fake_path = os.path.join(recent_path, fake_file)

            try:
                # Создаем пустой файл
                with open(fake_path, 'w') as f:
                    f.write(f"Opened with {prog} at {datetime.datetime.now()}")

                # Делаем дату "старой" (3-10 дней назад)
                old_date = datetime.datetime.now() - datetime.timedelta(
                    days=random.randint(3, 10),
                    hours=random.randint(0, 23)
                )
                os.utime(fake_path, (old_date.timestamp(), old_date.timestamp()))

                log(f"Создан ложный след: {fake_file} (от {old_date.strftime('%Y-%m-%d')})", "warning")
                created += 1

            except:
                pass

        if created > 0:
            log(f"Создано {created} ложных следов в недавних документах", "success")

    # Основная функция очистки
    def clean(self):
        log("=" * 60, "info")
        log("НАЧАЛО ОЧИСТКИ", "info")
        log("=" * 60, "info")

        # 1. Удаление папки .ctl (всегда полностью)
        ctl_path = f"C:\\Users\\{self.username}\\.ctl"
        if os.path.exists(ctl_path):
            try:
                # Считаем файлы
                file_count = 0
                for root, dirs, files in os.walk(ctl_path):
                    file_count += len(files)

                shutil.rmtree(ctl_path, ignore_errors=True)
                log(f"Папка .ctl полностью удалена (содержала {file_count} файлов)", "success")
                self.deleted_count += file_count
            except Exception as e:
                log(f"Ошибка при удалении .ctl: {str(e)}", "error")
        else:
            log("Папка .ctl не найдена", "warning")

        # 2. Очистка недавних файлов с "шумом" + изменение дат
        recent_path = f"C:\\Users\\{self.username}\\AppData\\Roaming\\Microsoft\\Windows\\Recent"

        # Пункт 3: Очистка с шумом
        self.noisy_cleanup(recent_path, "Недавние файлы")

        # Пункт 4: Изменение дат
        self.randomize_file_dates(recent_path, "Недавние файлы")

        # Пункт 2: Создание невинных файлов
        self.create_innocent_files(recent_path)

        # 3. Очистка TEMP
        temp_path = os.environ.get('TEMP', '')
        if temp_path:
            self.noisy_cleanup(temp_path, "Пользовательская TEMP")
            self.randomize_file_dates(temp_path, "Пользовательская TEMP")
            self.create_innocent_files(temp_path)

        system_temp = "C:\\Windows\\Temp"
        self.noisy_cleanup(system_temp, "Системная TEMP")
        self.randomize_file_dates(system_temp, "Системная TEMP")
        self.create_innocent_files(system_temp)

        # 4. Очистка Prefetch
        prefetch_path = "C:\\Windows\\Prefetch"
        if os.path.exists(prefetch_path):
            self.noisy_cleanup(prefetch_path, "Prefetch")
            self.randomize_file_dates(prefetch_path, "Prefetch")
            self.create_innocent_files(prefetch_path)

        # Пункт 6: Создание ложных следов
        self.create_fake_traces()

        log("=" * 60, "info")
        log("ИТОГИ ОЧИСТКИ", "info")
        log("=" * 60, "info")
        log(f"Всего удалено файлов: {self.deleted_count}", "success")
        log(f"Всего оставлено файлов: {self.kept_count}", "warning")


def main():
    # Очистка экрана
    os.system('cls')

    # Заголовок
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║              СИСТЕМНОЕ ОБСЛУЖИВАНИЕ v1.0                  ║")
    print("║              (оптимизация и очистка)                       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    # Получаем имя пользователя
    username = getpass.getuser()
    print(f"{Colors.BOLD}Пользователь: {Colors.CYAN}{username}{Colors.RESET}")
    print(f"{Colors.BOLD}Время запуска: {Colors.CYAN}{time.strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
    print()

    # Проверка прав администратора
    if not is_admin():
        log("Запуск от имени администратора...", "info")
        run_as_admin()
        return

    # Запуск очистки
    cleaner = StealthCleaner()
    cleaner.clean()

    # Финальное сообщение
    print(f"\n{Colors.BOLD}{Colors.GREEN}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║              ОБСЛУЖИВАНИЕ ЗАВЕРШЕНО                        ║")
    print("║              Система оптимизирована                        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    # Ожидание нажатия Enter
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