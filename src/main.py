from exam_processor import ExamProcessor
from GPT_grader import PaperGrader
from GPT_vision_extractor import ChatGPTVisionExtractor
from image_extractor import ImageExtractor
from student_metadata import StudentMetadataLoader
import os


def main(pdf_directory: str, config_path: str, correct_answers_path: str, output_path: str, api_key: str, output_format: str = "csv"):
    """
    Run the full exam processing pipeline for multiple PDFs.
    """
    # Initialize classes
    exam_processor = ExamProcessor(correct_answers_path, output_path, output_format)
    vision_extractor = ChatGPTVisionExtractor(api_key)
    grader = PaperGrader(api_key)

    # Process each PDF in the directory
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)

            # Step 1: Extract images from PDF
            image_extractor = ImageExtractor(pdf_path, config_path)
            extracted_data = image_extractor.process(dpi=1200)

            # Step 2: Extract text from images using ChatGPT Vision
            student_metadata = {}
            student_answers = {}

            for page_num, data in extracted_data.items():
                # Extract name and ID
                if data["name"]:
                    name = vision_extractor.analyze_image(data["name"][0])
                    student_metadata["name"] = name.strip()
                if data["id"]:
                    student_id = vision_extractor.analyze_image(data["id"][0])
                    student_metadata["id"] = student_id.strip()

                # Extract answers
                student_answers[page_num] = []
                for base64_image in data["answers"]:
                    text = vision_extractor.analyze_image(base64_image)
                    student_answers[page_num].append(text)

            # Step 3: Grade the answers
            results = []
            for page_num, answers in student_answers.items():
                for i, student_answer in enumerate(answers, start=1):
                    question_id = f"Page {page_num}, Question {i}"
                    correct_answer = exam_processor.correct_answers.get(question_id, "")
                    if not correct_answer:
                        print(f"Warning: No correct answer found for {question_id}")
                        continue

                    grading_result = grader.grade_answer(student_answer, correct_answer)
                    results.append({
                        "Student Name": student_metadata.get("name", "Unknown"),
                        "Student ID": student_metadata.get("id", "Unknown"),
                        "Question ID": question_id,
                        "Student Answer": student_answer,
                        "Correct Answer": correct_answer,
                        "Grading Result": grading_result
                    })

            # Step 4: Append results to output file
            exam_processor.save_results(results)

if __name__ == "__main__":
    # Define paths and API key
    pdf_directory = "exam_reports"
    config_path = "direction_files/config_file.json"
    correct_answers_path = "direction_files/correct_answers.json"
    metadata_path = "student_metadata.csv"
    output_path = "grading_results.csv"  # or "grading_results.json"
    api_key = ""  # Replace with your actual API key

    # Run the pipeline
    main(
    pdf_directory=pdf_directory,
    config_path=config_path,
    correct_answers_path=correct_answers_path,
    output_path=output_path,
    api_key=api_key,
    output_format="csv"
)