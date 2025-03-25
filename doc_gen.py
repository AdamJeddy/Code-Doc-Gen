from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import logging
import subprocess
from datetime import datetime
import re

# Configurations
DOCUMENTATION_FILE = "documentation.md"
DOC_BRANCH = "documentation"

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

llm = ChatOpenAI(model='gpt-4o', temperature=0, api_key=os.getenv("OPENAI_API_KEY"))

def get_current_commit_hash():
    """Get the current HEAD commit hash"""
    try:
        return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting commit hash: {e}")
        return None

def get_structured_diff(last_commit):
    """Get structured diff since last documented commit"""
    if not last_commit:
        return {"added": [], "modified": [], "deleted": []}
    
    try:
        diff_output = subprocess.check_output(
            ['git', 'diff', '--name-status', f"{last_commit}..HEAD"]
        ).decode().splitlines()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error getting git diff: {e}")
        return {"added": [], "modified": [], "deleted": []}

    changes = {"added": [], "modified": [], "deleted": []}
    for line in diff_output:
        if not line:
            continue
        status, path = line.split(maxsplit=1)
        if status == 'A':
            changes['added'].append(path)
        elif status == 'M':
            changes['modified'].append(path)
        elif status == 'D':
            changes['deleted'].append(path)
    return changes

def generate_documentation_content(context):
    """Generate documentation using GPT-4o"""
    response = llm.invoke(context)
    return response.content

def update_documentation_file(new_content, current_content=None):
    """
    Updates the documentation file.
    - If no current content exists, it creates a new file with dynamic and static sections.
    - If current content exists, it updates only the dynamic part (which includes Overview and Recent Changes)
      and preserves the static part (Usage, Contributing, License, Contact).
    - It also removes placeholder text and avoids duplicating the recent changes on every run.
    """
    new_commit_marker = f"Last Documented Commit: {get_current_commit_hash()}"
    
    # Clean up new_content: remove any placeholder markers
    new_content = re.sub(r"\[.*?describe.*?\]", "", new_content, flags=re.IGNORECASE).strip()

    # Remove any "```markdown" wrappers from new_content
    new_content = new_content.replace("```markdown", "")

    
    # If no existing content, create a document with clear markers:
    if not current_content:
        # Build a new document with dynamic and static sections
        dynamic_section = new_content + "\n"
        static_section = ""
        return f"# Code-Doc-Gen Project Documentation\n\n{dynamic_section}{static_section}\n{new_commit_marker}"
    
    # Otherwise, split the current content into dynamic and static parts.
    dynamic_marker = "## Dynamic Content Start"
    static_marker = "## Static Content Start"
    
    if dynamic_marker in current_content and static_marker in current_content:
        dynamic_part = current_content.split(static_marker)[0]
        static_part = current_content.split(static_marker)[1]
    else:
        # Fallback: treat entire content as dynamic if markers are missing.
        dynamic_part = current_content
        static_part = ""
    
    # Update the "Recent Changes" section within the dynamic part:
    # Look for an existing "## Recent Changes" header in dynamic_part.
    recent_changes_pattern = r"(## Recent Changes\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(recent_changes_pattern, dynamic_part, flags=re.DOTALL)
    
    # Build a new recent changes summary (you can extend this to include descriptions, commit messages, etc.)
    new_changes_summary = f"### Recent Changes\n{new_content}\n"
    
    if match:
        # Replace the existing recent changes section with the new summary.
        dynamic_updated = re.sub(recent_changes_pattern, new_changes_summary, dynamic_part, flags=re.DOTALL)
    else:
        # If no recent changes section exists, append one at the end of the dynamic part.
        dynamic_updated = dynamic_part.strip() + "\n\n" + new_changes_summary
    
    # Reassemble the document: dynamic part + static part (with its header) + new commit marker.
    updated_content = f"{dynamic_updated}\n\n{static_marker}\n{static_part.strip()}\n\n{new_commit_marker}"
    return updated_content

