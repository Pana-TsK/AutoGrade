import fitz  # PyMuPDF
import json
import base64
from io import BytesIO
from PIL import Image
import logging

class ImageExtractor:
    """
    Extracts images from predefined regions in a PDF using PyMuPDF.
    """
    def __init__(self, pdf_filepath: str, config_filepath: str):
        """
        Initialize the ImageExtractor with the PDF file and config file paths.
        
        :param pdf_filepath: Path to the PDF file.
        :param config_filepath: Path to the JSON config file specifying box coordinates.
        """
        self.pdf_filepath = pdf_filepath
        self.config_filepath = config_filepath
        self.logger = self._setup_logger()
        self.pdf = self._load_pdf()
        self.config = self._load_config()

    def _setup_logger(self):
        """Set up a logger for the class."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _load_pdf(self):
        """Load the PDF file."""
        try:
            return fitz.open(self.pdf_filepath)
        except Exception as e:
            self.logger.error(f"Error opening PDF: {e}")
            raise

    def _load_config(self):
        """Load the configuration file."""
        try:
            with open(self.config_filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading config file: {e}")
            raise

    def extract_image_from_boxes(self, page_num: int, boxes: list, dpi: int = 600) -> list:
        """
        Extract images from predefined boxes on a specific page.
        
        :param page_num: Page number to extract images from.
        :param boxes: List of box coordinates ([[x0, y0, x1, y1], ...]).
        :param dpi: Resolution for image extraction.
        :return: List of Base64-encoded images.
        """
        try:
            page = self.pdf.load_page(page_num)
            extracted_images = []
            for box in boxes:
                rect = fitz.Rect(box)
                matrix = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=matrix, clip=rect)
                img_bytes = pix.tobytes("png")
                base64_image = base64.b64encode(img_bytes).decode()
                extracted_images.append(base64_image)
            return extracted_images
        except Exception as e:
            self.logger.error(f"Error extracting images from page {page_num}: {e}")
            return []

    def process(self, dpi: int = 1200) -> dict[str, dict[str, list[str]]]:
        """
        Runs the full extraction pipeline using coordinates from the config.
        
        :param dpi: Resolution for image extraction.
        :return: dictionary mapping page numbers to extracted data (name, ID, answers).
        """
        all_extracted_data = {}

        for page_num, page_info in self.config.get("pages", {}).items():
            page_num = int(page_num)
            extracted_data = {"name": [], "id": [], "answers": []}

            for info in page_info:
                box_type = info.get("type", "answer")  # Default to "answer" if type is missing
                box = info["box"]
                images = self.extract_image_from_boxes(page_num, [box], dpi=dpi)

                if box_type == "name":
                    extracted_data["name"].extend(images)
                elif box_type == "id":
                    extracted_data["id"].extend(images)
                elif box_type == "answer":
                    extracted_data["answers"].extend(images)

            all_extracted_data[page_num] = extracted_data

        return all_extracted_data

    def show_image_from_base64(self, base64_str: str):
        """
        Display a Base64-encoded image using Pillow.
        
        :param base64_str: Base64-encoded image string.
        """
        try:
            img_data = base64.b64decode(base64_str)
            img = Image.open(BytesIO(img_data))
            img.show()
        except Exception as e:
            self.logger.error(f"Error displaying image: {e}")

# **Testing the Code**

if __name__ == "__main__":
    # Define paths for the PDF and config file
    pdf_path = "test_pdf_files/reports HPLC.pdf"
    config_path = "test_pdf_files/config_file.json"

    # Initialize the extractor with the paths
    extractor = ImageExtractor(pdf_path, config_path)

    # Run the extraction pipeline with higher resolution
    extracted_images = extractor.process(dpi=2000)
    
    # Show images
    for page_num, images in extracted_images.items():
        print(f"Page {page_num}:")
        for i, base64_image in enumerate(images, start=1):
            print(f"  Showing Answer Box {i}:")
            extractor.show_image_from_base64(base64_image)  # Display the image
