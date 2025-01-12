import os
import json
from pdf2image import convert_from_path
from llamaapi import LlamaAPI

# Replace with your actual Llama API token
LLAMA_API_TOKEN = "<your_api_token>"
LLAMA_API_URL = "https://api.llama.com/v1"  # Replace with actual API endpoint if different

# Initialize the Llama API
llama = LlamaAPI(LLAMA_API_TOKEN)

# Configuration
PDF_PATH = "input.pdf"  # Path to the input PDF file
OUTPUT_DIR = "output_images"  # Directory to store images
OUTPUT_TEXT_FILE = "output_text.md"  # Path to save the extracted text

# Function to convert PDF to images
def pdf_to_images(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    images = convert_from_path(pdf_path, dpi=300)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths

# Function to process an image with the Llama API
def process_image_with_llama(image_path):
    with open(image_path, "rb") as image_file:
        files = {"file": image_file}
        data = {
            "model": "llama3.1-70b",
            "messages": [{"role": "user", "content": "Extract text from the uploaded image."}],
            "functions": [],
            "stream": False
        }
        response = llama.run({"files": files, "data": data})
        return response.get("text", "")

# Main script
if __name__ == "__main__":
    print("Converting PDF to images...")
    try:
        image_paths = pdf_to_images(PDF_PATH, OUTPUT_DIR)
        print(f"Converted {len(image_paths)} pages into images.")

        all_text = []
        for idx, image_path in enumerate(image_paths):
            print(f"Processing page {idx + 1}...")
            extracted_text = process_image_with_llama(image_path)
            all_text.append(f"# Page {idx + 1}\n{extracted_text}\n")
        
        print("Saving extracted text to Markdown file...")
        with open(OUTPUT_TEXT_FILE, "w", encoding="utf-8") as text_file:
            text_file.writelines(all_text)
        
        print(f"Text extraction complete. Output saved to {OUTPUT_TEXT_FILE}.")
    except Exception as e:
        print(f"An error occurred: {e}")