def commit_to_documentation_branch():
    """Handle git operations for documentation branch"""
    try:
        # Create or checkout documentation branch
        subprocess.run(['git', 'checkout', '-B', DOC_BRANCH], check=True)
        
        # Add and commit documentation
        subprocess.run(['git', 'add', DOCUMENTATION_FILE], check=True)
        subprocess.run(['git', 'commit', '-m', f"docs: Auto-update documentation {datetime.now().isoformat()}"], check=True)
        subprocess.run(['git', 'push', '-f', 'origin', DOC_BRANCH], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Git operation failed: {e}")
        return False

def get_complete_repo_content():
    """Return a concatenated string of all tracked files (with headers) from the repository."""
    try:
        # List all tracked files (this respects .gitignore)
        file_list = subprocess.check_output(['git', 'ls-files']).decode().splitlines()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error listing repo files: {e}")
        return ""
    
    repo_content = []
    for f in file_list:
        if os.path.isfile(f):
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Add a header with the file path so the LLM knows which file it is reading
                    repo_content.append(f"### File: {f}\n```\n{content}\n```\n")
            except Exception as e:
                logging.warning(f"Could not read file {f}: {e}")
    return "\n".join(repo_content)

def main_flow():
    # Check if documentation already exists
    current_content = None
    last_commit = None

    if os.path.exists(DOCUMENTATION_FILE):
        with open(DOCUMENTATION_FILE, 'r') as f:
            current_content = f.read()
        # Extract last documented commit hash from existing documentation
        match = re.search(r"Last Documented Commit: ([a-f0-9]+)", current_content)
        last_commit = match.group(1) if match else None

    if not current_content:
        # No documentation exists: use the entire repository content
        complete_repo = get_complete_repo_content()
        prompt = f"""You are an expert developer and technical writer.
Using the complete code base provided below (which includes file paths and contents), generate detailed documentation that is specific to this project.
Include:
- A clear overview of the project's purpose, features, and goals.
- A breakdown of the file structure (listing each file and its role).
- Descriptions of key modules, functions, and components.
- Usage examples and dependency details (if applicable).

**Important Instructions:**
- Do not include any generic placeholder text (e.g. '[briefly describe...]').
- Do not wrap any text in '```markdown' or similar code fences.
- Output the documentation in Markdown with clear section headers.
- The content should be entirely specific to the code provided.

The complete repository content is provided below:

{complete_repo}

Ensure the documentation is specific to the code, and do not include generic or templated sections.
Format the output in Markdown with clear section headers.
"""
        print(prompt)
    else:
        # Documentation exists: only pass the diff (added, modified, deleted files)
        changes = get_structured_diff(last_commit)
        context = {
            "existing_content": current_content,
            "changes": changes,
            "files_changed": {
                "added": [f for f in changes['added'] if os.path.isfile(f)],
                "modified": [f for f in changes['modified'] if os.path.isfile(f)],
                "deleted": changes['deleted']
            }
        }
        prompt = f"""You are an expert developer and technical writer.
The project documentation already exists. However, there have been changes since the last documented commit.
The changes are as follows:
- Added files: {changes['added']}
- Modified files: {changes['modified']}
- Deleted files: {changes['deleted']}

Using this context, update the documentation to accurately reflect these changes.
**Important Instructions:**
- Do not include any generic placeholder text or any markdown wrappers such as '```markdown'.
- Only update the dynamic sections (such as the Overview and Recent Changes).
- Do not repeat static sections (like Usage, Contributing, License, Contact) that are already present.
- Provide a concise summary for the "Recent Changes" section, including a brief description of what was added, modified, or deleted.
- Output the updated content in Markdown.
"""
        print(context)
        print(prompt)
    
    # Generate documentation content using the LLM (assume generate_documentation_content calls the GPT API)
    new_content = generate_documentation_content(prompt)
    
    # Update the documentation file by appending the new commit marker
    updated_content = update_documentation_file(new_content, current_content)
    
    # Write the updated documentation to file
    with open(DOCUMENTATION_FILE, 'w') as f:
        f.write(updated_content)
    
    # Commit changes to the documentation branch
    if commit_to_documentation_branch():
        logging.info("Documentation updated successfully")
    else:
        logging.error("Failed to update documentation")


if __name__ == "__main__":
    main_flow()