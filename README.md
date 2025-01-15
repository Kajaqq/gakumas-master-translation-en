# gakumas-master-translation-en

## WARNING: The Chinese version isn't up to date with this repo
[简体中文](README_CN.md) | English


# Updating with Scripts

### Warning: This process differs significantly from the manual process described below and wont provide the same results
#### For Windows use the .bat files instead of make
- Use `make update` to update the MasterDB (`orig` and `json`) file from gakumas-diff
- Use `make export-db` to export the database files - this should only be run once to generate origin files
- Use `make gen-todo` to generate files to be translated into the `pretranslate_todo/todo` folder.
  - Manually copy the files from `pretranslate_todo/todo` into `gakumas-generic-strings-translation/working/todo`. Then, run `make pretranslate` in the `gakumas-generic-strings-translation`.
  - After translation is complete, copy the files from `gakumas-generic-strings-translation/working/new` into `pretranslate_todo/todo/new`. If the `new` folder does not exist, create it manually.
- Use `make merge` to merge the files from `pretranslate_todo/todo/new` into `data`.
- Once all processes are completed, please manually clear the `pretranslate_todo` folder.



# Manual Execution

## Manual Translation Workflow
1. Run `update.bat` to get the newest data and convert the YAML files from the `gakumasu-diff` repository into JSON files readable by the plugin. At this stage, the JSON contains the original Japanese text.
2. Run `export_db_json.py` to convert the generated JSON into the `key: original Japanese text` format.
3. Execute `pretranslate_process.py` and select option `1` or add `--export` to convert `key: original Japanese text` into `Japanese: ""` format for pre-translation.'\
3a. **The 2 steps above can also be done at once with `export-db.bat`**
4. Perform translation manually to obtain a `Japanese: English` file, append `_translated` to the end of the file like `Chara_translated.json`
5. Run `pretranslate_process.py` again and select option `3` or add `--import_back` to convert the translated `Japanese: English` file into the `key: English` format.
6. Finally, execute `import_db_json.py` to convert the `key: English` file into a JSON file readable by the plugin.

## Translation using Starlit Translator
1. Run `update.bat` to get the newest data and convert the YAML files from the `gakumasu-diff` repository into JSON files readable by the plugin. At this stage, the JSON contains the original Japanese text.
2. Run `export_db_json.py` to convert the generated JSON into the `key: original Japanese text` format.
3. Run `pretranslate_process.py --export_csv` to get `jp:en` csv files, this will generate files in the `pretranslate_todo/full_out` folder'\
3a. **The 2 steps above can also be done at once with `export-db-csv.bat`**
4. Perform translation using Starlit Translator, after translating copy the data back to the `pretranslate_todo/full_out`
5. Run `csv_to_json.bat` or `csv_json_bridge.py --mass_convert` to convert csv files back to json.
6. Run `pretranslate_process.py` again and select option `3` or add `--import_back` to convert the translated `Japanese: English` file into the `key: English` format.
7. Finally, execute `import_db_json.py` to convert the files into a JSON file readable by the plugin.

## Updating Based on Old Files

1. Generate the `todo` files by running `pretranslate_process.py` and selecting option `2` or adding `--gen-todo`. The old translation data must be located in the `data` directory, and new files are generated using `gakumasu_diff_to_json`.
2. After pre-translation is complete, place the new files into `todo/new` and run `pretranslate_process.py`, selecting option `4` or adding `--merge`.

## Converting json <---> CSV
- This toolkit supports seamless conversion for the `origin:translated` files between CSV and json 
- You can set the output of `pretranslate_process.py` by running it with `--export` for json and `--export_csv` for csv
- You can also change the formats with `csv_json_bridge.py input output` where input and output can be a csv/json pair or a json/csv pair.
- Be aware though that `pretranslate_process.py` will only accept back a json file so every csv file will need to be converted back into .json format
- For mass converting csv back to json use `csv_to_json.bat` or `csv_json_bridge.py --mass_convert`
