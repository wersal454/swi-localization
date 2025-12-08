#!/usr/bin/env python3
"""
XML String Comparison Tool
==========================

This script compares the content of <t> tags between two XML files
and finds IDs where the content has changed.

Usage:
    python compare_xml_changes.py path/to/old.xml path/to/new.xml

Example:
    python compare_xml_changes.py 0001.xml 0001-L007.xml

Output:
    - List of IDs where content changed, with old and new values
    - Summary statistics
"""

import xml.etree.ElementTree as ET
import sys
import os
from collections import defaultdict

def extract_strings(file_path):
    """
    Extract all id and text content from <t> tags in XML file.
    
    Returns:
        dict: {id: text} pairs
        set: All IDs in the file
    """
    id_to_text = {}
    all_ids = set()
    
    try:
        tree = ET.parse(file_path)
        for t in tree.iter('t'):
            t_id = t.get('id')
            if t_id:
                all_ids.add(t_id)
                # Get text content, default to empty string if None
                text = t.text if t.text is not None else ""
                # Strip whitespace for comparison (optional)
                text = text.strip()
                id_to_text[t_id] = text
                
    except ET.ParseError as e:
        print(f"XML parsing error in {file_path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    return id_to_text, all_ids

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_xml_changes.py <old_file.xml> <new_file.xml>")
        print("Example: python compare_xml_changes.py english.xml german_updated.xml")
        sys.exit(1)
    
    old_file, new_file = sys.argv[1], sys.argv[2]
    
    # Extract strings from both files
    print(f"Processing files:\n  Old: {old_file}\n  New: {new_file}")
    print("-" * 50)
    
    old_strings, old_ids = extract_strings(old_file)
    new_strings, new_ids = extract_strings(new_file)
    
    # Find common IDs (exist in both files)
    common_ids = old_ids.intersection(new_ids)
    
    # Find IDs where text has changed
    changed_ids = []
    changes = []
    
    for t_id in sorted(common_ids, key=int):
        old_text = old_strings.get(t_id, "")
        new_text = new_strings.get(t_id, "")
        
        if old_text != new_text:
            changed_ids.append(t_id)
            changes.append({
                'id': t_id,
                'old': old_text,
                'new': new_text
            })
    
    # Find added and removed IDs (optional)
    added_ids = new_ids - old_ids
    removed_ids = old_ids - new_ids
    
    # Output results
    print("\n" + "=" * 50)
    print("COMPARISON RESULTS")
    print("=" * 50)
    
    # Summary statistics
    print(f"\nSummary:")
    print(f"  Total strings in old file: {len(old_ids)}")
    print(f"  Total strings in new file: {len(new_ids)}")
    print(f"  Common strings: {len(common_ids)}")
    print(f"  Changed strings: {len(changed_ids)}")
    print(f"  Added strings: {len(added_ids)}")
    print(f"  Removed strings: {len(removed_ids)}")
    
    # Detailed changes
    if changes:
        print(f"\nFound {len(changes)} changed strings:")
        print("-" * 50)
        
        for change in changes:
            print(f"\nID: {change['id']}")
            print(f"  Old: {change['old']}")
            print(f"  New: {change['new']}")
            
            # Show character difference if relevant
            if len(change['old']) != len(change['new']):
                print(f"  Length change: {len(change['old'])} → {len(change['new'])} chars")
    
    else:
        print("\nNo changes found in common strings.")
    
    # Show added strings
    if added_ids:
        print(f"\nAdded strings ({len(added_ids)}):")
        for t_id in sorted(added_ids, key=int):
            text = new_strings[t_id]
            print(f"  ID {t_id}: {text}")
    
    # Show removed strings
    if removed_ids:
        print(f"\nRemoved strings ({len(removed_ids)}):")
        for t_id in sorted(removed_ids, key=int):
            text = old_strings[t_id]
            print(f"  ID {t_id}: {text}")
    
    # Export option
    if changes:
        export_option = input("\nExport changes to CSV file? (y/n): ")
        if export_option.lower() == 'y':
            csv_filename = f"changes_{os.path.splitext(os.path.basename(old_file))[0]}.csv"

            try:
                with open(csv_filename, 'w', encoding='utf-8') as f:
                    f.write("ID,Type,Text\n")  # Head

                    for change in changes:
                        # Screening
                        old_escaped = change['old'].replace('"', '""').replace('\n', '\\n')
                        new_escaped = change['new'].replace('"', '""').replace('\n', '\\n')

                        # Old version
                        f.write(f'{change["id"]},Old, "{old_escaped}"\n')
                        # New version
                        f.write(f'{change["id"]},New, "{new_escaped}"\n')
                        # empty line
                        f.write('\n')

                print(f"Changes exported to {csv_filename}")
            except Exception as e:
                print(f"Error exporting to CSV: {e}")

if __name__ == "__main__":
    main()