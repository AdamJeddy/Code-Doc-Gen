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


#########################
## Git Helper Functions##
#########################

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
    Reads the repository structure and provides an overview of up to 10 top-level items.
    For each file, if it is a text file, it includes a short snippet of its content.
    Directories are indicated accordingly.
    """
    overview = "Repository Overview:\nTop-level items:\n"
    try:
        items = os.listdir(".")[:10]
        for item in items:
            if item == "documentation_generator.py":
                continue
            if os.path.isdir(item):
                overview += f"\n- {item}/ (directory)"
            else:
                try:
                    with open(item, "r", encoding="utf-8") as f:
                        content = f.read(2000)
                        snippet = content.strip().replace("\n", " ")[:100]
                        overview += f"\n- {item}: {snippet}..."
                except Exception:
                    overview += f"\n- {item}: (binary or unreadable file)"
    except Exception as e:
        overview += f"\nError reading repository structure: {e}"
    return overview

###################
## Tools Section ##
################### 

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
    # Remove any Markdown formatting if present
    if file_contents.startswith("```") and file_contents.endswith("```"):
        file_contents = file_contents.strip("```").strip()

    # Obtain the current HEAD commit hash
    try:
        head_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True
        ).stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Error retrieving HEAD commit: " + e.stderr)
        head_commit = "unknown"
    new_marker_line = f"Last Documented Commit: {head_commit}"

    if os.path.isfile(file_path):
        # Read the existing file content
        with open(file_path, "r", encoding="utf-8") as f:
            existing_content = f.read()
        
        # Split the file into lines and remove lines that are duplicate updates headings or commit markers
        lines = existing_content.split("\n")
        filtered_lines = []
        for line in lines:
            stripped = line.strip()
            # Remove any line that is exactly an "Updates" heading or starts with the commit marker
            if stripped == "## Updates" or stripped.startswith("Last Documented Commit:"):
                continue
            filtered_lines.append(line)
        base_content = "\n".join(filtered_lines).rstrip()

        # Append the new Updates section only if there is update content
        if file_contents.strip():
            updated_content = f"{base_content}\n\n## Updates\n{file_contents.strip()}\n\n{new_marker_line}"
        else:
            updated_content = f"{base_content}\n\n{new_marker_line}"
    else:
        # File doesn't exist; create new content with update section and marker.
        updated_content = f"{file_contents.strip()}\n\n{new_marker_line}"

    # Write the updated content back to the file
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
tools = [github_documentation_commit, create_file_tool, check_document_file_exists]


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
        This repository does not yet have a documentation file. Based on the following repository overview, generate comprehensive documentation in markdown format.
        
        {repo_overview}
        
        The documentation should include sections such as Overview, File Structure, Features & Important Functions. 
        Ensure that the final line includes a marker with the latest commit hash in the format:
        Last Documented Commit: <commit_hash>
        
        The output should be named as {DOCUMENTATION_FILE} and should not be wrapped in markdown fences.
        
        Make sure the document is created on a new branch called '{DOC_BRANCH}' and pushed to the remote repository.
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
        The current documentation was last updated at commit {last_commit}.
        Since then, the following commits have been made:
        
        New Commits:
        {chr(10).join(new_commits)}
        
        Diff Summary:
        {diff_details[:2000]}  <!-- This summary is truncated to avoid overwhelming the prompt -->
        
        Based on these recent changes, update the existing documentation in markdown format.
        Changes should add to a section called 'Updates' that includes summary of the changes since the last documentation update. 
        The final line of the output must include an updated marker with the latest commit hash in the following format, make sure to replace the existing marker:
        Last Documented Commit: <commit_hash>
        
        The output should be named as {DOCUMENTATION_FILE} and should not be wrapped in markdown fences.
        
        Make sure the document is created on a new branch called '{DOC_BRANCH}' and pushed to the remote repository.
        """
    
    # Initialize and invoke the agent with the dynamic prompt
    agent_executor = initialize_agent(
        tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )
    
    # Invoke the agent with the dynamic prompt
    agent_executor.invoke({"input": prompt_template})

if __name__ == "__main__":
    run_agent()