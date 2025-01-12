import os
import json
from typing import List
from dataclasses import dataclass
from pdf2image import convert_from_path
from llamaapi import LlamaAPI


@dataclass
class ProcessingConfig:
    pdf_path: str
    output_dir: str
    output_text_file: str
    dpi: int = 300


class PDFProcessor:
    def __init__(self, api_token: str):
        """Initialize the PDFProcessor with LlamaAPI client."""
        self.llama = LlamaAPI(api_token)
        self.model = "llama3.1-70b"

    def _convert_pdf_to_images(self, config: ProcessingConfig) -> List[str]:
        """Convert PDF pages to images and save them to output directory."""
        if not os.path.exists(config.output_dir):
            os.makedirs(config.output_dir)

        images = convert_from_path(config.pdf_path, dpi=config.dpi)
        image_paths = []

        for i, image in enumerate(images):
            image_path = os.path.join(config.output_dir, f"page_{i + 1}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)

        return image_paths

    def _process_image(self, image_path: str) -> str:
        """Process a single image through the LlamaAPI."""
        try:
            # Open the image file and pass it in the request
            with open(image_path, "rb") as image_file:
                # Prepare the API request
                api_request = {
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": "Extract text from this image."}
                    ],
                    "stream": False,
                }

                # Pass the file as part of the API call
                files = {"file": ("image.png", image_file, "image/png")}
                response = self.llama.run(api_request, files=files)
                result = response.json()

                # Extract text from the response
                return result.get("text", "")

        except Exception as e:
            raise Exception(f"Error processing image {image_path}: {str(e)}")

    def process_pdf(self, config: ProcessingConfig) -> None:
        """Process the entire PDF and save extracted text."""
        try:
            print("Converting PDF to images...")
            image_paths = self._convert_pdf_to_images(config)
            print(f"Converted {len(image_paths)} pages into images.")

            all_text = []
            for idx, image_path in enumerate(image_paths):
                print(f"Processing page {idx + 1}...")
                extracted_text = self._process_image(image_path)
                all_text.append(f"# Page {idx + 1}\n{extracted_text}\n")

            print("Saving extracted text to Markdown file...")
            with open(config.output_text_file, "w", encoding="utf-8") as text_file:
                text_file.writelines(all_text)

            print(
                f"Text extraction complete. Output saved to {config.output_text_file}"
            )

        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")


def read_api_key(file_path: str) -> str:
    """Read the API key from an external file."""
    try:
        with open(file_path, "r", encoding="utf-8") as key_file:
            return key_file.read().strip()
    except FileNotFoundError:
        raise Exception(f"API key file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading API key file: {str(e)}")


def main():
    # Define the path to the API key file
    api_key_file = "api_key.txt"

    # Read the API key from the file
    api_token = read_api_key(api_key_file)

    # Define processing configuration
    config = ProcessingConfig(
        pdf_path="input.pdf",
        output_dir="output_images",
        output_text_file="output_text.md",
        dpi=300,
    )

    try:
        # Initialize the PDFProcessor
        processor = PDFProcessor(api_token)

        # Process the PDF
        processor.process_pdf(config)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
