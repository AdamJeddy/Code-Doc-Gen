from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
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


###################
## Tools Section ##
################### 

@tool
def github_documentation_commit(commit_message=""):
    """ Commits the current changes to the 'documentation' branch of the Github repository """
    branch_name = "documentation"
    commit_message_main = f"{commit_message} - {datetime.now().strftime('%d-%m-%y %H:%M:%S')}"
    
    # Switchs to the "documentation" branch (or Creates it if it doesn't exist)
    subprocess.run(["git", "checkout", "-B", branch_name])
    
    # Add only .md files
    subprocess.run(["git", "add", "*.md"])
    
    # Commit with the message
    subprocess.run(["git", "commit", "-m", commit_message_main])
    
    # Push to the remote repository
    subprocess.run(["git", "push", "-u", "origin", branch_name])
    
    return "Committed to Github on branch 'documentation'"

def create_file_tool(file_contents: str, file_path: str) -> str:
    """
    Function that creates/updates a markdown file with the contents provided as input 
    and file path provided as inputs
    """
    
    # Remove any Markdown formatting if present
    if file_contents.startswith("```") and file_contents.endswith("```"):
        file_contents = file_contents.strip("```").strip()
    
    with open(file_path, "w") as f:
        f.write(file_contents)
    
    return "File updated"

@tool
def check_document_file_exists() -> str:
    """Checks if the repository has a file named 'document.md'"""
    if os.path.isfile("document.md"):
        return "File 'document.md' exists"
    else:
        return "File 'document.md' does not exist"


create_file_tool = StructuredTool.from_function(create_file_tool)
tools = [github_documentation_commit, create_file_tool, check_document_file_exists]



###################
## Agent Section ##
###################

agent_executor = initialize_agent(
    tools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

agent_executor.invoke(
    {
        "input": "Write a basic code documentation in markdown format with the file name as documentation.md. Output ONLY THE MARKDOWN without wrapping it in ```. Commit changes to branch called documentation with an appropriate commit message."
    }
)