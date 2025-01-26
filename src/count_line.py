import os

def count_python_lines(directory='.'):
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    total_lines += len(lines)
                    print(f"{file_path}: {len(lines)} lines")
    print(f"\nTotal number of lines in Python files: {total_lines}")

count_python_lines()
