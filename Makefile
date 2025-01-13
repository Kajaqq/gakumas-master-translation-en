update:
	cd gakumasu-diff/orig && git fetch && git checkout origin/main
	python scripts/gakumasu_diff_to_json.py

export-db:
	python scripts/export_db_json.py
	python scripts/pretranslate_process.py --export

gen-todo:
	python scripts/pretranslate_process.py --gen_todo

merge:
	python scripts/pretranslate_process.py --merge
