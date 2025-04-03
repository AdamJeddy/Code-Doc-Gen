# Code-Doc-Gen Documentation

## Overview

Code-Doc-Gen is a tool designed to automatically generate and update documentation for code changes using LangChain and OpenAI's GPT-4o. The project is structured to analyze the complete repository content, detect changes, and maintain documentation with commit tracking. It integrates with Git to ensure that documentation is always up-to-date with the latest code changes.

### Key Features

- **Complete Repository Analysis**: Analyzes all tracked files for initial documentation.
- **Intelligent Change Tracking**: Uses structured diffs to categorize changes while excluding the documentation file itself.
- **Context-Aware Updates**: Preserves static content while dynamically updating change summaries.
- **Git Integration**: Maintains documentation in a dedicated branch with automatic commits.
- **Adaptive Prompting**: Generates context-specific prompts for both initial creation and updates.

## File Structure

- **.gitignore**: Specifies files and directories to be ignored by Git, such as `.env`.
- **README.md**: Provides an overview of the project, setup instructions, and usage details.
- **agent_version_doc_gen.py**: Contains the initial experimental version of the documentation generator using an agent-based approach.
- **doc_gen.py**: Implements the current stable version of the documentation generator with enhanced features.
- **langchain_github_documenter.ipynb**: A Jupyter notebook for research and development of code sections.
- **main.py**: A simple script demonstrating the use of utility functions.
- **math_utils.py**: Provides basic mathematical operations.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **string_utils.py**: Contains string manipulation functions.
- **test_math_utils.py**: Unit tests for the `math_utils.py` module.

## Key Modules and Functions

### doc_gen.py

- **get_current_commit_hash()**: Retrieves the current HEAD commit hash.
- **get_structured_diff(last_commit)**: Obtains a structured diff since the last documented commit, excluding `documentation.md`.
- **generate_documentation_content(context)**: Generates documentation using GPT-4o based on the provided context.
- **update_documentation_file(new_content, current_content)**: Updates the documentation file by appending new content and a commit marker.
- **commit_to_documentation_branch()**: Handles Git operations for the documentation branch.
- **get_complete_repo_content()**: Returns a concatenated string of all tracked files with headers.
- **main_flow()**: The main function that orchestrates the documentation generation and update process.

### agent_version_doc_gen.py

- **update_sections(existing_content, changes)**: Updates specific sections of the documentation based on detected changes.
- **get_last_documented_commit(file_path)**: Extracts the last documented commit hash from the documentation file.
- **get_new_commits(since_commit)**: Returns a list of commit messages and hashes since the provided commit.
- **get_structured_git_diff(since_commit)**: Parses git diff into structured categories: added, modified, deleted files.
- **run_agent()**: Initializes and runs the agent to generate or update documentation.

### math_utils.py

- **add(a, b)**: Returns the sum of two numbers.
- **subtract(a, b)**: Returns the difference between two numbers.

### string_utils.py

- **to_uppercase(text)**: Converts a string to uppercase.
- **reverse_string(text)**: Reverses the given string.

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

    Create a `.env` file in the root directory with:

    ```env
    OPENAI_API_KEY=<your-api-key>
    LANGSMITH_TRACING=true
    LANGSMITH_ENDPOINT=<endpoint>
    LANGSMITH_API_KEY=<key>
    LANGSMITH_PROJECT=<project-name>
    ```

### Running the Documentation Generator

1. **Generate/Update Documentation**

    Run the current version:

    ```bash
    python doc_gen.py
    ```

    The tool will:
    - Create initial documentation from complete repository analysis.
    - For updates: analyze changes since the last documented commit.
    - Maintain persistent documentation in `documentation.md`.
    - Commit changes to the `documentation` branch.

2. **View Documentation**

    The generated `documentation.md` contains:
    - Project overview and structure.
    - Detailed file descriptions.
    - Version-specific change history.
    - Final commit marker:  
      `Last Documented Commit: <commit_hash>`

## Dependencies

- **langchain==0.3.21**
- **langchain_openai==0.3.10**
- **python-dotenv==1.0.1**

Ensure all dependencies are installed in your virtual environment to run the project successfully.

Last Documented Commit: f741c88b003565dcc52e24be3b1171744be78f36