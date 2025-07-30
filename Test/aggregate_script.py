import json
import os

# Define the JSON files to aggregate
json_files = [
    'categories.json',
    'change_requests.json',
    'companies.json',
    'departments.json',
    'incident_attachments.json',
    'incident_comments.json',
    'incident_history.json',
    'incident_knowledge.json',
    'incident_sla.json',
    'incidents.json',
    'knowledge_base.json',
    'sla.json',
    'subcategories.json',
    'surveys.json',
    'tasks.json',
    'users.json'
]

# Define directories
original_dir = 'data'
offset_dir = 'new_data_offset'
aggregated_dir = 'data_aggregated'

# Create aggregated directory if it doesn't exist
os.makedirs(aggregated_dir, exist_ok=True)

print("Starting data aggregation...")
print("=" * 50)

# Process each JSON file
for filename in json_files:
    original_path = os.path.join(original_dir, filename)
    offset_path = os.path.join(offset_dir, filename)
    aggregated_path = os.path.join(aggregated_dir, filename)
    
    # Check if both files exist
    if not os.path.exists(original_path):
        print(f"⚠️  Original file not found: {original_path}")
        continue
    
    if not os.path.exists(offset_path):
        print(f"⚠️  Offset file not found: {offset_path}")
        continue
    
    try:
        # Read original data
        with open(original_path, 'r') as f:
            original_data = json.load(f)
        
        # Read offset data
        with open(offset_path, 'r') as f:
            offset_data = json.load(f)
        
        # Aggregate data (original + offset)
        aggregated_data = {}
        
        # Add original data first
        for key, value in original_data.items():
            aggregated_data[key] = value
        
        # Add offset data
        for key, value in offset_data.items():
            aggregated_data[key] = value
        
        # Save aggregated data
        with open(aggregated_path, 'w') as f:
            json.dump(aggregated_data, f, indent=2)
        
        # Print summary
        original_count = len(original_data)
        offset_count = len(offset_data)
        total_count = len(aggregated_data)
        
        print(f"✅ {filename}")
        print(f"   Original: {original_count} records")
        print(f"   Offset:   {offset_count} records")
        print(f"   Total:    {total_count} records")
        print()
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {str(e)}")
        print()

print("=" * 50)
print("Data aggregation completed!")
print(f"Aggregated files saved in: {aggregated_dir}")

# Create a summary report
summary = {
    "aggregation_summary": {
        "source_directories": {
            "original": original_dir,
            "offset": offset_dir
        },
        "output_directory": aggregated_dir,
        "files_processed": []
    }
}

for filename in json_files:
    aggregated_path = os.path.join(aggregated_dir, filename)
    if os.path.exists(aggregated_path):
        with open(aggregated_path, 'r') as f:
            data = json.load(f)
            summary["aggregation_summary"]["files_processed"].append({
                "filename": filename,
                "total_records": len(data)
            })

# Save summary report
summary_path = os.path.join(aggregated_dir, '_aggregation_summary.json')
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"📊 Summary report saved: {summary_path}")
