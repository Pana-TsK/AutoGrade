# AutoGrade

AutoGrade is a tool designed to automate the grading process for programming assignments. It supports multiple programming languages and provides detailed feedback to students.

## Features

- Automated grading based on file containing solutions
- Detailed feedback for students
- Easy integration with existing systems
- Customizable grading criteria

## Installation

To install AutoGrade, clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/AutoGrade.git
cd AutoGrade
pip install -r requirements.txt
```

## Usage

1. Create the exam sheet with clearly defined answer squares/rectangles (in PDF format).
2. Find the coordinates of each box on the PDF file.
3. Rewrite the necessary direction files:
    - `config_file.json` defines the name and ID squares, in addition to each question square.
    - For each question square, provide the GPT prompts for points counting in the `correct_answers.json` file.
4. Run the script through the main file. Don't forget to provide your OpenAI API key!
5. Validate the exam results.

### Command Line Options

CLI is not yet supported with the current build, but may come in the near future.

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or feedback, please contact us at panagiotis.tsampanis47@gmail.com.

## Acknowledgements

We would like to thank all the contributors and the open-source community for their support.

## Roadmap

- Create CLI
- Add more robust image detection
- Create a GUI for ease of access
- Simplify the identification of questions

## Support

If you encounter any issues or have any questions, please open an issue on GitHub or contact us at panagiotis.tsampanis47@gmail.com.
