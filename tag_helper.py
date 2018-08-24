"""

Helper function to assist the tagging process of the
publications

If the folder structure is like this:

webpages/1/xxx.html
          /xxx.tag.json
          /xxx.txt

webpages/2/xxx.html
          /xxx.tag.json
          /xxx.txt

...

When tagging the publication for webpage 2,
this file should be placed into the folder of webpages/2/

webpages/2/xxx.html
          /xxx.tag.json
          /xxx.txt
          /tag_helper.py

Run this program with:
python tag_helper.py

Please use python 3, instead of python 2.
run "python --version" to check the version of python

environment setup:
pip install chardet

"""
import json
import chardet
import copy
import os
import sys


# def detect_encodings(filepath):
#     """filepath must exists"""
#     with open(filepath, 'rb') as fin:
#         content = fin.read()
#         results = chardet.detect(content)
#     return results['encoding']


def detect_encodings(filepath):
    """filepath must exists

    A detecting function with utf-8 first strategy.
    It will try to open the file with uft-8 encoding.
    If not utf-8, it will try to use chardet to detect
    encoding of txt file in the same folder.
    If fail, then it will detect encoding of the file itself.
    We use this strategy because the result given by chardet
    on Json file is not reliable.

    This function only works on this project, because there
    are some assumptions in this function:
    (1) folder structure, file with the same name.
    (2) txt file are almost all utf-8, because of generating process
    """

    def naive_detect():
        with open(filepath, 'rb') as fin:
            content = fin.read()
            results = chardet.detect(content)
        return results['encoding']

    try:
        with open(filepath, encoding='utf-8') as fin:
            fin.read()
        return 'utf-8'
    except Exception as e:
        pass

    try:
        if filepath[-4:] == '.txt':
            txt_file_path = filepath
        else:
            head, tail = os.path.split(filepath)
            filename = tail.split('.')[0]
            txt_file_path = os.path.join(head, filename + '.txt')
            return naive_detect(txt_file_path)
    except Exception as e:
        pass

    return naive_detect(filepath)


def construct_text_for_publication(
    input_lines,
    publication_start_line,
    num_of_lines_per_publication
):
    if num_of_lines_per_publication <= 0:
        print('wrong num_of_lines_per_publication, exiting')
        exit(1)

    if num_of_lines_per_publication == 1:
        text = input_lines[publication_start_line].strip()
        return text, [publication_start_line]

    else:
        text = ''
        publications_lines = []
        for i in range(num_of_lines_per_publication):
            text += input_lines[publication_start_line + i]
            publications_lines.append(publication_start_line + i)
        return text.strip(), publications_lines


def publication_tag_helper(
        page_text_path,
        list_of_line_num,
        json_file_path,
        overiding_mode=True,
        num_of_lines_per_publication=1):

    file_encoding = detect_encodings(page_text_path)
    with open(page_text_path, 'r', encoding=file_encoding) as fin:
        lines = fin.readlines()
    pure_lines = ['first_line_place_holder']
    for line in lines:
        pure_lines.append(line)

    file_encoding = detect_encodings(json_file_path)
    with open(json_file_path, 'r', encoding=file_encoding) as fin_json:
        data = json.load(fin_json)

    publication_dict = {}
    publication_dict['text'] = 'PLACEHOLDER'
    publication_dict['line_num'] = 'PLACEHOLDER'

    if overiding_mode:
        data['publications'].clear()

    for line_num in list_of_line_num:
        # text = pure_lines[line_num]
        text, pub_lines = construct_text_for_publication(
            pure_lines,
            line_num,
            num_of_lines_per_publication)
        tmp_publication_dict = copy.deepcopy(publication_dict)
        tmp_publication_dict['line_num'] = pub_lines
        tmp_publication_dict['text'] = text

        data['publications'].append(tmp_publication_dict)

    with open(json_file_path, 'w', encoding='utf-8') as fout_json:
        json.dump(data, fout_json, indent=2, sort_keys=True)


def main():

    PY3 = sys.version_info[0] == 3
    if not PY3:
        print('please use python 3 to run the program, exiting...')
        exit(1)

    try:
        files = os.listdir('.')
        filename = None
        ext = '.tag.json'
        length = len(ext)
        for f in files:
            if len(f) > length and f[-length:] == ext:
                filename = f[:-length]
                break
        if filename is None:
            print('\ncheck xxx.tag.json is present in the current folder')
            print('error, exiting...')
            exit(1)
    except Exception as e:
        print(e)
        print("""This file must be placed into the folder
that contains each individual webpage""")
        print("Exiting")
        exit(1)
    print(filename)

    page_text_path = filename + '.txt'
    page_html_path = filename + '.html'
    json_file_path = filename + '.tag.json'

    if os.path.exists(json_file_path) and os.path.exists(page_text_path):
        print('page_text_path', page_text_path)
        print('page_html_path', page_html_path)
        print('json_file_path', json_file_path)
        print()
    else:
        print("""page_text or page_html file do not exists,
            this tag_helper needs to be put in the same folder as
            the other files.
            """)
        exit(1)

    print("""\nsave the tagged json file before running this program!!!\n""")

    print("""Please choose the mode:
(1)Enter list of lines numbers
(2)Enter starting line number, end line number (inclusive), and step value""")

    number = input()
    if number == '1':
        print('user choose mode 1')
        print("""please enter all the line numbers in one line,
separated by spaces""")

        line_num_lists = [int(x) for x in input().split()]

    elif number == '2':
        print()
        print('user choose mode 2')
        print('please enter the begin line number')
        begin_num = int(input())
        print('please enter the end line number (inclusive)')
        end_num = int(input())
        print('please enter the step number')
        step = int(input())

        line_num_lists = []
        for i in range(begin_num, end_num + 1, step):
            line_num_lists.append(i)

    else:
        print('wrong code, exit')
        exit(1)

    print("""\nhow many lines each publication occupies, 1 is default,
press Enter for 1. Enter other number if each publication
occupies more than one line""")
    num_of_lines_per_publication = 1
    answer = input()
    if answer.strip() != '':
        try:
            num_of_lines_per_publication = int(answer)
        except Exception as e:
            print("wrong input, program exiting...")

    print('\n' + str(num_of_lines_per_publication) +
          ' line(s) per publication\n')

    print('print the [starting] line numbers for each publication:')
    print(line_num_lists)
    print('is it correct? ([y]/n)')

    answer = input()
    if answer.lower() == 'n':
        print('user choose to exit...')
        exit()

    print('overriding the existing publications in json? ([y]/n)')

    answer = input()
    overiding_mode = True
    if answer.lower() == 'n':
        overiding_mode = False

    publication_tag_helper(page_text_path, line_num_lists,
                           json_file_path, overiding_mode,
                           num_of_lines_per_publication)

    print('Done!')


if __name__ == '__main__':
    main()
