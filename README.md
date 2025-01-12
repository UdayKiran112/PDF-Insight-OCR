# PDF Insight OCR

A powerful Python-based OCR tool for extracting text from PDF documents using optical character recognition. The tool automatically converts PDF pages to high-quality images, processes them using the Llama OCR API, and generates clean, formatted Markdown output.

## Features

- Efficient PDF to image conversion with configurable quality settings
- Advanced OCR processing using the Llama OCR API
- Structured Markdown output with proper page separation
- Comprehensive error handling and logging
- Type-safe implementation with Python type hints
- Batch processing support for multi-page documents
- Configurable output paths and API settings

## Installation

### Prerequisites

Before installing PDF Insight OCR, ensure you have the following prerequisites:

1. Python 3.7 or higher
2. poppler-utils (required for PDF conversion)

#### Installing poppler-utils

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download the binary from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/) and add it to your system PATH.

### Setting Up the Project

1. Clone the repository:
```bash
git clone https://github.com/your-username/pdf-insight-ocr.git
cd pdf-insight-ocr
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Update the configuration in `pdf_insight_ocr.py`:
```python
# Configuration
PDF_PATH = "your_document.pdf"
OUTPUT_DIR = "output_images"
OUTPUT_TEXT_FILE = "output_text.md"
LLAMA_API_URL = "https://api.llama-ocr.com/v1/process"
API_KEY = "your-api-key"
```

2. Run the script:
```bash
python pdf_insight_ocr.py
```

### Advanced Usage

You can also use the `PDFInsightOCR` class in your own Python scripts:

```python
from pdf_insight_ocr import PDFInsightOCR

# Initialize the processor
processor = PDFInsightOCR(
    api_key="your-api-key",
    api_url="https://api.llama-ocr.com/v1/process",
    output_dir="custom_output_dir",
    output_text_file="custom_output.md"
)

# Process a PDF
processor.process_pdf("path/to/your/document.pdf")
```

## API Reference

### PDFInsightOCR Class

#### Constructor

```python
def __init__(
    self,
    api_key: str,
    api_url: str,
    output_dir: str = "output_images",
    output_text_file: str = "output_text.md"
)
```

Parameters:
- `api_key`: Your Llama OCR API key
- `api_url`: The Llama OCR API endpoint
- `output_dir`: Directory to save converted images (default: "output_images")
- `output_text_file`: Path for the output Markdown file (default: "output_text.md")

#### Methods

**process_pdf(pdf_path: str)**
- Processes a PDF file end-to-end
- Parameters:
  - `pdf_path`: Path to the input PDF file

**convert_pdf_to_images(pdf_path: str) -> List[Path]**
- Converts PDF pages to images
- Returns: List of paths to converted images

**process_image(image_path: Path) -> Optional[str]**
- Processes a single image using the OCR API
- Returns: Extracted text or None if processing failed

**save_to_markdown(texts: List[Optional[str]])**
- Saves extracted texts to a Markdown file
- Parameters:
  - `texts`: List of extracted texts for each page

## Output Format

The tool generates a Markdown file with the following structure:

```markdown
# Page 1

[Extracted text from page 1]

# Page 2

[Extracted text from page 2]

...
```

If text extraction fails for a page, it will be noted in the output:

```markdown
# Page 3

*Error: Could not extract text from this page.*
```

## Error Handling

The tool includes comprehensive error handling:

- PDF conversion errors are caught and logged
- API communication errors are handled gracefully
- File I/O errors are properly managed
- All errors are logged with detailed messages

## Logging

Logging is configured by default with:
- INFO level messages for successful operations
- ERROR level messages for failures
- Timestamps and log levels in output
- Console output for immediate feedback

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pdf2image](https://github.com/Belval/pdf2image) for PDF conversion capabilities
- [Llama OCR](https://llama-ocr.com) for OCR processing
- All contributors and users of PDF Insight OCR

---

Developed with ❤️ for the open-source community.