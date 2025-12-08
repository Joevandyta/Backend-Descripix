from groq import Groq
import base64
import os
import json
from dotenv import load_dotenv
from .llama_prompt import datasetsId, datasetsEn
# Load API key dari file .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not found!")

module_dir = os.path.dirname(__file__)
file_path_en = os.path.join(module_dir, "instruction_en.txt")
file_path_id = os.path.join(module_dir, "instruction_id.txt")

def read_instruction(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    
# Fungsi untuk encode gambar ke base64
def encode_image(image_url):
    image = image_url.read()
    return base64.b64encode(image).decode('utf-8')

# Inisialisasi client Groq
client = Groq(api_key=groq_api_key)

# Fungsi untuk menghasilkan caption dari gambar + metadata
def getCaption(image_url, metadata, language_code, style):
    print(f"Language Code: {language_code}")
    if language_code == 'id':
        instructions = read_instruction(file_path_id)

        
        # instructions += f"\n- Gunakan gaya bahasa {style}, dengan struktur kalimat yang sesuai konteks dan hindari penggunaan yang bertentangan dengan karakter gaya tersebut."
        if style == 'formal':
            instructions += (
                "\n- Gunakan gaya bahasa formal yang sopan, terstruktur, dan sesuai kaidah bahasa Indonesia baku."
                "\n- Hindari penggunaan kata tidak baku atau ekspresi informal."
            )
        elif style == 'poetical':
            instructions += (
                "\n- Gunakan gaya bahasa puitis dengan diksi yang indah dan imajinatif."
                "\n- Boleh menggunakan majas seperti personifikasi, metafora, atau perumpamaan untuk memperkaya makna."
            )
        elif style == 'casual':
            instructions += (
                "\n- Gunakan gaya bahasa santai, alami, dan mudah dipahami, seolah berbicara dengan teman."
                "\n- Hindari struktur kalimat yang terlalu kaku atau formal."
            )

        instructions_metadata = "\nMasukkan metadata berikut ke dalam caption untuk membentuk caption yang lengkap dan koheren:"
        prompt_parts = datasetsId()

    elif language_code == 'en':
        instructions = read_instruction(file_path_en)
        if style == 'formal':
            instructions += (
                "\n- Use a formal writing style that is polite, structured, and follows proper English grammar conventions."
                "\n- Avoid using slang, contractions, or overly casual expressions."
            )
        elif style == 'poetical':
            instructions += (
                "\n- Use a poetic writing style with beautiful and imaginative diction."
                "\n- You may use figurative language such as personification, metaphors, or similes to enrich meaning."
            )
        elif style == 'casual':
            instructions += (
                "\n- Use a casual and natural writing style that feels conversational and easy to understand."
                "\n- Avoid overly rigid or formal sentence structures."
            )

        instructions_metadata = "\nIncorporate the following metadata into the caption to form a complete and coherent sentence:"
        prompt_parts = datasetsEn()
        
    if metadata and any(value.strip() for value in metadata.values()):
        metadata_str =  "; ".join(f"{key.capitalize().replace('_', ' ')}: {value}" for key, value in metadata.items())

        finalMetadata = f"{instructions_metadata}\n{metadata_str}"

        final_instructions = f"{instructions} {finalMetadata} {prompt_parts}"
        # final_instructions = f"{instructions} {finalMetadata}"

    else:
        final_instructions = f"{instructions} {prompt_parts}"
    

    print("Final Instructions:", final_instructions)
    # Encode gambar ke base64
    base64_image = encode_image(image_url)
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": final_instructions
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ], 
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    result = completion.choices[0].message.content
    return result
    