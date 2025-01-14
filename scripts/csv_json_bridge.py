import json
import csv
import sys
import pathlib

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

def write_csv(filepath, data, header=CSV_HEADER):
    """Writes data to a CSV file.

    Args:
        filepath (str): The path to the CSV file.
        data (list): A list of dictionaries representing the rows.
        header (list): A list of strings representing the header.

    Raises:
        IOError: If there is an error writing to the file.
    """
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)
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

if __name__ == '__main__':
    first_file = sys.argv[1] if len(sys.argv) > 1 else None
    second_file = sys.argv[2] if len(sys.argv) > 2 else None
    first_file_extension = pathlib.Path(first_file).suffix
    second_file_extension = pathlib.Path(second_file).suffix
    if first_file_extension != second_file_extension:
        if first_file_extension == '.json' and second_file_extension == '.csv':
            json_to_csv(first_file, second_file)
        elif first_file_extension == '.csv' and second_file_extension == '.json':
            csv_to_json(first_file, second_file)
    else:
        raise ValueError(f"The provided files have the same extensions!")
