import json
import os

# Define source and target directories
source_dir = 'data_aggregated'
target_dir = 'resolve_duplicates'

# Create target directory if it doesn't exist
os.makedirs(target_dir, exist_ok=True)

def adjust_category_id(category_id_str):
    """
    Adjust category_id based on the rules:
    - If 11, 12, or 13: decrease by 10
    - If higher than 13: decrease by 7
    - Otherwise: keep unchanged
    """
    if not category_id_str:
        return category_id_str
    
    try:
        category_id = int(category_id_str)
        
        if category_id in [11, 12, 13]:
            new_id = category_id - 10
        elif category_id > 13:
            new_id = category_id - 3
        else:
            new_id = category_id
        
        return str(new_id)
    except (ValueError, TypeError):
        # If conversion fails, return original value
        return category_id_str

def process_json_file(filepath, filename):
    """Process a single JSON file and adjust category_id values"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        adjustments_made = 0
        total_entries = len(data)
        
        # Process each entry in the JSON file
        for key, entry in data.items():
            if isinstance(entry, dict) and 'category_id' in entry:
                original_value = entry['category_id']
                adjusted_value = adjust_category_id(original_value)
                
                if original_value != adjusted_value:
                    entry['category_id'] = adjusted_value
                    adjustments_made += 1
        
        # Save the processed data to target directory
        target_filepath = os.path.join(target_dir, filename)
        with open(target_filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return {
            'filename': filename,
            'total_entries': total_entries,
            'adjustments_made': adjustments_made,
            'status': 'success'
        }
        
    except Exception as e:
        return {
            'filename': filename,
            'total_entries': 0,
            'adjustments_made': 0,
            'status': 'error',
            'error': str(e)
        }

print("Starting category_id duplicate resolution...")
print("=" * 60)

# Get all JSON files in the source directory
json_files = [f for f in os.listdir(source_dir) if f.endswith('.json')]

if not json_files:
    print(f"No JSON files found in {source_dir}")
    exit()

processing_results = []

# Process each JSON file
for filename in sorted(json_files):
    filepath = os.path.join(source_dir, filename)
    
    print(f"Processing: {filename}")
    result = process_json_file(filepath, filename)
    processing_results.append(result)
    
    if result['status'] == 'success':
        if result['adjustments_made'] > 0:
            print(f"  ✅ {result['total_entries']} entries, {result['adjustments_made']} category_id adjustments made")
        else:
            print(f"  ✅ {result['total_entries']} entries, no category_id adjustments needed")
    else:
        print(f"  ❌ Error: {result['error']}")
    
print()
print("=" * 60)

# Create summary report
summary = {
    "processing_summary": {
        "source_directory": source_dir,
        "target_directory": target_dir,
        "adjustment_rules": {
            "category_id_11_12_13": "decrease by 10",
            "category_id_greater_than_13": "decrease by 7",
            "category_id_other": "no change"
        },
        "results": processing_results,
        "totals": {
            "files_processed": len([r for r in processing_results if r['status'] == 'success']),
            "files_with_errors": len([r for r in processing_results if r['status'] == 'error']),
            "total_adjustments": sum(r['adjustments_made'] for r in processing_results)
        }
    }
}

# Save summary report
summary_path = os.path.join(target_dir, '_category_resolution_summary.json')
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print("Processing completed!")
print(f"📂 Processed files saved in: {target_dir}")
print(f"📊 Summary report saved: {summary_path}")
print(f"🔧 Total category_id adjustments made: {summary['processing_summary']['totals']['total_adjustments']}")

# Display adjustment examples
print("\nAdjustment examples:")
print("  category_id '11' → '1'")
print("  category_id '12' → '2'") 
print("  category_id '13' → '3'")
print("  category_id '14' → '7'")
print("  category_id '20' → '13'")
print("  category_id '5' → '5' (no change)")
