import base64
from openai import OpenAI
import logging

class ChatGPTVisionExtractor:
    """
    Extracts text from images using the ChatGPT Vision API.
    """
    def __init__(self, api_key: str):
        """
        Initialize the ChatGPTVisionExtractor with the OpenAI API key.
        
        :param api_key: OpenAI API key.
        """
        self.client = OpenAI(api_key=api_key)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Set up a logger for the class."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def base64_encode_image(self, image_path: str) -> str:
        """
        Encode an image file to Base64.
        
        :param image_path: Path to the image file.
        :return: Base64-encoded image string.
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_str = base64.b64encode(image_file.read()).decode("utf-8")
            self.logger.debug(f"Encoded image length: {len(encoded_str)}")
            return encoded_str
        except Exception as e:
            self.logger.error(f"Error encoding image: {e}")
            return ""

    def analyze_image(self, base64_image: str) -> str:
        """
        Analyze a Base64-encoded image using the ChatGPT Vision API.
        
        :param base64_image: Base64-encoded image string.
        :return: Extracted text from the image.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Please, turn the written text inside of the squares into typed text."},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high",
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"Error in ChatGPT Vision API call: {e}")
            return ""
    
if __name__ == "__main__":
    # Replace with your actual API key and image path.
    api_key = ""
    image_path = "test_images/ceci_nest_pas.png"
    
    # Instantiate the ChatGPTVisionExtractor class.
    vision_extractor = ChatGPTVisionExtractor(api_key)
    
    # Convert the image to Base64.
    base64_image = vision_extractor.base64_encode_image(image_path)
    
    # Send the image to ChatGPT Vision and print the result.
    result_text = vision_extractor.analyze_image(base64_image)
    print("Extracted Text from Image:")
    print(result_text)
