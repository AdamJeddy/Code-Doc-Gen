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
    Updates the documentation file. If current_content exists, only update the dynamic sections:
    - Overview and project-specific sections.
    - "Recent Changes" section should be updated/merged without duplicating static sections.
    """
    new_commit_marker = f"Last Documented Commit: {get_current_commit_hash()}"
    
    # If no current content exists, just output new content with commit marker.
    if not current_content:
        return f"{new_content}\n\n{new_commit_marker}"
    
    # Otherwise, parse the current documentation into two parts:
    # 1. The static part (e.g. Usage, Contributing, License, Contact) that should remain untouched.
    # 2. The dynamic part (Overview, File Structure, Recent Changes) that will be updated.
    # You can use a delimiter (e.g. a specific marker) to separate these.
    # For example, assume the dynamic section starts with a marker "## Dynamic Content Start"
    # and static content follows a marker "## Static Content Start".
    
    dynamic_marker = "## Dynamic Content Start"
    static_marker = "## Static Content Start"
    
    if dynamic_marker in current_content and static_marker in current_content:
        dynamic_part = current_content.split(static_marker)[0]
        static_part = current_content.split(static_marker)[1]
    else:
        # Fallback: if no markers exist, assume the whole document is dynamic.
        dynamic_part = current_content
        static_part = ""
    
    # Remove any placeholders from new_content
    new_content = re.sub(r"\[.*?briefly describe.*?\]", "", new_content, flags=re.IGNORECASE)
    
    # Update the dynamic section:
    # Instead of appending a whole new "Recent Changes" section at the end,
    # find an existing "Recent Changes" section and merge new changes.
    # For example, extract the existing recent changes block if present:
    recent_changes_pattern = r"(## Recent Changes\s*\n)(.*?)(\n## |\Z)"
    match = re.search(recent_changes_pattern, dynamic_part, flags=re.DOTALL)
    
    if match:
        header, existing_changes, tail = match.groups()
        # Prepare new recent changes block (could be a summary of the changes)
        new_recent_changes = f"{header}{new_content.strip()}\n"  # new changes overwrite old for demo purpose
        # Replace the existing recent changes section with the new one.
        updated_dynamic = re.sub(recent_changes_pattern, new_recent_changes + tail, dynamic_part, flags=re.DOTALL)
    else:
        # If no Recent Changes section exists, append one to the dynamic part.
        updated_dynamic = dynamic_part.strip() + f"\n\n## Recent Changes\n{new_content.strip()}\n"
    
    # Combine the updated dynamic part, static part, and new commit marker.
    updated_content = f"{updated_dynamic}\n\n## Static Content Start\n{static_part.strip()}\n\n{new_commit_marker}"
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

Using this context, update the existing documentation to reflect these changes.
Ensure that you update only the relevant sections, add a "Recent Changes" section, and preserve all accurate details from the previous documentation.
Format your response in Markdown.
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