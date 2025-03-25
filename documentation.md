# Code-Doc-Gen Project Documentation

## Dynamic Content Start

# Code-Doc-Gen Project Documentation

## Overview

The Code-Doc-Gen project is designed to automatically generate and update documentation for code changes in a repository. It leverages LangChain and OpenAI's GPT-4o to create comprehensive documentation by integrating with Git to detect code changes, extract a repository overview, and update documentation accordingly. The tool is adaptable to any project and maintains a record of updates by embedding a commit marker in the generated documentation.

## Features

- **Automatic Documentation Generation**: Utilizes GPT-4o to generate markdown documentation based on the repository's structure and changes.
- **Git Integration**: Detects new commits and changes using Git logs and diffs, and commits documentation updates to a dedicated branch.
- **Dynamic Prompt Building**: Constructs prompts for the language model based on the existence of documentation and recent changes.
- **Extensibility**: The modular design allows for easy customization and integration with additional systems.

## File Structure

- **.gitignore**: Specifies files and directories to be ignored by Git, such as `.env`.
- **README.md**: Provides an overview of the project, setup instructions, and usage guidelines.
- **agent_version_doc_gen.py**: Contains the logic for detecting changes, generating documentation, and committing updates.
- **doc_gen.py**: Handles the generation and updating of documentation, including managing commit markers.
- **file_operations.py**: Provides basic file read and write operations.
- **langchain_github_documenter.ipynb**: A Jupyter notebook for testing and R&D purposes.
- **main.py**: A simple script that prints greetings to the console.
- **math_operations.py**: Implements basic math operations such as addition, subtraction, multiplication, and division.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **string_operations.py**: Contains functions for string manipulation, including concatenation and case conversion.

## Key Modules and Functions

### agent_version_doc_gen.py

- **update_sections**: Updates specific sections of the documentation based on detected changes.
- **get_last_documented_commit**: Extracts the last documented commit hash from the documentation file.
- **get_new_commits**: Returns a list of commit messages and hashes since the provided commit.
- **get_diff_since_commit**: Returns the diff of changes since the provided commit.
- **get_structured_git_diff**: Parses git diff into structured categories: added, modified, deleted files.
- **get_repo_overview**: Provides an overview of the repository structure and content.
- **run_agent**: Initializes and runs the agent to generate or update documentation.

### doc_gen.py

- **get_current_commit_hash**: Retrieves the current HEAD commit hash.
- **get_structured_diff**: Gets structured diff since the last documented commit.
- **generate_documentation_content**: Generates documentation using GPT-4o.
- **update_documentation_file**: Updates the documentation file with new content and commit markers.
- **commit_to_documentation_branch**: Handles git operations for committing documentation updates.

### math_operations.py

- **add(a, b)**: Returns the sum of `a` and `b`.
- **subtract(a, b)**: Returns the difference between `a` and `b`.
- **multiply(a, b)**: Returns the product of `a` and `b`.
- **divide(a, b)**: Returns the division of `a` by `b`, raises an error if `b` is zero.

### string_operations.py

- **concatenate(str1, str2)**: Concatenates two strings.
- **to_uppercase(string)**: Converts a string to uppercase.
- **to_lowercase(string)**: Converts a string to lowercase.

## Usage Examples

1. **Clone the Repository**

   bash
   git clone <repository-url>
   cd <repository-directory>
   

2. **Create a Virtual Environment and Install Dependencies**

   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   

3. **Configure Environment Variables**

   Create a `.env` file in the root directory and add your OpenAI API key:

   env
   LANGSMITH_TRACING=true
   LANGSMITH_ENDPOINT=<endpoint>
   LANGSMITH_API_KEY=<key>
   LANGSMITH_PROJECT=<project name>
   OPENAI_API_KEY=<key>
   

4. **Generate or Update Documentation**

   Run the documentation generation script:

   bash
   python documentation_generator.py
   

   The tool will check for existing documentation and update it based on recent changes.

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

## Static Content Start
### Usage Examples
[Preserved content]

### Contributing
[Preserved content]

### License
[Preserved content]

### Contact
[Preserved content]

Last Documented Commit: 54c83936b3e1546391a95f103c1af83096586d29