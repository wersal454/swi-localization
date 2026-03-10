import xml.etree.ElementTree as ET
import sys

def extract_ids(file_path):
    """Extract all id attribute values from <t> tags in XML file"""
    ids = set()
    try:
        tree = ET.parse(file_path)
        for t in tree.iter('t'):
            t_id = t.get('id')
            if t_id:
                ids.add(t_id)
    except ET.ParseError as e:
        print(f"XML parsing error in {file_path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)
    return ids

def main():
    if len(sys.argv) != 3:
        print("Usage: python compare_xml_ids.py <file1.xml> <file2.xml>")
        sys.exit(1)

    file1, file2 = sys.argv[1], sys.argv[2]
    
    # Extract IDs from both files
    ids1 = extract_ids(file1)
    ids2 = extract_ids(file2)
    
    # Find IDs missing in second file
    missing_ids = sorted(ids1 - ids2, key=int)
    
    # Format output
    if missing_ids:
        print(f"Found {len(missing_ids)} missing IDs in second file:")
        print("\n".join(missing_ids))
    else:
        print("All IDs from first file exist in second file")

if __name__ == "__main__":
    main()