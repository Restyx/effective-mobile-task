from datetime import date
from math import ceil
from os import system

class Account:
    def get_operation_list(self) -> list:
        # Считывает строки из текстового файла, форматирует их в список и создает объект operation для каждой записи
        try:
            file = open("account-history.txt", mode="r", encoding="utf-8")
            file_lines = file.readlines()
            operations: list = []
            operations_count = ceil(len(file_lines)/5) 

            for n in range(operations_count):
                elements: list = []

                for i, row in enumerate(file_lines[n*5:n*5+4]):
                    match i:
                        case 0:
                            date_list = row.lstrip('Дата: ').rstrip('\n').split('-')
                            date_list = list(map(int, date_list))
                            elements.append(date(date_list[0], date_list[1], date_list[2]))
                        case 1:
                            elements.append(row.lstrip('Категория: ').rstrip('\n'))
                        case 2:
                            elements.append(int(row.lstrip('Сумма: ').rstrip('\n')))
                        case 3:
                            elements.append(row.lstrip('Описание: ').rstrip('\n'))
                
                operation = Operation(elements[1], elements[2], elements[3], elements[0])
                operations.append(operation)
                        
            return operations
        
        except Exception as error:
            print(f"Unexpected: {error}")

        finally:
            file.close()

    def calculate_balance(self) -> int:
        # расчитывает баланс аккаунта суммируя доходы и расходы в текстовом файле
        operation_list: list = self.get_operation_list()
        account_balance: int = 0

        for operation in operation_list:
            match operation.get_type():
                case 'Доход':
                    account_balance += operation.get_value()
                case 'Расход':
                    account_balance -= operation.get_value()

        return account_balance

    def add_operation(self, operation_date: date, operation_type: str, operation_value: int, operation_description: str, file_name: str = "account-history.txt") -> None:
        # Принимает данные для записи, создает объект Operation и добавляет этот объект в конце тестого файла
        try:
            file = open(file_name, mode="a", encoding="utf-8")
            operation: Operation = Operation(operation_type, operation_value, operation_description, operation_date)
            file.writelines(operation.export())

        except Exception as error:
            return f"Ошибка: {error}\n"

        finally:
            file.close()

    def update_operation(self, operation_list: list, file_name: str = "account-history.txt") -> None:
        # Принимает лист объектов операций и переписывает текстовый файл
        try:
            file = open(file_name, mode="w", encoding="utf-8")
            lines: list = []

            for operation in operation_list:
                operation_elements = operation.export()

                for element in operation_elements:
                    lines.append(element)            
            file.writelines(lines)

        except Exception as error:
            return f"Ошибка: {error}\n"

        finally:
            file.close()
    
    def search_operation(self, search_key: int, search_criteria: None) -> None:
        # Принимает ключ и значение для поиска и выводит в консоль соответствующие записи
        try:
            operation_list: list = self.get_operation_list()
            response: str = ''

            for operation in operation_list:
                match search_key:
                    case 1:
                        # Дата
                        if operation.get_date() == search_criteria: response +=''.join(operation.export())
                    case 2:
                        # Категория
                        if operation.get_type() == search_criteria.capitalize(): response +=''.join(operation.export())
                    case 3:
                        # Сумма
                        if eval(f"{str(operation.get_value())}{search_criteria}"): response +=''.join(operation.export())
                    case 4:
                        # Описание
                        if search_criteria in operation.get_description(): response +=''.join(operation.export())
            
            return response
        
        except Exception as error:
            return f"Unexpected: {error}"

class Operation:
    def __init__(self, type: str, value: int, description: str, input_date: date = date.today()) -> None:
        self._date: date = input_date
        self._type: str = type
        self._value: int = value
        self._description: str = description

    def export(self) -> list:
        # служит для экспорта информации о записи другим функциям  
        lines = [f"Дата: {self._date}\n", f"Категория: {self._type}\n", f"Сумма: {self._value}\n", f"Описание: {self._description}\n", "\n"]
        return lines
    
    # Гетеры и Сетеры
    def get_date(self) -> date:
        return self._date

    def get_type(self) -> str:
        return self._type
    
    def get_value(self) -> int:
        return self._value
    
    def get_description(self) -> str:
        return self._description
    
    def set_date(self, date: date) -> None:
        self._date = date
    
    def set_type(self, type: str) -> None:
        self._type = type
    
    def set_value(self, value: int) -> None:
        self._value = value
    
    def set_description(self, description: str) -> None:
        self._description = description


