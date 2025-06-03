# Создание Структуры Каталогов / Directory Tree Creator

## Русский

Python-скрипт, который создает структуру каталогов и файлов на основе текстового файла, отформатированного как вывод команды `tree`. Это полезно для быстрого создания макетов проектов

### Особенности
*   Разбирает (парсит) текстовое представление структуры каталогов, похожее на вывод `tree`.
*   Создает соответствующие каталоги и пустые файлы в файловой системе.
*   Обрабатывает стандартные символы команды `tree` (`├──`, `└──`, `│`).
*   Имя базового выходного каталога и имя входного файла определения можно настроить непосредственно в скрипте.

### Как использовать

1.  **Подготовьте файл определения:**
    *   Создайте текстовый файл (например, `tree_definition.txt`).
    *   Заполните его желаемой структурой каталогов, имитируя вывод команды `tree`.
        *   Используйте `.` в качестве первой строки, если вы хотите, чтобы вся структура была создана *внутри* каталога `output_base_directory`, указанного в скрипте. Если `.` опущен, элементы будут созданы непосредственно *в* `output_base_directory`.
    *   **Пример `tree_definition.txt`:**
        ```
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
        ```

2.  **Настройте (необязательно):**
    *   Откройте файл `main.py`.
    *   Измените `input_filename`, если ваш файл определения называется иначе.
    *   Измените `output_base_directory`, чтобы указать, где будет создана структура.

3.  **Запустите скрипт:**
    ```bash
    python main.py
    ```

4.  **Результат:**
    Скрипт создаст указанную структуру каталогов и файлов внутри `output_base_directory` (по умолчанию это `my_project` или аналогичное имя, в зависимости от используемой версии скрипта).

### Важные замечания по формату `tree_definition.txt`:

*   **Корневой элемент (`.`):** Если первая строка - это `.`, это означает, что последующие элементы являются дочерними для `output_base_directory`. Сам символ `.` не создает папку с именем ".".
*   **Символы:** Используйте стандартные символы `tree`:
    *   `├──` для элемента, который не является последним на своем уровне.
    *   `└──` для последнего элемента на своем уровне.
    *   `│` для вертикальных линий, соединяющих родительские и дочерние ветви.
*   **Отступы и Префиксы:** Скрипт в первую очередь полагается на *точные шаблоны префиксов*, генерируемые командой `tree` для расчета глубины (например, `├── имя`, `│   ├── имя`, `│   │   ├── имя`). Количество пробелов *внутри* этих префиксов (например, три пробела в `│   `) имеет решающее значение.
*   **Файлы и Каталоги:** Элементы с распространенным расширением файла (содержащие точку `.`) рассматриваются как файлы (например, `main.py`, `all.yml`). Элементы без расширения обычно рассматриваются как каталоги.

* * *

## English

A Python script that creates a directory and file structure based on a text file formatted like the output of the `tree` command. This is useful for quickly scaffolding project layouts or Ansible role structures.

### Features
*   Parses `tree`-like textual representation of a directory structure.
*   Creates corresponding directories and empty files on the filesystem.
*   Handles common `tree` command symbols (`├──`, `└──`, `│`).
*   The output base directory and input definition filename can be configured directly within the script.

### How to Use

1.  **Prepare the Definition File:**
    *   Create a text file (e.g., `tree_definition.txt`).
    *   Populate it with your desired directory structure, mimicking the `tree` command output.
        *   Use `.` as the first line if you want the entire structure to be created *inside* the `output_base_directory` specified in the script. If `.` is omitted, items will be created directly *in* the `output_base_directory`.
    *   **Example `tree_definition.txt`:**
        ```
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
        ```

2.  **Configure (Optional):**
    *   Open `main.py`.
    *   Modify `input_filename` if your definition file has a different name.
    *   Modify `output_base_directory` to change where the structure will be created.

3.  **Run the Script:**
    ```bash
    python main.py
    ```

4.  **Output:**
    The script will create the defined directory and file structure inside the `output_base_directory` (default is `my_project` or similar, depending on the script version you are using).

### Important Notes for `tree_definition.txt` Format:

*   **Root Element (`.`):** If the first line is `.`, it signifies that subsequent items are children of the `output_base_directory`. The `.` itself does not create a folder named ".".
*   **Symbols:** Use standard `tree` symbols:
    *   `├──` for an item that is not the last in its level.
    *   `└──` for the last item in its level.
    *   `│` for vertical lines connecting parent to children branches.
*   **Indentation & Prefixes:** The script primarily relies on the *exact prefix patterns* generated by the `tree` command for depth calculation (e.g., `├── name`, `│   ├── name`, `│   │   ├── name`). The number of spaces *within* these prefixes (e.g., the three spaces in `│   `) is crucial.
*   **Files vs. Directories:** Items with a common file extension (containing a `.`) are treated as files (e.g., `main.py`, `all.yml`). Items without an extension are generally treated as directories.