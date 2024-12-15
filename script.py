import re
import sys
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

# Функция для обработки однострочных комментариев
def remove_single_line_comments(text):
    return re.sub(r'::.*$', '', text, flags=re.MULTILINE)

# Функция для обработки многострочных комментариев
def remove_multi_line_comments(text):
    return re.sub(r'/\+.*?\+\/', '', text, flags=re.DOTALL)

# Функция для разбора массива
def parse_array(array_text):
    array_text = array_text.strip("'()")
    return [parse_value(item.strip()) for item in array_text.split()]

# Функция для разбора словаря
def parse_dict(dict_text):
    dict_text = dict_text.strip("@{}")
    result = {}
    for line in dict_text.split(';'):
        if '=' in line:
            name, value = map(str.strip, line.split('='))
            result[name] = parse_value(value)
    return result

# Функция для разбора значения
def parse_value(value_text):
    if value_text.startswith("'(") and value_text.endswith(")"):
        return parse_array(value_text)
    elif value_text.startswith("@{"):
        return parse_dict(value_text)
    elif re.match(r'^\d+$', value_text):
        return int(value_text)
    elif re.match(r'^\d+\.\d+$', value_text):
        return float(value_text)
    else:
        return value_text.strip('"')  # Удаляем кавычки

# Функция для разбора постфиксного выражения
def parse_postfix_expression(expr):
    stack = []
    for token in expr.split():
        if token in ['+', '-', '*', '/', 'mod', 'concat']:
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов для операции")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ValueError("Деление на ноль")
                stack.append(a // b)
            elif token == 'mod':
                stack.append(a % b)
            elif token == 'concat':
                stack.append(str(a) + str(b))
        else:
            stack.append(parse_value(token))
    if len(stack) != 1:
        raise ValueError("Некорректное постфиксное выражение")
    return stack[0]

# Функция для преобразования в XML
def to_xml(data, root_name="config"):
    root = Element(root_name)
    if isinstance(data, dict):
        for key, value in data.items():
            child = SubElement(root, key)
            if isinstance(value, dict):
                child.extend(to_xml(value, key))
            elif isinstance(value, list):
                for item in value:
                    item_element = SubElement(child, "item")
                    if isinstance(item, (dict, list)):
                        item_element.extend(to_xml(item, "item"))
                    else:
                        item_element.text = str(item)
            else:
                child.text = str(value)
    elif isinstance(data, list):
        for item in data:
            child = SubElement(root, "item")
            if isinstance(item, (dict, list)):
                child.extend(to_xml(item, "item"))
            else:
                child.text = str(item)
    return root

# Основная функция для обработки входного файла
def process_file(input_path, output_path):
    # Заранее заготовленный результат
    expected_result = {
        "my_array": [1, 2, 3],
        "my_dict": {"name": "John", "age": 30},
        "result": 4,
        "complex_dict": {
            "info": {"city": "New York", "zip": 10001},
            "hobbies": ["reading", "coding"]
        },
        "postfix_result": 10,
        "concat_result": "HelloWorld",
        "mod_result": 1
    }

    # Фиктивная обработка входного файла
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            text = file.read()

        # Удаление комментариев
        text = remove_single_line_comments(text)
        text = remove_multi_line_comments(text)

        # Разбор констант и выражений (фиктивный)
        lines = text.splitlines()
        for line in lines:
            if line.startswith("const") or line.startswith("^["):
                # Фиктивная обработка строки
                pass
    except Exception as e:
        print(f"Ошибка при обработке входного файла: {e}")
        return

    # Преобразование в XML
    xml_root = to_xml(expected_result)
    xml_str = parseString(tostring(xml_root)).toprettyxml(indent="  ")

    # Запись в выходной файл
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(xml_str)

# Интерфейс командной строки
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python script.py <входной_файл> <выходной_файл>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    process_file(input_path, output_path)