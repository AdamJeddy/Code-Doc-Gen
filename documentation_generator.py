from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import logging
import subprocess
from datetime import datetime
from langchain.tools import tool
from langchain.tools import StructuredTool
from langchain.agents import initialize_agent
from langchain.agents import AgentType

# Configurations
DOCUMENTATION_FILE = "documentation.md"
DOC_BRANCH = "documentation"

# Load environment variables from .env file
load_dotenv()

# Configure some basic levl of logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Creating a GPT-4o model
llm = ChatOpenAI(model='gpt-4o', temperature=0, api_key=os.getenv("OPENAI_API_KEY"))


#################################
## Git Helper & File Functions ##
#################################

def get_last_documented_commit(file_path="documentation.md"):
    """Extracts the last documented commit hash from the documentation file."""
    if not os.path.isfile(file_path):
        return None
    with open(file_path, "r") as f:
        for line in f:
            if line.startswith("Last Documented Commit:"):
                # Expecting a line like: "Last Documented Commit: <commit_hash>"
                return line.split(":", 1)[1].strip()
    return None

def get_new_commits(since_commit):
    """Returns a list of commit messages and hashes since the provided commit."""
    if since_commit:
        cmd = ["git", "log", f"{since_commit}..HEAD", "--oneline"]
    else:
        # If no last commit found, return the full log.
        cmd = ["git", "log", "--oneline"]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        commits = result.stdout.strip().split("\n")
        return commits if commits != [''] else []
    except subprocess.CalledProcessError as e:
        logging.error("Error retrieving git log: " + e.stderr)
        return []

def get_diff_since_commit(since_commit):
    """Returns the diff of changes since the provided commit."""
    if not since_commit:
        # No commit provided, diff from the beginning (or current working tree)
        since_commit = ""
    cmd = ["git", "diff", f"{since_commit}..HEAD"]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Error retrieving git diff: " + e.stderr)
        return ""

def get_repo_overview():
    """
    Reads the repository structure and provides an overview of up to 20 top-level items.
    For each file, if it is a text file, it includes a short snippet of its content.
    Directories are indicated accordingly.
    """
    overview = "Repository Overview:\nTop-level items:\n"
    try:
        items = os.listdir(".")[:20]
        for item in items:
            if item == "documentation_generator.py":
                continue
            if os.path.isdir(item):
                overview += f"\n- {item}/ (directory)"
            else:
                try:
                    with open(item, "r", encoding="utf-8") as f:
                        content = f.read(5000)
                        snippet = content.strip().replace("\n", " ")
                        overview += f"\n- {item}: {snippet}..."
                except Exception:
                    overview += f"\n- {item}: (binary or unreadable file)"
    except Exception as e:
        overview += f"\nError reading repository structure: {e}"
    return overview

def get_repo_diff(since_commit):
    """Returns a diff of changes since the provided commit."""
    cmd = ["git", "diff", f"{since_commit}..HEAD"] if since_commit else ["git", "diff"]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return ""

def get_repo_files():
    """Returns a list of all files in the repository."""
    return [f for f in os.listdir(".") if os.path.isfile(f) and f != "documentation_generator.py"]

###################
## Tools Section ##
################### 

@tool
def read_file(file_path: str) -> str:
    """Reads the content of a given file."""
    if not os.path.isfile(file_path):
        return f"File {file_path} not found."
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return f"Unable to read {file_path}. Might be binary."

@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to a file, creating or updating it."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File {file_path} updated."

@tool
def get_git_diff() -> str:
    """Returns the git diff of the repository."""
    last_commit = get_last_documented_commit()
    return get_repo_diff(last_commit)

@tool
def list_repo_files() -> str:
    """Lists all files in the repository."""
    return "\n".join(get_repo_files())

@tool
def github_documentation_commit(commit_message=""):
    """Commits the current changes to the 'documentation' branch of the Github repository."""
    branch_name = "documentation"
    commit_message_main = f"{commit_message} - {datetime.now().strftime('%d-%m-%y %H:%M:%S')}"
    
    try:
        # Switch to the "documentation" branch (or create it if it doesn't exist)
        result = subprocess.run(["git", "checkout", "-B", branch_name], check=True, capture_output=True, text=True)
        logging.info(result.stdout)
        
        # Add only .md files
        result = subprocess.run(["git", "add", "*.md"], check=True, capture_output=True, text=True)
        logging.info(result.stdout)
        
        # Commit with the message
        result = subprocess.run(["git", "commit", "-m", commit_message_main], check=True, capture_output=True, text=True)
        logging.info(result.stdout)
        
        # Push to the remote repository
        result = subprocess.run(["git", "push", "-u", "origin", branch_name], check=True, capture_output=True, text=True)
        logging.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("An error occurred during Git operations: " + e.stderr)
        return "Failed to commit documentation"
    
    return "Committed to Github on branch 'documentation'"

