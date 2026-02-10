# Problem 6: Codebase Archaeology

## Difficulty: Very Hard (Agentic)
## Expected Tool Calls: 8-20
## Discrimination Target: Systematic exploration, cross-referencing, iterative discovery

## Task

Analyze a deliberately messy codebase and produce a comprehensive report.

## The Codebase

A 20+ file Python project with:
- Circular imports (some working, some will break)
- Dead code (functions never called anywhere)
- Duplicated functions with subtle differences
- Configuration scattered across 5+ files
- Hidden bugs that only trigger in edge cases
- Misleading comments and docstrings

## Your Mission

Produce `analysis_report.md` with:

### 1. Dependency Graph (20 pts)
- List which file imports which
- Identify any circular import chains
- Mark which imports will fail at runtime

### 2. Dead Code Analysis (20 pts)
- List all functions/classes never called
- List all variables assigned but never used
- Identify unreachable code blocks

### 3. Duplication Report (15 pts)
- Find the 3 pairs of duplicated functions
- Explain the subtle differences between each pair
- Recommend which version to keep

### 4. Configuration Audit (15 pts)
- List all configuration sources (files, env vars, hardcoded)
- Document their precedence order
- Identify any conflicting values

### 5. Bug Hunt (20 pts)
- Find and describe the 3 hidden bugs
- Explain under what conditions they trigger
- Provide fixes

### 6. Refactoring Plan (10 pts)
- Suggest priority order for cleanup
- Estimate effort for each item
- Identify dependencies between refactoring tasks

## Files Structure

```
messy_project/
├── __init__.py
├── main.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── local_settings.py
│   └── defaults.yaml
├── core/
│   ├── __init__.py
│   ├── engine.py
│   ├── processor.py
│   └── utils.py
├── models/
│   ├── __init__.py
│   ├── user.py
│   ├── data.py
│   └── helpers.py
├── services/
│   ├── __init__.py
│   ├── api.py
│   ├── database.py
│   └── cache.py
├── utils/
│   ├── __init__.py
│   ├── common.py
│   ├── formatting.py
│   └── validation.py
├── legacy/
│   ├── old_processor.py
│   └── deprecated.py
├── config.json
├── config.ini
└── .env.example
```

## Evaluation

```bash
python evaluate_p6.py analysis_report.md
```

The evaluator checks:
- All dependency relationships identified
- All dead code found
- All duplications found with correct diff
- All config sources identified
- All bugs found and explained
- Refactoring plan is logical

## Hints

- Start by reading `main.py` to understand entry points
- Use grep to find all import statements
- Track function definitions vs function calls
- Check for similar function names across files
- Look for TODO/FIXME/BUG comments (some are misleading!)
- Configuration can come from: .py, .json, .yaml, .ini, .env, env vars
