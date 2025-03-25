# Code-Doc-Gen Documentation

## Overview

Code-Doc-Gen is a tool designed to automatically generate and update documentation for code changes in a repository. It leverages LangChain and OpenAI's GPT-4o to create comprehensive documentation by integrating with Git to detect code changes, extract a repository overview, and update documentation accordingly. The tool is adaptable to any project and maintains a record of updates by embedding a commit marker in the generated documentation.

## Features

- **Automatic Documentation Generation**: Generates documentation based on the repository's structure and code changes.
- **Git Integration**: Utilizes Git commands to track changes and manage documentation updates.
- **LangChain Integration**: Interfaces with GPT-4o to generate markdown documentation using dynamic prompts.
- **Commit Tracking**: Embeds a commit marker in the documentation to track the last documented commit.
- **Extensibility**: Designed to be easily extendable for different project needs.

## File Structure

- **.gitignore**: Specifies files and directories to be ignored by Git, such as `.env`.
- **README.md**: Provides an overview of the project, setup instructions, and usage guidelines.
- **agent_version_doc_gen.py**: Contains the logic for detecting code changes, generating documentation, and committing updates.
- **doc_gen.py**: Handles the main flow of documentation generation and updates.
- **file_operations.py**: Provides basic file read and write operations.
- **langchain_github_documenter.ipynb**: A Jupyter notebook for testing and R&D of code sections.
- **main.py**: A simple script that prints greetings to the console.
- **math_operations.py**: Implements basic math operations such as addition, subtraction, multiplication, and division.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **string_operations.py**: Implements basic string operations like concatenation and case conversion.

## Key Modules and Functions

### agent_version_doc_gen.py

- **update_sections**: Updates specific sections of the documentation based on detected changes.
- **get_last_documented_commit**: Extracts the last documented commit hash from the documentation file.
- **get_new_commits**: Returns a list of commit messages and hashes since the last documented commit.
- **get_diff_since_commit**: Returns the diff of changes since the last documented commit.
- **get_structured_git_diff**: Parses git diff into structured categories: added, modified, deleted files.
- **get_repo_overview**: Provides an overview of the repository structure and content.
- **run_agent**: Initializes and invokes the agent to generate or update documentation.

### doc_gen.py

- **get_current_commit_hash**: Retrieves the current HEAD commit hash.
- **get_structured_diff**: Gets structured diff since the last documented commit, excluding documentation.md.
- **generate_documentation_content**: Generates documentation using GPT-4o.
- **update_documentation_file**: Updates the documentation file with new content and a commit marker.
- **commit_to_documentation_branch**: Handles git operations for the documentation branch.
- **main_flow**: Main function to handle the documentation generation and update process.

### file_operations.py

- **read_file**: Reads the content of a given file.
- **write_file**: Writes content to a file, creating or updating it.

### math_operations.py

- **add**: Returns the sum of two numbers.
- **subtract**: Returns the difference between two numbers.
- **multiply**: Returns the product of two numbers.
- **divide**: Returns the quotient of two numbers, handling division by zero.

### string_operations.py

- **concatenate**: Concatenates two strings.
- **to_uppercase**: Converts a string to uppercase.
- **to_lowercase**: Converts a string to lowercase.

## Usage Examples

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables by creating a `.env` file in the root directory and adding your OpenAI API key.

### Running the Tool

To generate or update documentation, run the following command:
```bash
python documentation_generator.py
```

This will check for existing documentation, detect new commits and changes, and update the documentation accordingly.

## Dependencies

- **langchain**: Version 0.3.21
- **langchain_openai**: Version 0.3.9
- **python-dotenv**: Version 1.0.1

Ensure all dependencies are installed by checking the `requirements.txt` file.

Last Documented Commit: b52eb2a2edae5e21017c9d7d6a3f52436b769ef9