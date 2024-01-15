# python-code-analyzer
 Python script to run basic format validation on .py files in a directory tree.


Run from cmd and pass the folder or file path as an argument:

```python code-analyzer folder_or_file_path```


The script checks for 6 format errors in lines:

-S001: Longer than 79 characters.

-S002: Indentation is not a multiple of four.

-S003: Unnecessary semicolon.

-S004: Less than two spaces before inline comments.

-S005: Pending TODO.

-S006: More than two blank lines used before this line.