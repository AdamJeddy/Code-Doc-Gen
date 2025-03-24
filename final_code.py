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
    Reads the repository structure and main files to provide a high-level overview.
    This is a simple placeholder implementation. later extend it to read key files,
    extract README content, or analyze main modules.
    """
    overview = "Repository Overview:\n"
    # List the top-level files and directories
    try:
        result = subprocess.run(["ls", "-1"], check=True, capture_output=True, text=True)
        items = result.stdout.strip().split("\n")
        overview += "Top-level items:\n" + "\n".join(items)
    except subprocess.CalledProcessError as e:
        overview += "Error reading repository structure."
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
    Creates or updates a markdown file with the provided contents.
    It appends a marker line with the latest commit hash for reference.
    """
    # Remove any Markdown formatting if present
    if file_contents.startswith("```") and file_contents.endswith("```"):
        file_contents = file_contents.strip("```").strip()
    
    # Obtain the current HEAD commit hash
    try:
        head_commit = subprocess.run(["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error("Error retrieving HEAD commit: " + e.stderr)
        head_commit = "unknown"
    
    # Append/update the marker for the last documented commit
    marker_line = f"\n\nLast Documented Commit: {head_commit}"
    # Optionally, remove any old marker before appending 
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            content = f.read()
        # Remove previous marker if exists
        content = "\n".join([line for line in content.split("\n") if not line.startswith("Last Documented Commit:")])
    else:
        content = ""
    
    new_content = file_contents + marker_line
    with open(file_path, "w") as f:
        f.write(new_content)
    
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



###################
## Agent Section ##
###################

# Determine what has changed since the last documentation update
last_commit = get_last_documented_commit("documentation.md")
new_commits = get_new_commits(last_commit)
diff_details = get_diff_since_commit(last_commit)

# Build a dynamic prompt including new commit info and diff
prompt_template = f"""
There have been the following code changes since the last documentation update:
New Commits:
{chr(10).join(new_commits)}

Diff Summary:
{diff_details[:1000]}  <!-- Truncated to avoid overwhelming the prompt -->

Based on these changes, generate updated documentation in markdown format. 
Do not wrap the output in markdown fences. The file name should be documentation.md.
Include an updated marker with the latest commit hash as the last line in the file.
"""


agent_executor = initialize_agent(
    tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# Invoke the agent with the dynamic prompt
agent_executor.invoke({"input": prompt_template})