import json
import os


def compare_json_folders(folder1, folder2):
    """
    Compare the contents of JSON files in two folders for consistency.

    Args:
    folder1 (str): The path to the first folder.
    folder2 (str): The path to the second folder.

    Returns:
    dict: Returns a dictionary containing the comparison results:
    - "matched": A list of files with the same content in the two folders.
    - "mismatched": A list of files with different content.
    - "missing_in_folder2": A list of files that exist in folder1 but not in folder2.
    - "missing_in_folder1": A list of files that exist in folder2 but not in folder1.
    """
    result = {
        "matched": [],
        "mismatched": [],
        "missing_in_folder2": [],
        "missing_in_folder1": []
    }

    # Get the JSON file names in two folders
    files1 = {f for f in os.listdir(folder1) if f.endswith('.json')}
    files2 = {f for f in os.listdir(folder2) if f.endswith('.json')}

    # Find files that exist only in one folder
    result["missing_in_folder2"] = list(files1 - files2)
    result["missing_in_folder1"] = list(files2 - files1)

    # Compare the contents of the common files in two folders
    common_files = files1 & files2

    for file_name in common_files:
        path1 = os.path.join(folder1, file_name)
        path2 = os.path.join(folder2, file_name)

        try:
            with open(path1, 'r', encoding='utf-8') as f1, open(path2, 'r', encoding='utf-8') as f2:
                json1 = json.load(f1)
                json2 = json.load(f2)

            if json1 == json2:
                result["matched"].append(file_name)
            else:
                result["mismatched"].append(file_name)
        except Exception as e:
            print(f"Error comparing {file_name}: {e}")

    return result


folder1 = input("Folder 1: ")
folder2 = input("Folder 2: ")
comparison_result = compare_json_folders(folder1, folder2)

print("Matched files:", comparison_result["matched"])
print("Mismatched files:", comparison_result["mismatched"])
print("Missing in folder2:", comparison_result["missing_in_folder2"])
print("Missing in folder1:", comparison_result["missing_in_folder1"])
# Mismatched files: ['ProduceChallengeSlot.json', 'ProduceNavigation.json', 'ProduceCardCustomize.json']
