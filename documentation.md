# Code-Doc-Gen Project Documentation

## Overview

# Code-Doc-Gen Project Documentation

## Overview

The Code-Doc-Gen project is designed to automatically generate and update documentation for code changes in a repository. It leverages LangChain and OpenAI's GPT-4o to create detailed markdown documentation. The tool integrates with Git to detect code changes, extract a repository overview, and update documentation accordingly. It is adaptable to any project and maintains a record of updates by embedding a commit marker in the generated documentation.

## Features

- **Automatic Documentation Generation**: Uses GPT-4o to generate comprehensive documentation based on the repository's structure and changes.
- **Git Integration**: Detects new commits and changes using Git logs and diffs, and commits documentation updates to a dedicated branch.
- **Dynamic Prompt Building**: Constructs prompts for the language model based on the existence of documentation and recent changes.
- **Commit Tracking**: Embeds a commit marker in the documentation to track the last documented commit.
- **Extensibility**: The modular design allows for easy customization and integration with additional systems.

## File Structure

- **.gitignore**: Specifies files and directories to be ignored by Git, such as `.env`.
- **README.md**: Provides an overview of the project, setup instructions, and usage guidelines.
- **agent_version_doc_gen.py**: Contains the logic for generating and updating documentation using LangChain and GPT-4o.
- **doc_gen.py**: Implements the main flow for generating documentation, handling Git operations, and updating the documentation file.
- **file_operations.py**: Provides utility functions for reading and writing files.
- **langchain_github_documenter.ipynb**: A Jupyter notebook for research and development of the documentation generation process.
- **main.py**: A simple script that prints greetings to the console.
- **math_operations.py**: Implements basic math operations such as addition, subtraction, multiplication, and division.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **string_operations.py**: Implements basic string operations such as concatenation and case conversion.

## Key Modules and Functions

### agent_version_doc_gen.py

- **update_sections**: Updates specific sections of the documentation based on detected changes.
- **get_last_documented_commit**: Extracts the last documented commit hash from the documentation file.
- **get_new_commits**: Returns a list of commit messages and hashes since the provided commit.
- **get_diff_since_commit**: Returns the diff of changes since the provided commit.
- **get_structured_git_diff**: Parses git diff into structured categories: added, modified, deleted files.
- **get_repo_overview**: Provides an overview of the repository structure and contents.
- **run_agent**: Initializes and invokes the agent to generate or update documentation.

### doc_gen.py

- **get_current_commit_hash**: Retrieves the current HEAD commit hash.
- **get_structured_diff**: Gets structured diff since the last documented commit.
- **generate_documentation_content**: Generates documentation using GPT-4o.
- **update_documentation_file**: Updates the documentation file with new content and a commit marker.
- **commit_to_documentation_branch**: Handles Git operations for the documentation branch.
- **main_flow**: Main function to execute the documentation generation and update process.

### file_operations.py

- **read_file**: Reads the content of a given file.
- **write_file**: Writes content to a file, creating or updating it.

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

To generate or update documentation, run the following command:

```bash
python documentation_generator.py
```

This will check for the existence of `documentation.md`, generate or update the documentation based on recent changes, and commit the updates to the `documentation` branch.

## Dependencies

The project requires the following Python packages, as specified in `requirements.txt`:

- `langchain==0.3.21`
- `langchain_openai==0.3.9`
- `python-dotenv==1.0.1`

Ensure these dependencies are installed in your virtual environment before running the project.

Last Documented Commit: c27427d18057baf48192af0adcc1debc46a3571f