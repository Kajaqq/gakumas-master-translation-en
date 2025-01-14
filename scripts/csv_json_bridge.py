import json
import csv
import sys
import pathlib
from concurrent.futures import ThreadPoolExecutor

CSV_HEADER = ['source', 'translatedstr']

def read_json(filepath):
    """Reads a JSON file and returns its content as a dictionary.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict: The content of the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not a valid JSON.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError:
        raise FileNotFoundError(f"JSON file not found at {filepath}")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Invalid JSON format in {filepath}")

def write_csv(filepath, data:dict, header=None):
    """Writes data to a CSV file.

    Args:
        filepath (str): The path to the CSV file.
        data (dict): A list of dictionaries representing the rows.
        header (list): A list of strings representing the header.

    Raises:
        IOError: If there is an error writing to the file.
    """
    if header is None:
        header = CSV_HEADER
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csv_data:
            writer = csv.writer(csv_data)
            writer.writerow(header)
            for key, value in data.items():
                writer.writerow([key, value])
    except IOError as e:
        raise IOError(f"Error writing to CSV file {filepath}: {e}")

def read_csv(filepath):
    """Reads a CSV file and returns its content as a list of dictionaries.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries representing the rows.

    Raises:
        FileNotFoundError: If the file does not exist.
        csv.Error: If there is an error parsing the CSV.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found at {filepath}")
    except csv.Error as e:
        raise csv.Error(f"Error parsing CSV file {filepath}: {e}")

def write_json(filepath, data):
    """Writes data to a JSON file.

    Args:
        filepath (str): The path to the JSON file.
        data (dict): The data to write.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        raise IOError(f"Error writing to JSON file {filepath}: {e}")

def json_to_csv(json_filepath, csv_filepath):
    """Converts a JSON file to a CSV file, handling empty values.

    Args:
        json_filepath (str): The path to the input JSON file.
        csv_filepath (str): The path to the output CSV file.
    """
    data = read_json(json_filepath)
    csv_data = [{'source': key, 'translatedstr': value} for key, value in data.items()]
    write_csv(csv_filepath, csv_data, CSV_HEADER)

def csv_to_json(csv_filepath, json_filepath):
    """Converts a CSV file to a JSON file, handling missing 'translatedstr' and empty values.

    Args:
        csv_filepath (str): The path to the input CSV file.
        json_filepath (str): The path to the output JSON file.
    """
    data = read_csv(csv_filepath)
    json_data = {}
    for row in data:
        if 'translatedstr' in row:
            json_data[row['source']] = row['translatedstr']
        else:
            json_data[row['source']] = ''  # Handle missing 'translatedstr' as empty string
    write_json(json_filepath, json_data)

def mass_csv_to_json(csv_folder, json_folder=None):
    """
    Converts all CSV files in a folder to JSON files.

    Args:
        csv_folder (str): Path to the folder containing CSV files.
        json_folder (str, optional): Path to the folder where JSON files will be saved.
                                     If None, uses the same folder as csv_folder.
    """
    csv_folder_path = pathlib.Path(csv_folder)
    json_folder_path = pathlib.Path(json_folder) if json_folder else csv_folder_path

    if not csv_folder_path.is_dir():
        raise ValueError(f"The provided CSV folder path is not a directory: {csv_folder}")

    csv_files = list(csv_folder_path.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {csv_folder}")
        return

    with ThreadPoolExecutor() as executor:
        for csv_file in csv_files:
            json_file = json_folder_path / csv_file.with_suffix(".json").name
            print(f'Converting {csv_file} to JSON...')
            executor.submit(csv_to_json, str(csv_file), str(json_file))

def main():
    """
    Main function to handle command line arguments and perform file conversion.
    """
    if len(sys.argv) > 1:
        if sys.argv[1] == "--mass_convert":
            input_folder = sys.argv[2] if len(sys.argv) > 2 else "./pretranslate_todo/full_out"
            output_folder = sys.argv[3] if len(sys.argv) > 3 else None
            mass_csv_to_json(input_folder, output_folder)
        else:
            first_file = pathlib.Path(sys.argv[1])
            second_file = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else None

            if not first_file.exists():
                raise FileNotFoundError(f"The first file does not exist: {first_file}")
            if second_file and not second_file.exists():
                raise FileNotFoundError(f"The second file does not exist: {second_file}")

            if second_file and first_file.suffix != second_file.suffix:
                if first_file.suffix == ".json" and second_file.suffix == ".csv":
                    json_to_csv(str(first_file), str(second_file))
                elif first_file.suffix == ".csv" and second_file.suffix == ".json":
                    csv_to_json(str(first_file), str(second_file))
                else:
                    raise ValueError("Invalid file combination for conversion.")
            else:
                raise ValueError("The provided files have the same extensions or second file is not provided.")
    else:
        print("No arguments provided. Please provide file paths or --mass_convert flag.")

if __name__ == "__main__":
    main()
    pass
