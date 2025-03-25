# Code-Doc-Gen Project Documentation

# Code-Doc-Gen Project Documentation

## Overview

The Code-Doc-Gen project is designed to automate the generation and updating of documentation for code changes in a repository. It leverages LangChain and OpenAI's GPT-4o to dynamically create markdown documentation based on the current state of the codebase. The tool integrates with Git to detect changes, generate a repository overview, and update documentation files accordingly. This project is particularly useful for maintaining up-to-date documentation in rapidly evolving codebases.

## Features

- **Automated Documentation Generation**: Automatically generates comprehensive documentation for the entire repository or updates existing documentation based on recent changes.
- **Git Integration**: Utilizes Git commands to track changes, retrieve commit logs, and manage documentation updates on a dedicated branch.
- **LangChain Integration**: Interfaces with GPT-4o to generate markdown documentation using dynamic prompts.
- **Commit Tracking**: Embeds a commit marker in the documentation to track the last documented commit.
- **Extensibility**: Modular design allows for easy customization and integration with additional systems.

## File Structure

- **.gitignore**: Specifies files and directories to be ignored by Git, such as `.env`.
- **README.md**: Provides an overview of the project, setup instructions, and usage guidelines.
- **agent_version_doc_gen.py**: Contains the main logic for detecting code changes, generating documentation, and committing updates to a Git branch.
- **doc_gen.py**: Similar to `agent_version_doc_gen.py`, it handles documentation generation and updates using a different approach.
- **file_operations.py**: Provides utility functions for reading and writing files.
- **langchain_github_documenter.ipynb**: A Jupyter notebook for experimenting with and testing different sections of the code.
- **main.py**: A simple script that prints greetings to the console.
- **math_operations.py**: Implements basic mathematical operations such as addition, subtraction, multiplication, and division.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **string_operations.py**: Implements basic string operations such as concatenation and case conversion.

## Key Modules and Functions

### agent_version_doc_gen.py

- **update_sections**: Updates specific sections of the documentation based on detected changes.
- **get_last_documented_commit**: Extracts the last documented commit hash from the documentation file.
- **get_new_commits**: Returns a list of commit messages and hashes since the last documented commit.
- **get_diff_since_commit**: Returns the diff of changes since the last documented commit.
- **get_structured_git_diff**: Parses git diff into structured categories: added, modified, deleted files.
- **get_repo_overview**: Provides an overview of the repository structure, including snippets of text files.
- **run_agent**: Initializes and invokes the agent to generate or update documentation based on the current state of the repository.

### doc_gen.py

- **get_current_commit_hash**: Retrieves the current HEAD commit hash.
- **get_structured_diff**: Gets structured diff since the last documented commit.
- **generate_documentation_content**: Generates documentation using GPT-4o.
- **update_documentation_file**: Updates the documentation file with new content and commit markers.
- **commit_to_documentation_branch**: Handles git operations for committing documentation updates to a dedicated branch.
- **main_flow**: Orchestrates the process of generating or updating documentation based on the repository's state.

### file_operations.py

- **read_file**: Reads the content of a specified file.
- **write_file**: Writes content to a specified file.

### math_operations.py

- **add**: Returns the sum of two numbers.
- **subtract**: Returns the difference between two numbers.
- **multiply**: Returns the product of two numbers.
- **divide**: Returns the quotient of two numbers, raising an error if the divisor is zero.

### string_operations.py

- **concatenate**: Concatenates two strings.
- **to_uppercase**: Converts a string to uppercase.
- **to_lowercase**: Converts a string to lowercase.

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

    Create a `.env` file in the root directory and add your OpenAI API key:

    ```env
    LANGSMITH_TRACING=true
    LANGSMITH_ENDPOINT=<endpoint>
    LANGSMITH_API_KEY=<key>
    LANGSMITH_PROJECT=<project name>
    OPENAI_API_KEY=<key>
    ```

### Running the Documentation Generator

1. **Generate or Update Documentation**

    Run the documentation generation script:

    ```bash
    python documentation_generator.py
    ```

    The tool will check for existing documentation and update it based on recent changes, or generate new documentation if none exists.

2. **View the Documentation**

    Open the generated `documentation.md` file to review the documentation. The final line of the file includes a commit marker in the format:

    ```
    Last Documented Commit: <commit_hash>
    ```

## Dependencies

- **langchain==0.3.21**
- **langchain_openai==0.3.9**
- **python-dotenv==1.0.1**

Ensure all dependencies are installed by running `pip install -r requirements.txt`.

Last Documented Commit: 469eefbdb25edd1bd7a4776d20f72ba7e528526d