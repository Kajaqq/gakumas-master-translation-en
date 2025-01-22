import os
import json
import shutil
import argparse
import sys

import import_db_json
import export_db_json
from csv_json_bridge import write_json, write_csv

def values_to_keys(root_dir, output_type='json'):
    output_dir = "./pretranslate_todo/full_out"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for root, dirs, files in os.walk(root_dir):
        for name in files:
            if not name.endswith(".json"):
                continue
            data = {}
            with open(os.path.join(root, name), 'r', encoding='utf-8') as f:
                orig_data = json.load(f)

            for _, v in orig_data.items():
                data[v] = ""

            output_file = os.path.join(output_dir, name)
            if output_type == 'json':
                write_json(output_file, data)

            elif output_type == 'csv':
                csv_file = output_file.replace('.json', '.csv')
                write_csv(csv_file, data)

            print("Extracted file", name[:-4]+output_type)


def pretranslated_to_kv_files(
        root_dir: str,
        translated_dir: str,
        save_dir="pretranslate_todo/translated_out"
):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for root, dirs, files in os.walk(translated_dir):
        for name in files:
            if not name.endswith("_translated.json"):
                continue
            translated_file = os.path.join(root, name)
            orig_file = os.path.join(root_dir, name[:-16] + ".json")
            save_file = os.path.join(save_dir, name[:-16] + ".json")

            with open(translated_file, 'r', encoding='utf-8') as f:
                translated_data = json.load(f)  # Original file - Japanese

            with open(orig_file, 'r', encoding='utf-8') as f:
                orig_data = json.load(f)  # key:Japanese file

            for k, orig_jp in orig_data.items():
                orig_data[k] = translated_data.get(orig_jp, orig_jp)

            with open(save_file, 'w', encoding='utf-8') as f:
                json.dump(orig_data, f, ensure_ascii=False, indent=4)

            print("Merging files", name)
    print("The merge is complete. \n Please execute import_db_json to import the translation file back.")


def gen_todo(new_files_dir: str):
    """
    Generate untranslated jp: "" file
    """
    old_files_dir = "./data"
    temp_key_en_dir = "./pretranslate_todo/temp_key_en"
    temp_key_jp_dir = "./pretranslate_todo/temp_key_jp"
    todo_out_dir = "./pretranslate_todo/todo"

    if not os.path.isdir(temp_key_en_dir):
        os.makedirs(temp_key_en_dir)
    if not os.path.isdir(temp_key_jp_dir):
        os.makedirs(temp_key_jp_dir)
    if not os.path.isdir(todo_out_dir):
        os.makedirs(todo_out_dir)

    # temp convert a json to key:en
    for root, dirs, files in os.walk(old_files_dir):
        for file in files:
            if file.endswith(".json"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(temp_key_en_dir, file)
                export_db_json.ex_main(input_path, output_path)

    # temp convert a json to key:jp
    for root, dirs, files in os.walk(new_files_dir):
        for file in files:
            if file.endswith(".json"):
                input_path = os.path.join(root, file)
                output_path = os.path.join(temp_key_jp_dir, file)
                export_db_json.ex_main(input_path, output_path)

    # Traverse the new jp file
    for root, dirs, files in os.walk(temp_key_jp_dir):
        for file in files:
            jp_file = os.path.join(root, file)
            en_file = os.path.join(temp_key_en_dir, file)
            out_data = {}

            with open(jp_file, 'r', encoding='utf-8') as f:
                jp_data = json.load(f)

            if not os.path.exists(en_file):
                for _, v in jp_data.items():
                    out_data[v] = ""
            else:
                with open(en_file, 'r', encoding='utf-8') as f:
                    en_data = json.load(f)
                for k, v in jp_data.items():
                    if k not in en_data:
                        out_data[v] = ""

            if out_data:
                todo_file = os.path.join(todo_out_dir, file)
                with open(todo_file, 'w', encoding='utf-8') as f:
                    json.dump(out_data, f, ensure_ascii=False, indent=4)
                print("TODO File", todo_file)


def merge_todo():
    new_files_dir = "./pretranslate_todo/todo/new"  # jp:en files
    old_trans_dir = "./pretranslate_todo/temp_key_en"  # old key:en files
    new_key_jp_dir = "./pretranslate_todo/temp_key_jp"  # key:jp files
    output_dir = "./pretranslate_todo/merged"  # merged key:en files

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # First copy the new key:jp to the output folder
    for root, dirs, files in os.walk(new_key_jp_dir):
        for file in files:
            if file.endswith(".json"):
                shutil.copyfile(os.path.join(root, file), os.path.join(output_dir, file))

    # Merge old translations
    for root, dirs, files in os.walk(old_trans_dir):
        for file in files:
            if file.endswith(".json"):
                old_key_en_file = os.path.join(root, file)  # root = old version key:en
                new_key_jp_file = os.path.join(output_dir, file)  # output_dir = new version key:jp

                with open(old_key_en_file, 'r', encoding='utf-8') as f:
                    old_key_en_data: dict = json.load(f)
                if os.path.exists(new_key_jp_file):
                    with open(new_key_jp_file, 'r', encoding='utf-8') as f:
                        new_key_jp_data = json.load(f)
                else:
                    new_key_jp_data = {}

                for k, v in old_key_en_data.items():
                    new_key_jp_data[k] = v

                with open(new_key_jp_file, 'w', encoding='utf-8') as f:
                    json.dump(new_key_jp_data, f, ensure_ascii=False, indent=4)

    pretranslated_to_kv_files(output_dir, new_files_dir, output_dir)

    if input("If you want to import the db to json, please enter 1:") == "1":
        import_db_json.main("./gakumasu-diff/json", output_dir, "data")
        print("Files exported into data folder")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gen_todo', action='store_true')
    parser.add_argument('--merge', action='store_true')
    parser.add_argument('--import_back',action='store_true')
    parser.add_argument('--export', action='store_true')
    parser.add_argument('--export_csv',action='store_true')
    args = parser.parse_args()


    if len(sys.argv)==1:
        do_idx = input("[1] Export all to files to be translated\n"
                       "[2] Compare and update to generate todo files\n"
                       "[3] Convert translation files (jp:en) back to key-value json\n"
                       "[4] Merge the translated todo files back to plugin json\n"
                       "Please select an operation: ")
    elif args.gen_todo:
        gen_todo("gakumasu-diff/json")
        return
    elif args.merge:
        do_idx = "4"
    elif args.import_back:
        pretranslated_to_kv_files('exports','pretranslate_todo/full_out')
        return
    elif args.export:
        values_to_keys('exports')
        return
    elif args.export_csv:
        values_to_keys('exports',output_type='csv')
        return
    else:
        raise RuntimeError("Invalid Arguments.")

    if do_idx == "1":
        values_to_keys(input("Input export folder(or press enter for default): ") or "exports")

    elif do_idx == "2":
        gen_todo(input("Input gakumasu_diff_to_json folder(or press enter for default): ") or "gakumasu-diff/json")

    elif do_idx == "3":
        pretranslated_to_kv_files(
            root_dir=input("Input export folder(or press enter for default): ") or "exports",
            translated_dir=input("Input translated(jp:en format) folder(or press enter for default): ") or "pretranslate_todo/full_out"
        )

    elif do_idx == "4":
        merge_todo()


if __name__ == '__main__':
    main()
