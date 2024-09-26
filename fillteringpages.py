import json

def sort_json_by_index(input_file, output_file):
    # Read the JSON file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Sort the data based on the "Index" field
    # Convert "Index" to integer for proper numerical sorting
    sorted_data = sorted(data, key=lambda x: int(x['Index']))
    
    # Write the sorted data back to a new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=2)

# Use the function
input_file = '/home/vithamas/Desktop/Real-estate scarping/all_real_estate_projects.json'  # Replace with your input file name
output_file = 'sorted_real_estate_projects.json'  # Name of the output file

sort_json_by_index(input_file, output_file)

print(f"Sorted data has been written to {output_file}")