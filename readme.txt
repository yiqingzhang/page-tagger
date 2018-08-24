


list of files:

license.txt            ---  license for the program.
tag_helper.py          ---  python script that helps the tagging of publication strings, especially there are more than one publication strings in a webpage.
validate.py            ---  python script that validate the annotated webpages, it only checks for obvious mistakes.
tagging_protocol.txt   ---  annotation rules and protocols.




================================================================
We maintain a list of helpful notes for HomePub dataset annotation here, and the list will be updated if necessary.


(1) It is recommended to use a modern text editor to view and edit json and .txt files. For example, Sublime Text, and Atom Editor are good choices. 


(2) It is important validate the tagged json, after you finish tagging each page.


(3) The tag_helper.py must be placed in the same folder as the xxx.html, xxx.tag.json files.


(4) Read comments at the beginning of programs, before running programs. The comments at the top of programs contains information about how to run programs.


(5) If a single publication is separated in two lines:
for example as in tagged_example/47, and tagged_example/21, our tag_helper.py program can deal with that.

    For example, if we want to tag publication using the tag_helper.py for tagged_example/47, the following input can be used:

    2 (choose mode 2)
    43 (start line of the first publication)
    127 (start line of the last publication)
    3 (step value, since there is a publication every 3 lines)
    3 (each publication occupies 3 lines)
    y (confirm)
    y (confirm overriding)


(6) It is highly recommended to use Anaconda Python environment, please install python 3.

    https://www.continuum.io/downloads


(7) Why the contents in the text file are all in the same line, under Windows system?
    Because some text editors under windows system use different delimiters for newline. To avoid this, use a modern text editor, such as Sublime Text.


(8) Please do not change the content of .txt .html files.


(9) About json file: if you got an error message saying it is not a valid json file, you can check your json file here: https://jsonformatter.curiousconcept.com/ to get some clues. 

