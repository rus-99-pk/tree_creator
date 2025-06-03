import os
import re
import shutil
import json

def parse_tree_definition(lines):
    root_structure = {}
    # Стек: (глубина, ссылка_на_узел). Глубина -1 для root_structure.
    node_stack = [(-1, root_structure)]

    for line_num, original_line_from_file in enumerate(lines):

        # 1. Стандартизация пробелов и удаление \n
        current_line_text = original_line_from_file.replace('\xa0', ' ').rstrip()

        if not current_line_text.strip():
            continue

        # 2. Извлечение префикса (символы дерева + пробелы до имени) и имени элемента
        #    Паттерн: ^(?P<prefix>[│├──└── \t]*)(?P<name>.*)
        #    prefix: все символы дерева и пробелы/табы в начале
        #    name: остальная часть строки
        match = re.match(r'^(?P<prefix>[│├──└── \t]*)(?P<name>.*)', current_line_text)
        
        if not match: # Маловероятно, если строка не пустая
            continue

        prefix_part = match.group('prefix')
        item_name_candidate = match.group('name').strip()


        if not item_name_candidate:
            continue
        
        clean_item_name = item_name_candidate

        # 3. Обработка корневого элемента '.'
        if clean_item_name == '.' and line_num == 0:
            # Точка '.' обычно не имеет префикса или имеет минимальный отступ, если все дерево сдвинуто.
            # Мы считаем ее концептуальным родителем с глубиной -1.
            continue

        # 4. Вычисление эффективной глубины на основе длины префикса
        #    L = 4 + D * 3  => D = (L - 4) / 3
        #    Где D - глубина (0 для первого уровня, 1 для второго и т.д.)
        #    L - длина префикса (len(prefix_part))
        
        prefix_len = len(prefix_part)
        current_effective_depth = -1

        if prefix_len < 4:
            current_effective_depth = 0
        else:
            if (prefix_len - 4) % 3 == 0:
                current_effective_depth = (prefix_len - 4) // 3
            else:
                current_effective_depth = (prefix_len - 4) // 3 

        item_name = clean_item_name
        is_file = '.' in item_name and not item_name.endswith('/') and not item_name.endswith(os.sep)

        # 5. Корректировка стека узлов
        while node_stack and node_stack[-1][0] >= current_effective_depth:
            popped_depth, _ = node_stack.pop()

        if not node_stack:
            print(f" CRITICAL ERROR: Stack is empty! Cannot find parent of '{item_name}' at line {line_num+1}.")
            raise ValueError(f"Стек пуст для элемента '{item_name}'")

        parent_depth, parent_node = node_stack[-1]

        # 6. Добавление элемента в структуру
        if is_file:
            parent_node[item_name] = None
        else:
            new_directory_node = {}
            parent_node[item_name] = new_directory_node
            node_stack.append((current_effective_depth, new_directory_node))

    return root_structure

def create_filesystem_structure(base_path, tree_dict):
    for name, content in tree_dict.items():
        item_path = os.path.join(base_path, name)
        if content is None:
            os.makedirs(os.path.dirname(item_path), exist_ok=True)
            with open(item_path, 'w', encoding='utf-8') as f: pass
            print(f" Created file: {item_path}")
        else:
            os.makedirs(item_path, exist_ok=True)
            print(f" Created directory: {item_path}")
            create_filesystem_structure(item_path, content)

def main():
    input_filename = "tree_definition.txt"
    output_base_directory = "my_project"

    if not os.path.exists(input_filename):
        print(f"Creating sample file '{input_filename}'...")
        sample_content = """
./
├── file1.txt
├── file2.ini
├── dir1
│   └── file1.txt
├── dir2
│   ├── dir1
│   │   ├── dir1
│   │   │   └── file1.yml
│   │   └── dir2
│   │       └── file2.yaml
└── file3.yml
        """.strip()
        with open(input_filename, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"Sample file '{input_filename}' created.")
        return

    print(f"Reading tree definition from: '{input_filename}'")
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return

    parsed_tree = {}
    try:
        parsed_tree = parse_tree_definition(lines)
    except Exception as e:
        print(f"\nCRITICAL ERROR DURING PARSING: {e}")
        import traceback
        traceback.print_exc()
        print("\nStructure at time of error (if any):")
        # Показать, что успело распарситься
        print(json.dumps(parsed_tree, indent=2))
        return

    if os.path.exists(output_base_directory):
        print(f"\nDeleting existing directory: '{output_base_directory}'...")
        try:
            shutil.rmtree(output_base_directory)
        except OSError as e:
            print(f"Error deleting '{output_base_directory}': {e}")
            return
            
    print(f"\nCreating directory structure in: '{output_base_directory}'")
    os.makedirs(output_base_directory, exist_ok=True)
    try:
        create_filesystem_structure(output_base_directory, parsed_tree)
        print(f"\nDirectory structure successfully created in '{output_base_directory}'.")
    except Exception as e:
        print(f"Error creating file system: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()