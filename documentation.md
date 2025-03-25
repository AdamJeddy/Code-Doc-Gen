# Code-Doc-Gen Documentation

## Overview

Code-Doc-Gen is a tool designed to automatically generate and update documentation for code changes in a repository. It leverages LangChain and OpenAI's GPT-4o to create comprehensive documentation by integrating with Git to detect code changes, extract repository overviews, and update documentation files. The tool is adaptable to any project and maintains a record of updates by embedding a commit marker in the generated documentation.

## Features

- **Automatic Documentation Generation**: Detects new commits and changes using Git logs and diffs, and generates or updates documentation accordingly.
- **LangChain Integration**: Utilizes LangChain to interface with GPT-4o for generating markdown documentation based on dynamic prompts.
- **Git Integration**: Uses Git commands to retrieve commit logs, diffs, and to commit documentation updates.
- **Repository Overview**: Generates an overview of up to 20 top-level files, including snippets for text files.
- **Extensibility**: Modular design allows for easy extension or customization to suit different project needs.

## File Structure

- **.gitignore**: Specifies files and directories to be ignored by Git, such as `.env`.
- **README.md**: Provides an overview of the project, setup instructions, and usage guidelines.
- **agent_version_doc_gen.py**: Contains the main logic for detecting changes, generating documentation, and committing updates.
- **doc_gen.py**: Handles the generation and updating of documentation using GPT-4o.
- **file_operations.py**: Provides basic file read and write operations.
- **langchain_github_documenter.ipynb**: A Jupyter notebook for testing and R&D of the code sections.
- **main.py**: A simple script that prints greetings to the console.
- **math_operations.py**: Implements basic math operations such as addition, subtraction, multiplication, and division.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **string_operations.py**: Implements basic string operations like concatenation and case conversion.

## Key Modules and Functions

### agent_version_doc_gen.py

- **update_sections**: Updates specific sections of the documentation based on detected changes.
- **get_last_documented_commit**: Extracts the last documented commit hash from the documentation file.
- **get_new_commits**: Returns a list of commit messages and hashes since the provided commit.
- **get_diff_since_commit**: Returns the diff of changes since the provided commit.
- **get_structured_git_diff**: Parses git diff into structured categories: added, modified, deleted files.
- **get_repo_overview**: Provides an overview of the repository structure and contents.
- **run_agent**: Initializes and runs the agent to generate or update documentation.

### doc_gen.py

- **get_current_commit_hash**: Retrieves the current HEAD commit hash.
- **get_structured_diff**: Gets structured diff since the last documented commit.
- **generate_documentation_content**: Generates documentation using GPT-4o.
- **update_documentation_file**: Updates the documentation file with new content and a commit marker.
- **commit_to_documentation_branch**: Handles git operations for committing to the documentation branch.
- **main_flow**: Main function to check for existing documentation, generate new content, and commit updates.

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

   Create a `.env` file in the root directory and add your OpenAI API key:

   ```env
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=<endpoint>
   LANGSMITH_API_KEY=<key>
   LANGSMITH_PROJECT=<project name>
   OPENAI_API_KEY=<key>
   ```

4. **Generate or Update Documentation**

   Run the documentation generation script:

   ```bash
   python documentation_generator.py
   ```

   The tool will check for existing documentation and update it based on new commits and changes.

## Dependencies

- **langchain==0.3.21**
- **langchain_openai==0.3.9**
- **python-dotenv==1.0.1**

Ensure all dependencies are installed by running `pip install -r requirements.txt`.

## Troubleshooting

- **Git Issues**: Ensure Git is installed and the repository is properly initialized.
- **Environment Variables**: Verify that your `.env` file contains a valid OpenAI API key.
- **Dependencies**: Confirm that all dependencies are installed by checking `requirements.txt`.
- **Logging**: Review the logs output to the console for error messages during Git operations or documentation generation.

Last Documented Commit: 729ec986a9b32756376e7cb0beb62d5c05e1dd44