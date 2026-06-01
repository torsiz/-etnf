import subprocess
import sys
import os
import colorama  # ИМПОРТИРУЕМ COLORAMA

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def run_pip_command(command: list):
    try:
        full_command = [sys.executable, '-m', 'pip'] + command
        print(f"{Colors.OKCYAN}▶ Выполняется команда: {' '.join(full_command)}{Colors.ENDC}")
        result = subprocess.run(full_command, check=True, capture_output=True, text=True, encoding='utf-8')
        if result.stdout: print(result.stdout)
        print(f"\n{Colors.OKGREEN}✅ Команда выполнена успешно!{Colors.ENDC}")
        return True, result.stdout
    except FileNotFoundError:
        print(f"{Colors.FAIL}❌ Ошибка: 'pip' не найден.{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.FAIL}❌ Произошла ошибка.{Colors.ENDC}")
        print(f"{Colors.WARNING}Сообщение от pip:{Colors.ENDC}\n{e.stderr}")
    return False, None

def install_package():
    package_name = input("Введите имя пакета для установки: ")
    if package_name: run_pip_command(['install', package_name])
    else: print(f"{Colors.WARNING}Имя пакета не может быть пустым.{Colors.ENDC}")

def uninstall_package():
    package_name = input("Введите имя пакета для удаления: ")
    if package_name: run_pip_command(['uninstall', package_name, '-y'])
    else: print(f"{Colors.WARNING}Имя пакета не может быть пустым.{Colors.ENDC}")

def update_package():
    package_name = input("Введите имя пакета для обновления: ")
    if package_name: run_pip_command(['install', '--upgrade', package_name])
    else: print(f"{Colors.WARNING}Имя пакета не может быть пустым.{Colors.ENDC}")

def list_packages():
    print("Загрузка списка установленных пакетов...")
    run_pip_command(['list'])

def install_from_requirements():
    req_file = 'requirements.txt'
    if os.path.exists(req_file):
        print(f"Найден файл {req_file}. Начинаю установку пакетов...")
        run_pip_command(['install', '-r', req_file])
    else:
        print(f"{Colors.FAIL}Файл {req_file} не найден в текущей директории.{Colors.ENDC}")

def freeze_to_requirements():
    print("Сохранение списка пакетов в requirements.txt...")
    success, output = run_pip_command(['freeze'])
    if success and output:
        try:
            with open('requirements.txt', 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"{Colors.OKGREEN}Файл requirements.txt успешно создан/обновлен!{Colors.ENDC}")
        except IOError as e:
            print(f"{Colors.FAIL}Не удалось записать в файл: {e}{Colors.ENDC}")

def show_menu():
    print(f"\n{Colors.HEADER}{Colors.BOLD}--- Консольный Пакетный Менеджер v2.0 ---{Colors.ENDC}")
    print("1. Установить пакет")
    print("2. Удалить пакет")
    print("3. Обновить пакет")
    print("4. Показать список установленных пакетов")
    print("-" * 20)
    print("5. Установить из requirements.txt")
    print("6. Сохранить в requirements.txt (freeze)")
    print("-" * 20)
    print(f"7. {Colors.FAIL}Выход{Colors.ENDC}")
    return input(f"{Colors.OKBLUE}Выберите действие (1-7): {Colors.ENDC}")

def main():
    colorama.init(autoreset=True)
    
    while True:
        choice = show_menu()
        actions = {
            '1': install_package, '2': uninstall_package, '3': update_package,
            '4': list_packages, '5': install_from_requirements, '6': freeze_to_requirements,
        }
        if choice in actions:
            actions[choice]()
        elif choice == '7':
            print(f"{Colors.OKCYAN}Завершение работы...{Colors.ENDC}")
            break
        else:
            print(f"{Colors.WARNING}Неверный выбор.{Colors.ENDC}")
        input("\nНажмите Enter, чтобы продолжить...")

if __name__ == "__main__":
    main()