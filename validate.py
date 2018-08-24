"""

Program to validate the tagged files.

If the folder structure is like this:

webpages/1/xxx.html
          /xxx.tag.json
          /xxx.txt

webpages/2/xxx.html
          /xxx.tag.json
          /xxx.txt
...


place this program under webpages/:
webpages/validate.py

Run this program with:
python validate.py

Please use python 3, instead of python 2.
run "python --version" to see the version of python

environment setup:
pip install validate_email
pip install chardet

"""
import json
from validate_email import validate_email
import os
import sys
import chardet

# ##################other configuration##############
# please do not change this
ADD_START_INDEX_INFO = True
# ###################################################


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


def get_folder_list():
    print('Please enter the starting folder number for validating.')
    answer = input()
    try:
        start_folder_num = int(answer)
    except Exception as e:
        print('wrong input, exiting...')

    print('Please enter the end folder number for validating (inclusive)')
    answer = input()
    try:
        end_folder_num = int(answer)
    except Exception as e:
        print('wrong input, exiting...')
        exit(1)

    folder_num_lists = []
    for i in range(start_folder_num, end_folder_num + 1):
        folder_num_lists.append(i)

    print('print the folder numbers for validation:')
    print(folder_num_lists)
    print('is it correct? ([y]/n)')

    answer = input()
    if answer.lower() == 'n':
        print('user choose to exit...')
        exit()

    for i in range(len(folder_num_lists)):
        folder_num_lists[i] = str(folder_num_lists[i])

    for folder in folder_num_lists:
        if not os.path.exists(folder):
            print(folder, 'does not exists, exiting...')
            exit(1)

    return folder_num_lists


def validate_publications(data, text_filepath, json_filepath):
    try:
        contain_publication_list = data['contain_publication_list']
    except Exception as e:
        print('contain_publication_list is not present in json')
        exit(1)
    if contain_publication_list != 'T' and contain_publication_list != 'F':
        print('contain_publication_list must be either T or F, ERROR!')

    try:
        publications = data['publications']
    except Exception as e:
        print('publications is not present in json')
        exit(1)

    num_of_pubs = 0
    pure_publications = []
    for pub in publications:
        try:
            text = pub['text']
            if text != "COPY_SINGLE_PUBLICATION_HERE":
                num_of_pubs += 1
                pure_publications.append(pub)
        except Exception as e:
            print('text key does not exists in publications, exit...')
            exit(1)

    if num_of_pubs > 0 and contain_publication_list == 'F':
        print('num_of_pubs > 0 and contain_publication_list == F, ERROR!')
    if num_of_pubs == 0 and contain_publication_list == 'T':
        print('num_of_pubs == 0 and contain_publication_list == T, ERROR!')

    if num_of_pubs == 0:
        return

    with open(text_filepath, encoding=detect_encodings(text_filepath)) as fin:
        content = fin.read()

    for pub in pure_publications:
        text = pub['text']
        if text not in content:
            print(text + ' is not in txt file, ERROR!')
        else:
            start_index = content.find(text)
            if start_index == -1:
                print('starting index should not be 0')
            else:
                length = len(text)
                if ADD_START_INDEX_INFO:
                    pub['start_index_in_file'] = start_index
                    pub['length'] = length

    if ADD_START_INDEX_INFO:
        # sort the publications based on start_index_in_file
        pure_publications = sorted(pure_publications,
                                   key=lambda k: k['start_index_in_file'])
        data['publications'] = pure_publications

    with open(json_filepath, 'w', encoding='utf-8') as fout:
        json.dump(data, fout, indent=2, sort_keys=True)


def validate_json(data, folder_name):
    """
    data: the input json object, now it is assumed to be valid.

    """

    # check if it is a personal homepage
    try:
        is_personal_homepage = data['is_personal_homepage']
    except Exception as e:
        print('is_personal_homepage key is not present in json')
        exit(1)

    if is_personal_homepage != 'T' and is_personal_homepage != 'F':
        print('is_personal_homepage must be either T or F, ERROR!')
    if is_personal_homepage == 'F':
        print('not a personal homepage, DONE')
        return

    # check the email.
    try:
        email = data['email']
    except Exception as e:
        print('email key is not present in json')
        exit(1)
    is_valid = validate_email(email)
    if not is_valid and email != '':
        print('email ' + email + ' is not valid, ERROR!')

    # check the filename is not changed
    try:
        filename = data['filename']
    except Exception as e:
        print('filename key is not present in json')
        exit(1)
    json_filepath = os.path.join(folder_name, filename + '.tag.json')
    if not os.path.exists(json_filepath):
        print('filename does not match the file')
    text_filepath = os.path.join(folder_name, filename + '.txt')
    if not os.path.exists(text_filepath):
        print('filename does not match the file')

    # check the name
    try:
        name = data['name']
    except Exception as e:
        print('name key is not present in json')
        exit(1)

    with open(text_filepath, encoding=detect_encodings(text_filepath)) as fin:
        content = fin.read()
        if name not in content:
            print('name "' + name + '" is not in the txt file. ERROR!')

    # check the publications
    validate_publications(data, text_filepath, json_filepath)


def main():
    """"""
    PY3 = sys.version_info[0] == 3
    if not PY3:
        print('please use python 3 to run the program, exiting...')
        exit(1)

    if ADD_START_INDEX_INFO:
        print('\nmake sure to save all tagged files before validating\n')
        print('BACKUP UP the tagged files before validating\n')

    folder_list = get_folder_list()
    for folder in folder_list:
        text = '-------------------------'
        text += 'checking folder ' + folder
        text += '----------------------------'
        print(text)

        files = os.listdir(folder)
        try:
            ext = '.tag.json'
            length = len(ext)
            for f in files:
                if len(f) > length and f[-length:] == ext:
                    filename = f[:-length]
                    break
            if filename is None:
                print('\ncheck xxx.tag.json is present in folder' + folder)
                print('error, exiting...')
                exit(1)
        except Exception as e:
            print("""make sure place this validate.py in the right place,
                make sure .tag.json file is present in folder""" +
                  folder + ", and file name is not changed")
            print("Exiting...")
            exit(1)

        json_file_path = os.path.join(folder, filename + '.tag.json')
        text_file_path = os.path.join(folder, filename + '.txt')
        if not os.path.exists(json_file_path):
            print(json_file_path + ' does not exists, ERROR')
            exit(1)
        if not os.path.exists(text_file_path):
            print(text_file_path + ' does not exists, ERROR')
            exit(1)

        file_encoding = detect_encodings(json_file_path)
        with open(json_file_path, encoding=file_encoding) as fin:
            try:
                data = json.load(fin)
            except Exception as e:
                print(json_file_path, 'is not a valid JSON file')
                print('please check the format, exiting')
                exit(1)

            validate_json(data, folder)


if __name__ == '__main__':
    main()