def message_handler(message: int, account: Account, ) -> str:
    match message:
        case 1:
            balance: int = account.calculate_balance()
            response: str = f"Ваш баланс составляет: {balance}"
            return response
        
        case 2:
            try:
                input_date: date = date(int(input("Введите год: ")), int(input("Введите месяц: ")), int(input("Введите день: ")))
                input_type: str = input("Введите категорию (доход / расход): ").title()
                input_value: int = int(input("Введите сумму: "))
                input_description: str = input("Введите описание: ")
                
                account.add_operation(input_date, input_type, input_value, input_description)

                return "Операция успешно добавлена!"

            except Exception as error:
                return f"Ошибка: {error}\n"

        case 3:
            try:
                print("Выберите операцию для редактирования...")
                print("ID")
                
                operation_list: list = account.get_operation_list()
                
                for index, operation in enumerate(operation_list):
                    print(index, operation.get_date(), operation.get_type(), operation.get_value(), operation.get_description(), sep="\t")
                
                selected_operation_index: int = int(input("Выбрать ID: "))

                if selected_operation_index > len(operation_list)-1 or selected_operation_index < 0: raise ValueError("Выбран некоректный ID")

                print("Выберите атрибут для редактирования...")
                print("[1] Дата")
                print("[2] Категория")
                print("[3] Сумма")
                print("[4] Описание")

                attribute_dict: dict = {
                    1: "Дата",
                    2: "Категория",
                    3: "Сумма",
                    4: "Описание"
                }

                selected_attribute: int = int(input("№: "))
                print("Введите новое значение атрибута...")
                
                if selected_attribute > 4 or selected_attribute < 0: raise ValueError("Выбран некоректный атрибут")
                
                match attribute_dict[selected_attribute]:
                    case "Дата":
                        new_value: date = date(int(input("Введите год: ")), int(input("Введите месяц: ")), int(input("Введите день: ")))
                        
                        operation_list[selected_operation_index].set_date(new_value)
                        
                    case "Категория":
                        print("[1] Доход")
                        print("[2] Расход")

                        new_value: int = int(input("Категория: "))
                        type_dict: dict = {
                            1: "Доход",
                            2: "Расход"
                        }
                        operation_list[selected_operation_index].set_type(type_dict[new_value])

                    case "Сумма":
                        new_value: int = int(input("Сумма: "))
                        operation_list[selected_operation_index].set_value(new_value)

                    case "Описание":
                        new_value: str = input("Описание: ")
                        operation_list[selected_operation_index].set_description(new_value)
                account.update_operation(operation_list)
                return "Операция успешно отредактирована!"
            
            except Exception as error:
                return f"Ошибка: {error}\n"
        case 4:
            print("Выберите атрибут по которому будет происходить поиск...")
            print("[1] Дата")
            print("[2] Категория")
            print("[3] Сумма")
            print("[4] Описание")

            selected_attribute: int = int(input("№: "))

            print("Введите значение атрибута поиска...")
            if selected_attribute == 1: selected_value: date = date(int(input("Введите год: ")), int(input("Введите месяц: ")), int(input("Введите день: ")))
            else: selected_value: str = input("Значение: ")

            return account.search_operation(selected_attribute, selected_value)
        case _:
            return "Некоректное значение! Пожалуйста введите число от 1 до 4"


if __name__ == "__main__":
    account = Account()
    file = open("account-history.txt", "a+")
    file.close()

    while True:
        try:
            print("Выберите функцию (введите число от 1 до 4):")
            print("[1] Проверить баланс")
            print("[2] Добавить операцию")
            print("[3] Редактировать операцию")
            print("[4] Поиск")

            input_data: int = int(input("Выбрать: "))
            response = message_handler(input_data, account)
            system("cls")
            print(response, "\n\n")
        except Exception as error:
            system("cls")
            print(f"Ошибка! {error}")