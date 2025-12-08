#!/usr/bin/env python3
"""
XML String Comparison Tool with Visual Diff
"""

import xml.etree.ElementTree as ET
import sys
from difflib import ndiff

def colored_diff(text1, text2):
    """
    Return colored diff between two strings.
    """
    diff = list(ndiff(text1, text2))
    
    result = []
    for d in diff:
        if d[0] == ' ':
            result.append(d[2])
        elif d[0] == '-':
            result.append(f'\033[91m{d[2]}\033[0m')  # Red for removed
        elif d[0] == '+':
            result.append(f'\033[92m{d[2]}\033[0m')  # Green for added
    
    return ''.join(result)

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_xml_visual.py <file1.xml> <file2.xml>")
        sys.exit(1)
    
    file1, file2 = sys.argv[1], sys.argv[2]
    
    # Parse both files
    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)
    
    # Create dictionaries
    strings1 = {}
    strings2 = {}
    
    for t in tree1.iter('t'):
        t_id = t.get('id')
        if t_id:
            strings1[t_id] = t.text or ""
    
    for t in tree2.iter('t'):
        t_id = t.get('id')
        if t_id:
            strings2[t_id] = t.text or ""
    
    # Find common IDs
    common_ids = set(strings1.keys()) & set(strings2.keys())
    
    print(f"\n{'='*60}")
    print(f"Visual Comparison: {file1} vs {file2}")
    print(f"{'='*60}")
    
    changed_count = 0
    for t_id in sorted(common_ids, key=int):
        text1 = strings1[t_id]
        text2 = strings2[t_id]
        
        if text1 != text2:
            changed_count += 1
            print(f"\n\033[93mID: {t_id}\033[0m")  # Yellow for ID
            
            # Show side-by-side comparison for short strings
            if len(text1) < 50 and len(text2) < 50:
                print(f"  Old: {text1}")
                print(f"  New: {text2}")
            else:
                # Show visual diff
                print("  Changes:")
                diff = colored_diff(text1, text2)
                print(f"  {diff}")
    
    print(f"\n{'='*60}")
    print(f"Changed strings: {changed_count}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()