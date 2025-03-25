# Code-Doc-Gen
Project for Chalhoub Group Tech Case Study

## Overview

This repository contains a tool that automatically generates and updates documentation for code changes using LangChain and OpenAI's GPT-4o. The project has evolved through two main approaches:

1. **Current Stable Version** (`doc_gen.py`):  
   Implements an enhanced documentation generator that analyzes complete repository content and maintains better change tracking through structured diffs.

2. **Previous Experimental Version** (`agent_version_doc_gen.py`):  
   Initial approach using agent-based implementation (preserved for reference but not working as intended).

The tool integrates with Git to detect code changes, analyzes repository content, and maintains documentation with commit tracking. Key improvements in the current version include complete repository analysis, better change detection, and more robust documentation updates.

## Code Details

- **`doc_gen.py` (Current Version)**  
  Implements the enhanced documentation generator with:
  - Complete repository content analysis for initial documentation
  - Structured diff analysis (added/modified/deleted files)
  - Intelligent documentation updates preserving static content
  - Enhanced Git integration with automatic branch management
  - Exclusion of documentation file from change tracking

- **`agent_version_doc_gen.py` (Archived Version)**  
  Initial experimental approach using:
  - Agent-based prompt generation
  - Repository overview sampling
  - Basic change detection
  - Preserved for reference purposes only

## Project Evolution

The initial agent-based approach (`agent_version_doc_gen.py`) demonstrated functionality but had limitations in content analysis and change tracking. The current version (`doc_gen.py`) implements more robust repository analysis and maintains clearer separation between static documentation elements and dynamic updates.

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

    Create a `.env` file in the root directory with:

    ```env
    OPENAI_API_KEY=<your-api-key>
    LANGSMITH_TRACING=true
    LANGSMITH_ENDPOINT=<endpoint>
    LANGSMITH_API_KEY=<key>
    LANGSMITH_PROJECT=<project-name>
    ```

## How to Run

1. **Generate/Update Documentation**

    Run the current version:

    ```bash
    python doc_gen.py
    ```

    The tool will:
    - Create initial documentation from complete repository analysis
    - For updates: analyze changes since last documented commit
    - Maintain persistent documentation in `documentation.md`
    - Commit changes to `documentation` branch

2. **View Documentation**

    The generated `documentation.md` contains:
    - Project overview and structure
    - Detailed file descriptions
    - Version-specific change history
    - Final commit marker:  
      `Last Documented Commit: <commit_hash>`

## Key Features

- **Complete Repository Analysis**  
  For initial documentation, analyzes all tracked files with context-aware parsing.

- **Intelligent Change Tracking**  
  Uses structured diffs to categorize changes while excluding documentation file itself.

- **Context-Aware Updates**  
  Preserves static content while dynamically updating change summaries.

- **Git Integration**  
  Maintains documentation in dedicated branch with automatic commits.

- **Adaptive Prompting**  
  Generates context-specific prompts for both initial creation and updates.

## Troubleshooting

- **Git Issues**  
  Ensure documentation branch exists: `git checkout -b documentation`

- **API Errors**  
  Verify `.env` contains valid `OPENAI_API_KEY`

- **File Permissions**  
  Ensure script has read access to repository files

- **Dependencies**  
  Confirm installation with `pip freeze -r requirements.txt`

