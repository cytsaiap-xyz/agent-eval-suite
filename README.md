# Agent Evaluation Suite

A comprehensive evaluation framework for testing AI coding and agentic abilities.
All tests work **completely offline** - no API calls required.

## Overview

- **5 Coding Problems** - Algorithm, web dev, debugging, optimization
- **10 Agentic Problems** - Multi-step reasoning, iteration, tool usage, document processing

## Quick Start

```bash
# Navigate to suite
cd agent-eval-suite

# Run all evaluations
python harness/run_all.py

# Or run individual problems
python coding/p1_data_pipeline/evaluate_p1.py solution.py
python agentic/p6_codebase_archaeology/evaluate_p6.py analysis_report.md
```

## Problem Structure

### Coding Problems (100 pts each)

| # | Problem | Difficulty | Focus |
|---|---------|------------|-------|
| 1 | Data Pipeline | Hard | Data cleaning, edge cases |
| 2 | Interpreter | Very Hard | Lexer, parser, recursion |
| 3 | Kanban Board | Hard | DOM, state, undo/redo |
| 4 | Concurrency Bugs | Very Hard | Race conditions, locking |
| 5 | Performance Opt | Hard | Algorithm optimization |

### Agentic Problems (100 pts each)

| # | Problem | Expected Iterations | Focus |
|---|---------|---------------------|-------|
| 6 | Codebase Archaeology | 8-20 tool calls | Multi-file analysis |
| 7 | Test Generation | 10-20 iterations | Coverage targeting |
| 8 | Data Transformation | 12-25 tool calls | Multi-format ETL |
| 9 | Debug Loop | 15-30 iterations | Iterative debugging |
| 10 | Markdown Converter | 10-25 iterations | Self-correcting code |
| 11 | Word Document Analysis | 10-20 tool calls | DOCX parsing, TOC |
| 12 | PowerPoint Generation | 15-25 tool calls | PPTX creation, charts |
| 13 | Excel Processing | 15-30 tool calls | XLSX formulas, pivot |
| 14 | PDF Extraction | 10-20 tool calls | PDF parsing, tables |
| 15 | Multi-Format Integration | 20-35 tool calls | All formats combined |

## Directory Structure

```
agent-eval-suite/
├── README.md
├── harness/
│   ├── run_all.py          # Run all evaluations
│   └── score_report.py     # Generate summary report
├── coding/
│   ├── p1_data_pipeline/
│   │   ├── PROBLEM.md
│   │   ├── sales_data.csv
│   │   └── evaluate_p1.py
│   ├── p2_interpreter/
│   ├── p3_kanban/
│   ├── p4_concurrency/
│   └── p5_optimization/
├── agentic/
│   ├── p6_codebase_archaeology/
│   ├── p7_test_generation/
│   ├── p8_data_transformation/
│   ├── p9_debug_loop/
│   ├── p10_markdown_converter/
│   ├── p11_docx_analysis/
│   ├── p12_pptx_generation/
│   ├── p13_xlsx_processing/
│   ├── p14_pdf_extraction/
│   └── p15_multi_format/
└── results/
    └── (evaluation results go here)
```

## Usage for Model Evaluation

### Testing a Model

1. Give the model access to a problem directory
2. Present the PROBLEM.md to the model
3. Let the model work on the solution
4. Run the evaluation script

### Scoring

Each problem is worth 100 points. Suggested overall scoring:

| Range | Rating |
|-------|--------|
| 900-1000 | Exceptional |
| 750-899 | Strong |
| 500-749 | Competent |
| 250-499 | Developing |
| < 250 | Needs improvement |

### Model Discrimination

Problems are designed to differentiate between models:

- **Weak models**: Will struggle with basic features, miss edge cases
- **Average models**: Complete basic requirements, miss advanced features
- **Strong models**: Handle most features, good iteration
- **Exceptional models**: Complete all features, efficient iteration, edge case handling

## Requirements

- Python 3.10+
- Standard library only for problems
- pytest, coverage for test evaluation (p7, p9)
- flask, flask-sqlalchemy for p9
- python-docx, python-pptx, openpyxl for p11-p13, p15
- reportlab, PyMuPDF for p14-p15

Install dependencies:
```bash
pip install pytest pytest-cov flask flask-sqlalchemy pyyaml python-docx python-pptx openpyxl reportlab PyMuPDF
```

## Offline Guarantee

All problems are designed to work offline:
- No API calls to external services
- No internet connectivity required
- All test data included in the suite
- No external packages beyond standard library + testing tools

## Contributing

To add new problems:
1. Create problem directory under coding/ or agentic/
2. Include PROBLEM.md with full specification
3. Add evaluate_XX.py script
4. Provide all test data
5. Update this README

## License

MIT License - Use freely for evaluating AI coding assistants.
