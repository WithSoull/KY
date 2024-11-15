import os
import sys
import subprocess
import re

def parse_pyproject_toml(pyproject_path, root_package):
    """
    Простейший парсер для извлечения зависимостей из файла pyproject.toml.
    Возвращает список пар (root_package, dependency).
    """
    dependencies = []
    with open(pyproject_path, 'r') as file:
        in_dependencies_section = False
        
        for line in file:
            line = line.strip()
            
            # Определяем, что мы вошли в нужный раздел
            if line == "[tool.poetry.dependencies]" or line == "[project.dependencies]":
                in_dependencies_section = True
                continue
            # Если встречаем другой раздел, выходим из текущего
            elif line.startswith("[") and in_dependencies_section:
                break

            # Считываем зависимости в нужном разделе
            if in_dependencies_section and line:
                match = re.match(r'^([\w\-]+)\s*=.*', line)
                if match:
                    dependency = match.group(1)
                    if dependency != "python":  # Исключаем сам Python
                        dependencies.append((root_package, dependency))
                        
    return dependencies

def parse_requirements_txt(requirements_path, root_package):
    """
    Парсит зависимости из файла requirements.txt и возвращает список пар (root_package, dependency).
    """
    dependencies = []
    with open(requirements_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                dependency = line.split('==')[0]
                dependencies.append((root_package, dependency))
    return dependencies

def get_dependencies(package_path, root_package):
    """
    Определяет зависимости пакета, проверяя файлы pyproject.toml и requirements.txt.
    Возвращает зависимости в виде списка пар (root_package, dependency).
    """
    print(f"Содержимое директории {package_path}: {os.listdir(package_path)}")
    dependencies = []
    pyproject_path = os.path.join(package_path, 'pyproject.toml')
    requirements_path = os.path.join(package_path, 'requirements.txt')
    
    if os.path.exists(pyproject_path):
        dependencies = parse_pyproject_toml(pyproject_path, root_package)
    elif os.path.exists(requirements_path):
        dependencies = parse_requirements_txt(requirements_path, root_package)
    else:
        print("Файл pyproject.toml или requirements.txt не найден.")
    
    return dependencies

def build_dependency_graph(package, dependencies, max_depth, current_depth=0, visited=None):
    """
    Рекурсивно строит граф зависимостей пакета до указанной глубины.
    """
    if visited is None:
        visited = set()
    
    if current_depth >= max_depth or package in visited:
        return []
    
    visited.add(package)
    graph = dependencies.copy()  # Начинаем с зависимостей корневого пакета
    
    # Рекурсивно обрабатываем каждую зависимость
    for _, dep in dependencies:
        dep_path = os.path.join(package_path, dep)
        if os.path.isdir(dep_path):
            sub_dependencies = get_dependencies(dep_path, dep)
            graph.extend(build_dependency_graph(dep, sub_dependencies, max_depth, current_depth + 1, visited))
    
    return graph

def generate_plantuml_graph(dependencies):
    """
    Генерирует текстовое представление графа в формате PlantUML.
    """
    uml = "@startuml\n"
    for parent, child in dependencies:
        uml += f"\"{parent}\" --> \"{child}\"\n"
    uml += "@enduml\n"
    return uml

def save_to_file(content, filename):
    """
    Сохраняет содержимое в файл.
    """
    with open(filename, 'w') as f:
        f.write(content)

def visualize_graph(uml_path, plantuml_path):
    """
    Вызывает команду для генерации графического изображения с использованием PlantUML.
    """
    try:
        subprocess.run(['java', '-jar', plantuml_path, uml_path], check=True)
        print(f"Граф сохранен как изображение: {uml_path.replace('.uml', '.png')}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при вызове PlantUML: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Использование: python graph_visualizer.py <путь к PlantUML> <путь к пакету> <глубина>")
        sys.exit(1)

    plantuml_path = sys.argv[1]
    package_path = sys.argv[2]
    max_depth = int(sys.argv[3])

    # Получаем корневой пакет
    root_package = os.path.basename(os.path.normpath(package_path))

    # Получаем зависимости корневого пакета
    root_dependencies = get_dependencies(package_path, root_package)

    # Строим граф зависимостей
    dependency_graph = build_dependency_graph(root_package, root_dependencies, max_depth)

    # Генерация графа PlantUML
    uml_graph = generate_plantuml_graph(dependency_graph)
    uml_file = "dependencies.uml"
    save_to_file(uml_graph, uml_file)

    # Визуализация графа
    visualize_graph(uml_file, plantuml_path)
