# Code-Doc-Gen
Project for Chalhoub Group Tech Case Study

## Overview

This repository contains a tool that automatically generates and updates documentation for code changes in a repository using LangChain and OpenAI's GPT-4o. The tool integrates with Git to detect code changes, extract a repository overview, and update documentation. It is designed to be adaptable to any project and keeps track of updates by embedding a commit marker in the generated documentation.

## Code Details

- **`documentation_generator.py`**  
  Contains the core logic for:
  - Detecting new commits and changes using Git logs and diffs.
  - Generating a repository overview by listing key files and directories.
  - Dynamically building prompts for the agent based on whether documentation exists.
  - Creating or updating the documentation file (`documentation.md`) with an embedded commit marker.
  - Committing the documentation changes to a dedicated Git branch.

## Setup

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

## How to Run

1. **Generate or Update Documentation**

    Run the documentation generation script:

    ```bash
    python documentation_generator.py
    ```

    The tool will:
    - Check if `documentation.md` exists.
    - If it does not exist, generate comprehensive documentation based on a repository overview (listing key files and snippets of their contents).
    - If it exists, detect new commits and changes since the last documented commit, then update the documentation accordingly.

2. **View the Documentation**

    Open the generated `documentation.md` file to review the documentation (this should be created on a new branch called `documentation`). The final line of the file includes a commit marker in the format:

    ```
    Last Documented Commit: <commit_hash>
    ```

## Additional Information

- **LangChain Integration:**  
  Utilizes LangChain to interface with GPT-4o for generating markdown documentation based on dynamic prompts.

- **Git Integration:**  
  Uses Git commands via subprocess calls to retrieve commit logs, diffs, and to commit documentation updates. Error handling and logging are included to assist with troubleshooting.

- **Repository Overview:**  
  The tool generates an overview of up to 10 top-level files. For text files, it includes a short snippet (up to 200 characters) to help contextualize the purpose of each file.

- **Extensibility:**  
  The modular design allows you to easily extend or customize the tool to suit different project needs or integrate with additional systems.

## Troubleshooting

- **Git Issues:**  
  Ensure Git is installed and the repository is properly initialized.
  
- **Environment Variables:**  
  Verify that your `.env` file contains a valid OpenAI API key.

- **Dependencies:**  
  Confirm that all dependencies are installed by checking `requirements.txt`.

- **Logging:**  
  Review the logs output to the console for error messages during Git operations or documentation generation.
