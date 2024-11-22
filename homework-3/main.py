import json
import re
import argparse
import sys


class ConfigTranslator:
    def __init__(self):
        self.constants = {}

    def translate(self, data):
        if isinstance(data, dict):
            return self._translate_dict(data)
        elif isinstance(data, list):
            return self._translate_array(data)
        else:
            raise ValueError("Корневой элемент JSON должен быть объектом или массивом")

    def _translate_dict(self, data):
        result = []
        for key, value in data.items():
            if key == "_comment":  # Обработка комментариев
                result.append(f"! {value}")
                continue
            if isinstance(value, (int, float)):
                result.append(f"{key} is {value};")
            elif isinstance(value, str):
                result.append(f'{key} is [[{value}]];')
            elif isinstance(value, list):
                result.append(f"{key} is {self._translate_array(value)};")
            elif isinstance(value, dict):
                self.constants[key] = self._translate_dict(value)
                result.append(f"{key} is {{{key}}};")
            else:
                raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")
        return "\n".join(result)

    def _translate_array(self, data):
        values = []
        for item in data:
            if isinstance(item, (int, float)):
                values.append(str(item))
            elif isinstance(item, str):
                values.append(f"[[{item}]]")
            elif isinstance(item, list):
                values.append(self._translate_array(item))
            else:
                raise ValueError(f"Неподдерживаемый элемент массива: {type(item)}")
        return f"#( {' '.join(values)} )"

    def parse_constants(self, text):
        for name, value in self.constants.items():
            text = re.sub(rf"{{\b{name}\b}}", value, text)
        return text


def main():
    parser = argparse.ArgumentParser(description="Инструмент для преобразования JSON в учебный конфигурационный язык.")
    parser.add_argument("input", help="Путь к входному JSON-файлу")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Ошибка: Некорректный JSON. {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Ошибка: Файл {args.input} не найден.", file=sys.stderr)
        sys.exit(1)

    translator = ConfigTranslator()
    try:
        output = translator.translate(data)
        output = translator.parse_constants(output)
        print(output)
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
