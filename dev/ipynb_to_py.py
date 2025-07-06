import os
import json

def convert_ipynb_to_py(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    code_cells = [
        ''.join(cell['source'])
        for cell in notebook.get('cells', [])
        if cell.get('cell_type') == 'code'
    ]

    py_filename = filename.replace('.ipynb', '.py')
    with open(py_filename, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(code_cells))
    print(f"Converted: {filename} -> {py_filename}")

def main():
    for file in os.listdir('.'):
        if file.endswith('.ipynb') and file != 'info.ipynb':
            convert_ipynb_to_py(file)

if __name__ == '__main__':
    main()
