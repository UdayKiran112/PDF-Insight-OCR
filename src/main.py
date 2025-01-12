import os
from pdf2image import convert_from_path
import requests

# Configuration
PDF_PATH = "your_document.pdf"  # Path to the input PDF
OUTPUT_DIR = "output_images"    # Directory to save images
OUTPUT_TEXT_FILE = "output_text.md"  # Output markdown file
LLAMA_API_URL = "https://api.llamaocr.com/ocr"  # Replace with Llama OCR API URL
API_KEY = "your_api_key"  # Your Llama OCR API key

# Step 1: Convert PDF to images
def pdf_to_images(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths

# Step 2: Perform OCR using Llama API
def perform_ocr(image_path, api_url, api_key):
    with open(image_path, "rb") as image_file:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {api_key}"},
            files={"file": image_file}
        )
        response.raise_for_status()
        return response.json()["markdown_text"]  # Adjust key based on Llama API's response

# Step 3: Process all images and save text to a file
def process_images_and_export_text(image_paths, output_text_file, api_url, api_key):
    all_text = []
    for image_path in image_paths:
        print(f"Processing: {image_path}")
        try:
            markdown_text = perform_ocr(image_path, api_url, api_key)
            all_text.append(markdown_text)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))
    print(f"Text exported to: {output_text_file}")

# Main Execution
if __name__ == "__main__":
    # Step 1: Convert PDF to images
    print("Converting PDF to images...")
    image_paths = pdf_to_images(PDF_PATH, OUTPUT_DIR)
    
    # Step 2 and 3: Perform OCR and export text
    print("Performing OCR on images...")
    process_images_and_export_text(image_paths, OUTPUT_TEXT_FILE, LLAMA_API_URL, API_KEY)
