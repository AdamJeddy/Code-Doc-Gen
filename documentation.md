# Code-Doc-Gen Project Documentation

# Code-Doc-Gen Project Documentation

## Overview

The Code-Doc-Gen project is designed to automate the generation and updating of documentation for code changes within a repository. It leverages LangChain and OpenAI's GPT-4o to dynamically create markdown documentation based on the current state of the codebase. The tool integrates with Git to detect changes, generate a repository overview, and update documentation files accordingly. This project is particularly useful for maintaining up-to-date documentation in a rapidly evolving codebase.

## Features

- **Automated Documentation Generation**: Automatically generates comprehensive documentation for the entire repository or updates existing documentation based on recent changes.
- **Git Integration**: Utilizes Git commands to track changes, retrieve commit logs, and manage documentation updates on a dedicated branch.
- **LangChain Integration**: Interfaces with GPT-4o to generate markdown documentation using dynamic prompts.
- **Commit Tracking**: Embeds a commit marker in the documentation to track the last documented commit.
- **Extensibility**: Designed to be adaptable and extendable for various project needs.

## File Structure

- **.gitignore**: Specifies files and directories to be ignored by Git, such as `.env`.
- **README.md**: Provides an overview of the project, setup instructions, and usage guidelines.
- **agent_version_doc_gen.py**: Contains the logic for detecting changes, generating documentation, and committing updates using LangChain and Git.
- **doc_gen.py**: Similar to `agent_version_doc_gen.py`, it handles documentation generation and updates, focusing on structured diffs and content updates.
- **file_operations.py**: Provides basic file read and write operations.
- **langchain_github_documenter.ipynb**: A Jupyter notebook for research and development, testing various sections of the code.
- **main.py**: A simple script that prints greetings to the console.
- **math_operations.py**: Implements basic mathematical operations such as addition, subtraction, multiplication, and division.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **string_operations.py**: Implements basic string operations like concatenation and case conversion.

## Key Modules and Functions

### agent_version_doc_gen.py

- **update_sections**: Updates specific sections of the documentation based on detected changes.
- **get_last_documented_commit**: Extracts the last documented commit hash from the documentation file.
- **get_new_commits**: Returns a list of commit messages and hashes since the last documented commit.
- **get_diff_since_commit**: Returns the diff of changes since the last documented commit.
- **get_structured_git_diff**: Parses git diff into structured categories: added, modified, deleted files.
- **get_repo_overview**: Provides an overview of the repository structure, including file snippets.
- **run_agent**: Initializes and runs the LangChain agent to generate or update documentation.

### doc_gen.py

- **get_current_commit_hash**: Retrieves the current HEAD commit hash.
- **get_structured_diff**: Gets structured diff since the last documented commit.
- **generate_documentation_content**: Generates documentation using GPT-4o.
- **update_documentation_file**: Updates the documentation file with new content and commit markers.
- **commit_to_documentation_branch**: Handles git operations for committing documentation updates.

### file_operations.py

- **read_file**: Reads the content of a specified file.
- **write_file**: Writes content to a specified file.

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

1. **Generate or Update Documentation**:
   ```bash
   python documentation_generator.py
   ```

2. **View the Documentation**:
   Open the `documentation.md` file to review the generated documentation.

## Dependencies

- **langchain==0.3.21**
- **langchain_openai==0.3.9**
- **python-dotenv==1.0.1**

Ensure all dependencies are installed by running:
```bash
pip install -r requirements.txt
```

## Troubleshooting

- **Git Issues**: Ensure Git is installed and the repository is properly initialized.
- **Environment Variables**: Verify that your `.env` file contains a valid OpenAI API key.
- **Dependencies**: Confirm that all dependencies are installed by checking `requirements.txt`.
- **Logging**: Review the logs output to the console for error messages during Git operations or documentation generation.
### Usage Examples
[Preserved content]

### Contributing
[Preserved content]

### License
[Preserved content]

### Contact
[Preserved content]

Last Documented Commit: add2c391a882fd3d6082c5b4751f46e7ea6b6cb9