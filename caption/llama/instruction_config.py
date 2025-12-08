import os


module_dir = os.path.dirname(__file__)
file_path_en = os.path.join(module_dir, "instruction_en.txt")
file_path_id = os.path.join(module_dir, "instruction_id.txt")


def read_instruction(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    

def get_instruction(language_code):
    if language_code == 'id':
        return read_instruction(file_path_id)
    elif language_code == 'en':
        return read_instruction(file_path_en)
    else:
        return read_instruction(file_path_en)  # Default to English if language code is unrecognized