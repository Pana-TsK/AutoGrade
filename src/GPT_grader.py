from openai import OpenAI
import logging

class PaperGrader:
    """
    Grades student answers using the ChatGPT API.
    """
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize the PaperGrader with the OpenAI API key and model.
        
        :param api_key: OpenAI API key.
        :param model: Model to use for grading (default is "gpt-4").
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
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

    def grade_answer(self, student_answer: str, correct_answer: str) -> str:
        """
        Grade a student's answer against the correct answer.
        
        :param student_answer: The student's answer.
        :param correct_answer: The correct answer.
        :return: Grading result with score and feedback.
        """
        prompt = (
            "You are an experienced exam grader. "
            "Please grade the following answer by comparing it to the correct answer. "
            "Provide a numerical score (0-100) and detailed feedback explaining your grading decision.\n\n"
            "Student Answer:\n"
            f"{student_answer}\n\n"
            "Correct Answer:\n"
            f"{correct_answer}\n\n"
            "Grade and feedback:"
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a strict and experienced exam grader."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error in ChatGPT grading call: {e}")
            return ""

if __name__ == "__main__":
    # Replace with your actual API key. I removed mine, of course :)
    api_key = ""
    
    # Sample data: student's answer (extracted text) and correct answer.
    student_answer = (
        "The process of photosynthesis involves chlorophyll, light absorption, "
        "and conversion of CO2 and water into sugars and oxygen."
    )
    correct_answer = (
        "Photosynthesis is the process by which green plants and some other organisms "
        "use sunlight to synthesize foods with the help of chlorophyll, converting carbon dioxide and water into glucose and oxygen."
    )
    
    # Instantiate the PaperGrader class.
    grader = PaperGrader(api_key)
    
    # Grade the answer.
    result = grader.grade_answer(student_answer, correct_answer)
    print("Grading Result:")
    print(result)