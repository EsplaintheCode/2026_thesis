#!/usr/bin/env python3
"""
Check for indentation errors in Python code blocks within a Quarto document
"""

import re
import ast
import sys

def extract_python_blocks(qmd_file):
    """Extract Python code blocks from a .qmd file"""
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find Python code blocks using proper regex
    pattern = r'```\{python\}[^\n]*\n(.*?)```'
    blocks = re.findall(pattern, content, re.DOTALL | re.MULTILINE)
    
    return blocks

def check_block_syntax(code, block_num):
    """Check a Python code block for syntax errors"""
    try:
        # Remove any Quarto-specific directives
        lines = code.split('\n')
        python_lines = []
        for line in lines:
            if not line.strip().startswith('#|'):  # Skip Quarto directives
                python_lines.append(line)
        
        python_code = '\n'.join(python_lines)
        
        # Try to parse the code
        ast.parse(python_code)
        return None
        
    except IndentationError as e:
        return {
            'type': 'IndentationError',
            'block': block_num,
            'line': e.lineno,
            'message': e.msg,
            'text': e.text.strip() if e.text else None
        }
    except SyntaxError as e:
        return {
            'type': 'SyntaxError', 
            'block': block_num,
            'line': e.lineno,
            'message': e.msg,
            'text': e.text.strip() if e.text else None
        }
    except Exception as e:
        return {
            'type': type(e).__name__,
            'block': block_num,
            'message': str(e)
        }

def main():
    qmd_file = 'thesis_working.qmd'
    
    print(f"Checking {qmd_file} for indentation errors...")
    
    try:
        blocks = extract_python_blocks(qmd_file)
        print(f"Found {len(blocks)} Python code blocks")
        
        errors_found = []
        
        for i, block in enumerate(blocks, 1):
            error = check_block_syntax(block, i)
            if error:
                errors_found.append(error)
                
        if errors_found:
            print(f"\n{len(errors_found)} error(s) found:")
            for error in errors_found:
                print(f"\nBlock {error['block']}:")
                print(f"  {error['type']}: {error['message']}")
                if 'line' in error:
                    print(f"  Line {error['line']}: {error.get('text', '(no text)')}")
        else:
            print("\nNo syntax errors found in Python code blocks!")
            
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()