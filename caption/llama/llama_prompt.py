import os
import json

module_dir = os.path.dirname(__file__)
file_path_en = os.path.join(module_dir, "dataset_en.json")
file_path_id = os.path.join(module_dir, "dataset_id.json")


def load_dataset(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def datasetsEn():
    datasets = load_dataset(file_path_en)
    prompt_parts = ["\nHere are some samples of photo metadata input and the output descriptions that should be followed in writing captions:"]
    for i, item in enumerate(datasets, start=1):
        inputs = "; ".join(item["input"]) +";"  # jadikan satu baris
        output = item["output"]
        prompt_parts.append(f"{i}. Input: {inputs}  Output: {output} |")
    return " ".join(prompt_parts)

def datasetsId():
    datasets = load_dataset(file_path_id)
    prompt_parts = ["\nBerikut ini beberapa contoh input data metadata gambar dan output caption yang harus diikuti dalam menulis caption foto:"]
    
    for i, item in enumerate(datasets, start=1):
        inputs = "; ".join(item["input"]) +";"  # jadikan satu baris
        output = item["output"]
        prompt_parts.append(f"{i}. Input: {inputs}  Output: {output} |")
    return " ".join(prompt_parts)