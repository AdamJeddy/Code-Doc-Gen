# Code-Doc-Gen Project Documentation

## Overview

The Code-Doc-Gen project is designed to automate the generation and updating of documentation for code changes in a repository. It leverages LangChain and OpenAI's GPT-4o to create comprehensive documentation by integrating with Git to detect code changes, extract repository overviews, and update documentation files. The tool is adaptable to any project and maintains a record of updates by embedding a commit marker in the generated documentation.

## Features

- **Automated Documentation Generation:** Automatically generates documentation based on the repository's structure and code changes.
- **Git Integration:** Utilizes Git to track changes, retrieve commit logs, and manage documentation updates.
- **LangChain Integration:** Interfaces with GPT-4o to generate markdown documentation using dynamic prompts.
- **Commit Tracking:** Embeds a commit marker in the documentation to track the last documented commit.
- **Extensibility:** Designed to be easily extendable for different project needs or integration with additional systems.

## File Structure

The project consists of the following files:

- **`.gitignore`:** Specifies files and directories to be ignored by Git, such as `.env`.
- **`README.md`:** Provides an overview of the project, setup instructions, and usage guidelines.
- **`agent_version_doc_gen.py`:** Contains the core logic for detecting code changes, generating documentation, and committing updates.
- **`doc_gen.py`:** Handles the generation and updating of documentation using GPT-4o.
- **`file_operations.py`:** Provides utility functions for reading and writing files.
- **`langchain_github_documenter.ipynb`:** A Jupyter notebook for research and development of code sections.
- **`main.py`:** A simple script that prints greetings to the console.
- **`math_operations.py`:** Implements basic math operations such as addition, subtraction, multiplication, and division.
- **`requirements.txt`:** Lists the dependencies required for the project.
- **`string_operations.py`:** Implements basic string operations such as concatenation and case conversion.

## Key Modules and Functions

### `agent_version_doc_gen.py`

- **`update_sections(existing_content, changes)`:** Updates specific sections of the documentation based on detected changes.
- **`get_last_documented_commit(file_path)`:** Extracts the last documented commit hash from the documentation file.
- **`get_new_commits(since_commit)`:** Returns a list of commit messages and hashes since the provided commit.
- **`get_diff_since_commit(since_commit)`:** Returns the diff of changes since the provided commit.
- **`get_structured_git_diff(since_commit)`:** Parses git diff into structured categories: added, modified, deleted files.
- **`get_repo_overview()`:** Provides an overview of the repository structure and contents.
- **`run_agent()`:** Initializes and runs the agent to generate or update documentation.

### `doc_gen.py`

- **`get_current_commit_hash()`:** Retrieves the current HEAD commit hash.
- **`get_structured_diff(last_commit)`:** Gets structured diff since the last documented commit.
- **`generate_documentation_content(context)`:** Generates documentation using GPT-4o.
- **`update_documentation_file(new_content, current_content)`:** Updates the documentation file with new content and commit marker.
- **`commit_to_documentation_branch()`:** Handles git operations for committing documentation updates.

### `file_operations.py`

- **`read_file(file_path)`:** Reads the content of a given file.
- **`write_file(file_path, content)`:** Writes content to a file, creating or updating it.

### `math_operations.py`

- **`add(a, b)`:** Returns the sum of two numbers.
- **`subtract(a, b)`:** Returns the difference between two numbers.
- **`multiply(a, b)`:** Returns the product of two numbers.
- **`divide(a, b)`:** Returns the quotient of two numbers, raising an error if the divisor is zero.

### `string_operations.py`

- **`concatenate(str1, str2)`:** Concatenates two strings.
- **`to_uppercase(string)`:** Converts a string to uppercase.
- **`to_lowercase(string)`:** Converts a string to lowercase.

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

    The tool will:
    - Check if `documentation.md` exists.
    - If it does not exist, generate comprehensive documentation based on a repository overview.
    - If it exists, detect new commits and changes since the last documented commit, then update the documentation accordingly.

2. **View the Documentation**

    Open the generated `documentation.md` file to review the documentation. The final line of the file includes a commit marker in the format:

    ```
    Last Documented Commit: <commit_hash>
    ```

## Dependencies

The project requires the following Python packages, as specified in `requirements.txt`:

- `langchain==0.3.21`
- `langchain_openai==0.3.9`
- `python-dotenv==1.0.1`

Ensure all dependencies are installed to avoid any issues during execution.

Last Documented Commit: d4e18dd405ef415738a2cf80dd15adcef083cb69