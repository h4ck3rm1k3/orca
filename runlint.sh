
cat files.txt | PYTHONPATH=src xargs ~/.local/bin/pylint --output-format=parseable
