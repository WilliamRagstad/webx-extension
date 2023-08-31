"""
Pre-processor for the Textmate grammar language.

This script is used to compile an extended Textmate grammar language
into a JSON file that can be used by the VSCode editor.

The grammar language is extended to include the following features:
    - Comments
    - Regular expression macros/variables
    - Regular expression templates replaced by macros

Usage: python3 compile.py <input_file> <output_file>
"""

import argparse
import json
import sys

def remove_comment(line: str) -> str:
    """
    Remove comments from a line.
    Handles strings with "//" in them.
    """
    is_in_string = False
    comment_idx = -1
    for i in range(len(line)):
        if line[i] == '"': is_in_string = not is_in_string
        elif line[i] == '/' and line[i + 1] == '/' and not is_in_string:
            comment_idx = i
            break
    if comment_idx != -1: line = line[:comment_idx]
    return line

def replace_all_macros_in_template(template: str, macros: dict) -> str:
    """
    Replace macros in a regular expression template.
    Formatted as {{macro_name}}.
    """
    for macro in macros:
        template = template.replace("{{" + macro + "}}", macros[macro])
    return template

def handle_field(field, macros: dict):
    """Handle a field of the JSON object."""
    if isinstance(field, str):
        return replace_all_macros_in_template(field, macros)
    elif isinstance(field, dict):
        return apply_macros(field, macros)
    elif isinstance(field, list):
        for i in range(len(field)):
            field[i] = handle_field(field[i], macros)
        return field
    else:
        return field

def apply_macros(obj: dict, macros: dict) -> dict:
    """Apply macros to the JSON object."""
    # 1. Apply macros to the current macro field (if any)
    # 2. Create a new macro environment with the merged macros
    # 4. Recursively apply macros to the fields of the current object
    # 5. Return the updated object
    local_macros = macros.copy()
    if "macros" in obj:
        # local_macros.update(apply_macros(obj["macros"], macros))
        for macro in obj["macros"]:
            local_macros[macro] = replace_all_macros_in_template(obj["macros"][macro], local_macros)
        del obj["macros"]
    for key in obj:
        obj[key] = handle_field(obj[key], local_macros)
    return obj

def main():
    """Main function."""
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="input file")
    parser.add_argument("output_file", help="output file")
    args = parser.parse_args()

    # Read input file
    obj = None
    with open(args.input_file, "r") as f:
        # Store all text in a string
        lines = f.readlines()
        total = '\n'.join(map(remove_comment, lines))
        try:
            obj = json.loads(total)
        except json.decoder.JSONDecodeError as e:
            print("Error: invalid JSON file", file=sys.stderr)
            lineNr = e.lineno
            line = lines[lineNr - 1]
            print("Line", lineNr, ":", line, file=sys.stderr)
            print(e, file=sys.stderr)
            sys.exit(1)
    
    # Pre-process JSON
    obj = apply_macros(obj, {})

    # Write output file
    with open(args.output_file, "w") as f:
        json.dump(obj, f, indent=4)
    
    print("Successfully compiled", args.input_file, "to", args.output_file)
    sys.exit(0)

if __name__ == "__main__":
    main()