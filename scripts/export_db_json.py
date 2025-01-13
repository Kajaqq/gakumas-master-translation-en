import json
import sys
import os
import re
import string

def path_normalize_for_pk(path_str: str) -> str:
    """
    Converts something like 'produceDescriptions[0].produceDescriptionType'
    to 'produceDescriptions.produceDescriptionType'
    removing only the [number] layer so it matches primaryKeys.
    """
    return re.sub(r"\[\d+\]", "", path_str)

def check_need_export(v: str) -> bool:
    if not v:
        return False

    # Define the allowed character set
    allowed_chars = string.ascii_letters + string.digits + string.punctuation + " "

    # Check if all characters are in the allowed character set
    for char in v:
        if char not in allowed_chars:
            return True

    return False


def collect_translatable_text(data_obj, primary_keys):
    """
    Traverse data_obj (i.e. a single record) and collect the text information that needs to be translated.
    Return a dictionary of the form { fullKey: textValue, ... }.
    """

    result = {}

    # 1) Store primaryKeys in a set for quick judgment later
    pk_set = set(primary_keys)

    # 2) Build baseKey (put all primary key values together)
    pk_parts = []
    for pk in primary_keys:
        if "." not in pk:
            val = data_obj.get(pk, "")
            pk_parts.append(str(val))
        else:
            top_level, sub_field = pk.split(".", 1)
            top_val = data_obj.get(top_level, None)
            if isinstance(top_val, list) and len(top_val) > 0 and isinstance(top_val[0], dict):
                sub_val = top_val[0].get(sub_field, "")
                pk_parts.append(str(sub_val))
            elif isinstance(top_val, dict):
                sub_val = top_val.get(sub_field, "")
                pk_parts.append(str(sub_val))
            else:
                pk_parts.append("")

    baseKey = "|".join(pk_parts)

    # 3) Recursively traverse to find non-primary key, non-empty string fields
    def traverse(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_prefix = prefix + "." + k if prefix else k
                if isinstance(v, str):
                    # If the string is empty, skip it
                    if not check_need_export(v):
                        continue
                    # Process array index => produceDescriptions[0].xxx -> produceDescriptions.xxx
                    normalized_path = path_normalize_for_pk(new_prefix)
                    # If it is pk, skip
                    if normalized_path not in pk_set:
                        fullKey = baseKey + "|" + new_prefix
                        result[fullKey] = v
                elif isinstance(v, list):
                    if (len(v) > 0) and (not isinstance(v[0], str)):
                        traverse(v, new_prefix)
                    else:
                        new_v = "[LA_N_F]".join(v)
                        new_v = f"[LA_F]{new_v}"
                        # If the string is empty, skip it
                        if not check_need_export(new_v):
                            continue
                        # Process array index => produceDescriptions[0].xxx -> produceDescriptions.xxx
                        normalized_path = path_normalize_for_pk(new_prefix)
                        # If it is pk, skip
                        if normalized_path not in pk_set:
                            fullKey = baseKey + "|" + new_prefix
                            result[fullKey] = new_v

                elif isinstance(v, dict):
                    traverse(v, new_prefix)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                new_prefix = prefix + f"[{idx}]"
                if isinstance(item, (dict, list)):
                    traverse(item, new_prefix)

    traverse(data_obj)
    return result

def ex_main(input_json, output_json):
    if not os.path.isfile(input_json):
        print(f"Input file not found: {input_json}")
        sys.exit(1)

    with open(input_json, "r", encoding="utf-8") as f:
        root = json.load(f)

    if "rules" not in root or "primaryKeys" not in root["rules"]:
        print("Missing rules.primaryKeys, may not be the expected structure")
        sys.exit(1)

    primary_keys = root["rules"]["primaryKeys"]
    if "data" not in root or not isinstance(root["data"], list):
        print("The data array is missing and may not be the expected structure.")
        sys.exit(1)

    export_dict = {}
    for row in root["data"]:
        row_dict = collect_translatable_text(row, primary_keys)
        export_dict.update(row_dict)

    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(export_dict, out, ensure_ascii=False, indent=2)

    print(f"Export completed: {output_json} (total {len(export_dict)} entries)")

def main():
    orig_dir = sys.argv[1] if len(sys.argv) > 1 else "gakumasu-diff/json"
    if not os.path.isdir("./exports"):
        os.mkdir("./exports")

    for root, dirs, files in os.walk(orig_dir):
        for file in files:
            if file.endswith(".json"):
                input_path = os.path.join(root, file)
                output_path = os.path.join("./exports", file)
                ex_main(input_path, output_path)


if __name__ == "__main__":
    main()
