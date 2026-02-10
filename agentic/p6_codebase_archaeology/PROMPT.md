# Task: Codebase Archaeology

Analyze the `messy_project/` directory - a deliberately problematic Python codebase - and produce a comprehensive analysis report.

## Your Task

Explore the codebase and create `analysis_report.md` documenting your findings.

## The Codebase

`messy_project/` contains a 20+ file Python project with intentional problems:
- Circular imports (some work, some break)
- Dead code (functions/classes never used)
- Duplicated functions with subtle differences
- Configuration scattered across multiple files
- Hidden bugs

## Required Analysis

Your report must include:

### 1. Dependency Graph
- Which file imports which
- Identify any circular import chains
- Note which imports might fail at runtime

### 2. Dead Code Analysis
- List all functions that are never called
- List all classes that are never instantiated
- Identify entire files that are never imported

### 3. Duplication Report
Find the 3 pairs of duplicated functions:
- Where are they located?
- What are the subtle differences between each pair?
- Which version should be kept and why?

### 4. Configuration Audit
The project loads configuration from multiple sources:
- List all configuration sources (files, env vars, hardcoded)
- Document their intended precedence order
- Identify any conflicts or bugs in how config is loaded

### 5. Bug Hunt
Find and describe the 3 hidden bugs:
- What is the bug?
- In which file/function?
- Under what conditions does it trigger?
- How should it be fixed?

### 6. Refactoring Plan
- Suggest priority order for cleanup
- Identify dependencies between refactoring tasks
- Estimate relative effort (small/medium/large)

## How to Explore

Start with `main.py` to understand the entry point, then:
- Read import statements to understand dependencies
- Search for function definitions vs function calls
- Compare similar function names across files
- Look at all config-related files

## Output Format

Create `analysis_report.md` with clear sections for each of the 6 required analyses. Use markdown formatting with code blocks for file paths and function names.

## Hints

- The project has files in: config/, core/, models/, services/, utils/, legacy/
- Configuration comes from: .py, .json, .yaml, .ini, .env files
- Some comments in the code are misleading
- Dead code includes entire files that are never imported
- The bugs are subtle - look for logic errors, not syntax errors
