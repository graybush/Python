"""
copyLess will take a directory to be copied and looks recursively for files.
If any files are found that after being copied will have paths greater than 255 characters,
the files will be renamed by striping the shows title from the file name.
"""

import os
import re
import shutil
import sys


def copier(to_copy_list, copy_to):
    """
    checks to see if the path exists, if it does it copies files into the directory
    if the path doesnt exist it makes the dir then performs the copy
    """
    for copy_params in to_copy_list:
        if os.path.exists(copy_to):
            if os.path.exists(copy_params[1]):
                shutil.copy2(copy_params[0], copy_params[1] + '\\' + copy_params[2])
            else:
                os.mkdir(copy_params[1])
                shutil.copy2(copy_params[0], copy_params[1] + '\\' + copy_params[2])
        else:
            os.mkdir(copy_to)
            os.mkdir(copy_params[1])
            shutil.copy2(copy_params[0], copy_params[1] + '\\' + copy_params[2])

    print('\nFiles copied ... \n')
    sorted_list = []
    for copy_params in to_copy_list:
        sorted_list.append(copy_params[2])
    sorted_list = sorted(sorted_list)
    for copy_params in sorted_list:
        print(copy_params)


def file_len(file_path, copy_to, copy_from):
    """
    file_len checks the fully qualified path for paths over 255 characters
    """
    file_path_len = len(file_path)
    copy_to_len = len(copy_to)
    copy_from_len = len(copy_from)
    total = file_path_len - copy_from_len + copy_to_len
    if total > 255:
        return True
    else:
        return False


def return_contents(path, args):
    """
    return_contents looks returns a list (file_list) with all of the directory's files
    remove files with following file extensions: par2
    """
    if args == '--copy':
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".par2"):
                    os.unlink(root + '\\' + file)
                else:
                    file_list.append(os.path.join(root, file))
        return file_list

    if args == '--rename':
        file_list = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".par2"):
                    os.unlink(root + '\\' + file)
                else:
                    a = (root, file)
                    file_list.append(a)
        return file_list


def prepare2copy(file_list, copy_to, copy_from):
    """
    prepare2copy creates a list of files to be copied
    if the fully qualified path length is greater than 255 it will first rename the file
    """
    to_copy_list = []
    for file in file_list:
        if not file_len(file, copy_to, copy_from):
            # If the fully qualified path length is less than 255 copy it
            filename = os.path.split(file)
            a = (file, copy_to + filename[0][len(copy_from):], filename[1])
            to_copy_list.append(a)
        elif file_len(file, copy_to, copy_from):
            # If the fully qualified path length is greater than 255 rename then copy it
            filename = os.path.split(file)
            match = re.search(r'\d\d\d\d.*', filename[1])
            print('\n' + match.group(0))
            user_input = input('\n Approve rename? ')
            user_input = user_input.lower()
            if user_input == 'y':
                # Getting approval for the file rename
                b = (file, copy_to + filename[0][len(copy_from):], match.group(0))
                to_copy_list.append(b)
    return to_copy_list


def prepare2rename(file_list):
    """
    prepare2rename renames obfuscated files using the parent directory as the file name
    """
    to_rename_list = []
    for file in file_list:
        file_path = file[0] + '\\' + file[1]
        a = (file_path, file[0] + file[0][len(os.path.dirname(os.path.dirname(file_path))):] + file[1][-4:], file[0])
        to_rename_list.append(a)
    return to_rename_list


def renamer(to_rename_list):
    """
    renames the files in the directory with the directory name
    """
    for rename_params in to_rename_list:
        os.rename(rename_params[0], rename_params[1])
    print('\nFiles renamed ... \n')
    to_rename_list = sorted(to_rename_list, key=lambda x: x[1])
    for rename_params in to_rename_list:
        path_length = len(rename_params[2])
        print(rename_params[0][path_length:] + ' >>> ' + rename_params[1][path_length:] + '\n')


def main():
    args = sys.argv[1:]

    if not args:
        print("usage [--copy copy_from copy_to][--rename copy_from]")
        sys.exit(1)

    if args[0] == '--copy':
        print(args[2])
        copy_from = args[1]
        copy_to = args[2]
        file_list = return_contents(copy_from, args[0])
        to_copy_list = prepare2copy(file_list, copy_to, copy_from)
        copier(to_copy_list, copy_to)

    if args[0] == '--rename':
        rename_dir = args[1]
        file_list = return_contents(rename_dir, args[0])
        to_rename_list = prepare2rename(file_list)
        renamer(to_rename_list)


if __name__ == '__main__':
    main()
