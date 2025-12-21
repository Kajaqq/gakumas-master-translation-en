import json
import os
import sys

# Special rules for handling special cases of certain fields
# Format: {"filename": {"field name": {"rule"} }}
special_rules = {
    "ProduceStory.json": {
        "produceEventHintProduceConditionDescriptions": {
            "is_empty": True,  # Replace the field with an empty array if it is a single empty string array
        }
    },
    "Tutorial.json": {
        "texts": {
            "is_empty": True,  # Replace the field with an empty array if it is a single empty string array
        }
    },
    "ConditionSet..json": {
        "description": {
            "is_empty": True,  # Replace the field with an empty array if it is a single empty string array
        }
    },
    "IdolCardSkin.json": {
        "name": {
            "is_empty": True,  # Replace the field with an empty array if it is a single empty string array
        }
    },
}


def fill_back_translations(data_obj, primary_keys, trans_map, filename=None):
    """
    data_obj is a record of the original localized data;
    trans_map is the { fullKey: translatedValue } translated by third-party software
    Match based on baseKey (composed of primary key) + path, and fill the translation back into data_obj.
    """

    # Get baseKey first
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

    # Traverse data_obj, if key= base Key|xxx is found, replace its content
    def traverse(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_prefix = prefix + "." + k if prefix else k
                if isinstance(v, str):
                    fullKey = baseKey + "|" + new_prefix
                    if fullKey in trans_map:
                        obj[k] = trans_map[fullKey]
                elif isinstance(v, list):
                    fullKey = baseKey + "|" + new_prefix
                    if fullKey in trans_map:
                        trans_data = trans_map[fullKey]
                        if trans_data.startswith("[LA_F]"):
                            remaining = trans_data[len("[LA_F]"):]
                            if remaining == "":
                                obj[k] = []
                            else:
                                list_data = remaining.split("[LA_N_F]")
                                if filename in special_rules and k in special_rules[filename]:
                                    rule = special_rules[filename][k]
                                    if "is_empty" in rule and len(list_data) == 1 and list_data[0] == "":
                                        obj[k] = []
                                    else:
                                        obj[k] = list_data
                                else:
                                    obj[k] = list_data
                        else:
                            traverse(v, new_prefix)
                    else:
                        traverse(v, new_prefix)
                elif isinstance(v, dict):
                    traverse(v, new_prefix)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                new_prefix = prefix + f"[{idx}]"
                if isinstance(item, dict) or isinstance(item, list):
                    traverse(item, new_prefix)

    traverse(data_obj)


def import_main(base_json, translated_json, output_json):
    if not os.path.isfile(base_json):
        print(f"Cannot find base file: {base_json}")
        sys.exit(1)
    if not os.path.isfile(translated_json):
        print(f"Cannot find translation file: {translated_json}")
        sys.exit(1)

    with open(base_json, "r", encoding="utf-8") as f1:
        root = json.load(f1)

    with open(translated_json, "r", encoding="utf-8") as f2:
        trans_map = json.load(f2)  # {"key": "translated text", ...}

    if "rules" not in root or "primaryKeys" not in root["rules"]:
        print("Missing rules.primaryKeys, does your json have proper structure?")
        sys.exit(1)

    primary_keys = root["rules"]["primaryKeys"]
    if "data" not in root or not isinstance(root["data"], list):
        print("The data array is missing ,does your json have proper structure?")
        sys.exit(1)

    # Traverse the data array and fill in the translations one by one
    for row in root["data"]:
        fill_back_translations(row, primary_keys, trans_map)

    # Write new json
    with open(output_json, "w", encoding="utf-8") as out:
        json.dump(root, out, ensure_ascii=False, indent=2)

    print(f"Merge completed: {output_json}")


def main(base_dir, translated_dir, output_dir="merged"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(translated_dir):
        for file in files:
            if file.endswith(".json"):
                translated_json = os.path.join(root, file)
                base_json = os.path.join(base_dir, file)
                output_json = os.path.join(output_dir, file)
                import_main(base_json, translated_json, output_json)


if __name__ == "__main__":
    main(
        base_dir=sys.argv[1] if len(sys.argv) > 1  else "gakumasu-diff/json",
        translated_dir=sys.argv[2] if len(sys.argv) > 2 else "pretranslate_todo/translated_out"
    )
