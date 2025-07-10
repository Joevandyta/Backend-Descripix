from groq import Groq
import base64
import os
import json
from dotenv import load_dotenv
from .llama_prompt import dataset_to_prompt
# Load API key dari file .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY tidak ditemukan! Pastikan file .env sudah diatur dengan benar.")


# Fungsi untuk encode gambar ke base64
def encode_image(image_url):
    image = image_url.read()
    return base64.b64encode(image).decode('utf-8')

# Inisialisasi client Groq
client = Groq(api_key=groq_api_key)

# Fungsi untuk menghasilkan caption dari gambar + metadata
def getCaption(image_url, metadata):
    instructions = "You are an image captioning bot designed to generate descriptive captions based on the provided image. Include these instructions carefully:"
    prompt_parts = dataset_to_prompt()

    if metadata and any(value.strip() for value in metadata.values()):
        metadata_str =  "; ".join(f"{key.capitalize().replace('_', ' ')}: {value}" for key, value in metadata.items())

        finalMetadata = "Incorporate the following metadata into the caption to form a complete and coherent sentence:" + f"\n{metadata_str}"

        final_instructions = f"{instructions} {finalMetadata} {prompt_parts}"

    else:

        final_instructions = f"{instructions} {prompt_parts}"
    

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
    