# Project Documentation

## Overview

The **Code-Doc-Gen** project is designed to automate the generation and updating of documentation for code changes in a repository. It leverages LangChain and OpenAI's GPT-4o to dynamically create and update documentation based on the repository's structure and recent changes. The tool integrates with Git to detect code changes, extract a repository overview, and update documentation accordingly. This project is particularly useful for maintaining up-to-date documentation in rapidly evolving codebases.

## Features

- **Automated Documentation Generation**: Automatically generates comprehensive documentation for the repository, including an overview, file structure, and key features.
- **Dynamic Updates**: Detects new commits and updates the documentation to reflect recent changes.
- **Git Integration**: Utilizes Git commands to track changes and commit documentation updates to a dedicated branch.
- **LangChain Integration**: Uses LangChain to interface with GPT-4o for generating markdown documentation based on dynamic prompts.
- **Extensibility**: The modular design allows for easy customization and extension to suit different project needs.

## File Structure

```
.
├── .env
├── .gitignore
├── README.md
├── documentation_generator.py
├── file_operations.py
├── langchain_github_documenter.ipynb
├── main.py
├── math_operations.py
├── requirements.txt
└── string_operations.py
```

### File Descriptions

- **`.env`**: Contains environment variables such as API keys and project-specific configurations.
- **`.gitignore`**: Specifies files and directories to be ignored by Git, including the `.env` file.
- **`README.md`**: Provides an overview of the project, setup instructions, and usage guidelines.
- **`documentation_generator.py`**: Core script responsible for generating and updating documentation. It includes functions for Git operations, file reading/writing, and interacting with the LangChain API.
- **`file_operations.py`**: Contains utility functions for reading and writing files.
- **`langchain_github_documenter.ipynb`**: Jupyter notebook used for research and development of the documentation generation process.
- **`main.py`**: A simple script that prints greetings to the console.
- **`math_operations.py`**: Implements basic mathematical operations such as addition, subtraction, multiplication, and division.
- **`requirements.txt`**: Lists the Python dependencies required for the project.
- **`string_operations.py`**: Provides functions for string manipulation, including concatenation and case conversion.

## Key Modules and Functions

### `documentation_generator.py`

- **`update_sections(existing_content, changes)`**: Updates specific sections of the documentation based on detected changes.
- **`get_last_documented_commit(file_path)`**: Extracts the last documented commit hash from the documentation file.
- **`get_new_commits(since_commit)`**: Returns a list of commit messages and hashes since the provided commit.
- **`get_diff_since_commit(since_commit)`**: Returns the diff of changes since the provided commit.
- **`get_structured_git_diff(since_commit)`**: Parses git diff into structured categories: added, modified, deleted files.
- **`get_repo_overview()`**: Provides an overview of the repository structure, including snippets of text files.
- **`run_agent()`**: Initializes and runs the LangChain agent to generate or update documentation based on the repository's state.

### `file_operations.py`

- **`read_file(file_path)`**: Reads the content of a given file.
- **`write_file(file_path, content)`**: Writes content to a file, creating or updating it.

### `math_operations.py`

- **`add(a, b)`**: Returns the sum of two numbers.
- **`subtract(a, b)`**: Returns the difference between two numbers.
- **`multiply(a, b)`**: Returns the product of two numbers.
- **`divide(a, b)`**: Returns the quotient of two numbers, raising an error if the divisor is zero.

### `string_operations.py`

- **`concatenate(str1, str2)`**: Concatenates two strings.
- **`to_uppercase(string)`**: Converts a string to uppercase.
- **`to_lowercase(string)`**: Converts a string to lowercase.

## Usage Examples

### Setup

1. **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a Virtual Environment and Install Dependencies**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Configure Environment Variables**

    Create a `.env` file in the root directory and add your OpenAI API key and other necessary configurations.

### Running the Documentation Generator

1. **Generate or Update Documentation**

    ```bash
    python documentation_generator.py
    ```

    This command will generate a new `documentation.md` file or update the existing one based on recent changes.

2. **View the Documentation**

    Open the `documentation.md` file to review the generated documentation. The file will include a commit marker indicating the last documented commit.

## Dependencies

- **LangChain**: `langchain==0.3.21`
- **LangChain OpenAI**: `langchain_openai==0.3.9`
- **Python Dotenv**: `python-dotenv==1.0.1`

Ensure all dependencies are installed by running `pip install -r requirements.txt`.

## Troubleshooting

- **Git Issues**: Ensure Git is installed and the repository is properly initialized.
- **Environment Variables**: Verify that your `.env` file contains valid API keys.
- **Dependencies**: Confirm that all dependencies are installed correctly.
- **Logging**: Review console logs for error messages during Git operations or documentation generation.

Last Documented Commit: 23ed53ccd4dc12e778ee1454b9dfda5879688fe7