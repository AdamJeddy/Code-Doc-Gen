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

## Recent Changes
### Overview

The project documentation has been updated to reflect recent changes made to the codebase. The primary modification involves the `math_operations.py` file. This update aims to provide a detailed summary of the changes made to this file, ensuring that the documentation remains accurate and useful for developers and users interacting with the project.

### Recent Changes

#### Modified Files

- **math_operations.py**
  - **Summary of Changes**: The `math_operations.py` file has undergone modifications. While the specific details of the changes are not provided, it is important to review the file to understand the updates. These changes could involve bug fixes, performance improvements, or the addition of new mathematical functions. Developers are encouraged to examine the commit history and code comments for a comprehensive understanding of the modifications.
  - **Impact on Project**: The changes in `math_operations.py` may affect any functionality that relies on mathematical operations provided by this module. It is crucial to test any dependent features to ensure compatibility and correctness following these updates.

No new files were added, and no files were deleted in this update. The focus remains on the modifications made to the existing `math_operations.py` file.

Last Documented Commit: 70e52269a51e5b8b82ebbae40f718c74601194e9