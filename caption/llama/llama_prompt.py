import os
import json

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, "caption_datasets.json")


with open(file_path, 'r') as f:
    datasets = json.load(f)

def datasetsEn():
    prompt_parts = ["\nHere are some samples of photo metadata input and the output descriptions that should be followed in writing captions:"]
    for i, item in enumerate(datasets, start=1):
        inputs = "; ".join(item["input"]) +";"  # jadikan satu baris
        output = item["output"]
        prompt_parts.append(f"{i}. Input: {inputs}  Output: {output} |")
    return " ".join(prompt_parts)

def datasetsId():
    prompt_parts = ["\nBerikut ini beberapa contoh input metadata dari foto dan output caption yang harus diikuti dalam menulis caption foto:"]
    for i, item in enumerate(datasets, start=1):
        inputs = "; ".join(item["input"]) +";"  # jadikan satu baris
        output = item["output"]
        prompt_parts.append(f"{i}. Input: {inputs}  Output: {output} |")
    return " ".join(prompt_parts)