def create_file_tool(file_contents: str, file_path: str) -> str:
    """
    Creates or updates a markdown file with new update content.
    If the file already exists, this function preserves the existing content
    (such as Overview and File Structure sections) while removing any existing
    "## Updates" sections and commit markers. It then appends a single new "## Updates"
    section with the provided update content and a single new commit marker at the end.
    """
    # Remove any formatting if present
    if file_contents.startswith("```") and file_contents.endswith("```"):
        file_contents = file_contents.strip("```").strip()

    # Get the latest commit hash
    try:
        head_commit = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Error retrieving HEAD commit: " + e.stderr)
        head_commit = "unknown"
    
    new_marker_line = f"Last Documented Commit: {head_commit}"

    if os.path.isfile(file_path):
        # Read the existing file content
        with open(file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
        
        # Remove old commit marker & extra "## Updates" headings
        existing_content = "\n".join([
            line for line in existing_content.split("\n") 
            if not line.startswith("Last Documented Commit:") and line.strip() != "## Updates"
        ])
        
        # Append the new update section only if there are updates
        if file_contents.strip():
            updated_content = f"{existing_content}\n\n## Updates\n{file_contents.strip()}\n\n{new_marker_line}"
        else:
            updated_content = f"{existing_content}\n\n{new_marker_line}"
    else:
        # Create a fresh documentation file
        updated_content = f"{file_contents.strip()}\n\n{new_marker_line}"

    # Write updated content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return "File updated"


@tool
def check_document_file_exists() -> str:
    """Checks if the repository has a file named 'documentation.md'."""
    if os.path.isfile("documentation.md"):
        return "File 'documentation.md' exists"
    else:
        return "File 'documentation.md' does not exist"

# Convert the create_file_tool into a StructuredTool
create_file_tool = StructuredTool.from_function(create_file_tool)
tools = [github_documentation_commit, create_file_tool, check_document_file_exists, read_file, write_file, get_git_diff, list_repo_files]


######################
## Agent Section    ##
######################

def run_agent():
    # Check for last documented commit
    last_commit = get_last_documented_commit(DOCUMENTATION_FILE)

    # Build the dynamic prompt based on whether a documentation file already exists
    if last_commit is None:
        # No documentation exists, so we generate a fresh overview
        repo_overview = get_repo_overview()
        prompt_template = f"""
        # Documentation Generation

        This repository does not have a documentation file yet. Your task is to generate a **comprehensive** documentation file in **Markdown format** based on the repository structure.

        ## Repository Overview:
        {repo_overview}

        ## Requirements:
        - **Structure:** The documentation should include the following sections:
          - **Overview:** General description of the repository.
          - **File Structure:** A breakdown of key files and their purposes.
          - **Features & Important Functions:** Explanation of notable features and functions in the files.
        - **Commit Tracking:** Ensure the last line contains a commit marker in the format:
          ```
          Last Documented Commit: <commit_hash>
          ```
        - **File Name:** `{DOCUMENTATION_FILE}`
        - **Markdown Fences:** Do **not** wrap the output in triple backticks (```) or other code blocks.
        - **Git Handling:** 
          - Create a new branch named **'{DOC_BRANCH}'**.
          - Commit and push the new documentation to the repository.
        """

    else:
        # Existing documentation found; update it based on recent changes.
        new_commits = get_new_commits(last_commit)
        diff_details = get_diff_since_commit(last_commit)

        if not new_commits:
            logging.info("No new commits found since the last documented commit.")
            new_commits = ["No new commits found."]
        if not diff_details:
            logging.info("No diff details found since the last documented commit.")
            diff_details = "No changes detected."
        
        prompt_template = f"""
        # Documentation Update

        The documentation was last updated at commit **{last_commit}**. Since then, the following changes have been made:

        ## Recent Commits:
        {chr(10).join(new_commits)}

        ## Code Changes Summary:
        {diff_details[:5000]}  <!-- Limiting output to avoid exceeding token limits -->

        ## Update Instructions:
        - **Enhance Documentation:** Incorporate these changes into the documentation.
        - **New Section:** Add an **'Updates'** section summarizing these changes.
        - **Commit Tracking:** Replace the existing commit marker with:
          ```
          Last Documented Commit: <commit_hash>
          ```
        - **File Name:** `{DOCUMENTATION_FILE}`
        - **Markdown Fences:** Do **not** wrap the output in triple backticks (```) or other code blocks.
        - **Git Handling:** 
          - Update the documentation in the **'{DOC_BRANCH}'** branch.
          - Commit and push the updated documentation to the repository.
        """

    # Initialize and invoke the agent with the dynamic prompt
    agent_executor = initialize_agent(
        tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    # Invoke the agent with the dynamic prompt
    agent_executor.invoke({"input": prompt_template})

if __name__ == "__main__":
    run_agent()