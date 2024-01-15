import sys
import os


def analyse_file(file_path):
    file = open(file_path)
    lines = file.readlines()

    codes_msg_dict = {'S001': "Too long",
                      'S002': "Indentation is not a multiple of four",
                      'S003': "Unnecessary semicolon",
                      'S004': "At least two spaces required before inline comments",
                      'S005': "TODO found",
                      'S006': "More than two blank lines used before this line",
                      }

    def addcodetoline(count, code_no):
        line_no = count + 1
        if line_no in wrong_lines.keys():
            wrong_lines[line_no].append(code_no)
        else:
            wrong_lines[line_no] = [code_no]

    # Less than 79 chars per line
    def s001(lst):
        for count, line in enumerate(lst):
            if len(line) > 79:
                addcodetoline(count, 'S001')

    # Indentation multiple of four
    def s002(lst):
        for count, line in enumerate(lst):
            whitespaces = 0
            # Count indent whitespaces
            for char in line:
                if char == ' ':
                    whitespaces += 1
                else:
                    break
            # Check multiple of four
            if whitespaces % 4 != 0:
                addcodetoline(count, 'S002')

    # Unnecessary semicolon ;
    def s003(lst):
        for count, line in enumerate(lst):
            non_comment_part = line.split('#')[0]
            stack = []
            stack_chars = ('"', "'", ';')
            for char in non_comment_part:
                if char in stack_chars:
                    stack.append(char)
            open_string = False
            for char in stack:
                if char != ';':
                    open_string = not open_string
                if char == ';':
                    if not open_string:
                        addcodetoline(count, 'S003')
                        break

    # Two spaces before inline comments
    def s004(lst):
        for count, line in enumerate(lst):
            if '#' in line and line[0] != '#':
                non_comment_part = line.split('#')[0]
                if non_comment_part[-2:] != '  ':
                    addcodetoline(count, 'S004')

    # TO-DO in comment part, case insensitive
    def s005(lst):
        for count, line in enumerate(lst):
            if '#' in line:
                comment_part = ''
                if line[0] == '#':
                    comment_part = line
                else:
                    comment_part = line.split('#', 1)[1]

                if 'todo' in comment_part.lower():
                    addcodetoline(count, 'S005')

    # Two blank lines preceding code line
    def s006(lst):
        blank_counter = 0
        for count, line in enumerate(lst):
            # If string is blank (falsy), add to counter
            if not line.strip():
                blank_counter += 1
            else:
                if blank_counter > 2:
                    addcodetoline(count, 'S006')
                    blank_counter = 0

    # Analyse
    s001(lines)
    s002(lines)
    s003(lines)
    s004(lines)
    s005(lines)
    s006(lines)

    # Sort wrong_lines
    myKeys = list(wrong_lines.keys())
    myKeys.sort()
    sorted_dict = {i: wrong_lines[i] for i in myKeys}

    # Loop through wrong_lines
    for line, code_list in sorted_dict.items():
        # Loop through their codes
        for code in code_list:
            # Print line, code and code_msg
            print(f'{file_path}: Line {line}: {code} {codes_msg_dict[code]}')

    file.close()


# Recursive, call again when a folder is found
def walkintofolder(path):
    for root, dirs, files in os.walk(path):
        for file_path in files:
            # print(root + file_path)
            analyse_file(f'{root}\\{file_path}')
        for dir_path in dirs:
            walkintofolder(dir_path)


args = sys.argv
path = args[1]

if path[-3:] == ".py":
    analyse_file(path)
else:
    walkintofolder(path)
