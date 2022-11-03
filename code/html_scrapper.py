from bs4 import BeautifulSoup
import os
import codecs
import sys
import config
import re
from pathlib import Path
sys.setrecursionlimit(1500)

try:
    Root_path = Path(__file__).resolve(strict=True).parent.parent
except:
    Root_path = Path(r"C:\Users\sarwa\Documents\html_parser").resolve(strict=True)

def text_extract():
    # creating temp folder to save updated html file.
    html_file = "html_file"
    temp_file = "temp_file"
    html_file_path = os.path.join(Root_path, html_file)
    temp_file_path = os.path.join(Root_path, temp_file)

    # take input from user for start and end keyword if single html file present in folder.
    if config.sing_file_flag:
        starting_word = input("please enter the starting unique word: ")
        end_word = input("please enter the ending unique word: ")
    else:
        starting_word = config.starting_word
        end_word = config.end_word

    if not os.path.exists(temp_file_path):
        os.makedirs(temp_file_path)

    # remove existing updated file from the foler.
    for file in os.listdir(temp_file_path):
        os.remove(temp_file_path + "/" + file)

    for name in os.listdir(html_file_path):
        html_file = os.path.join(html_file_path, name)

        file = open(html_file, "r", encoding="ISO-8859-1")
        # reading and parsing html file to beutiful soup.
        html_cont = BeautifulSoup(file.read(), "html.parser")
        orig_html_content = html_cont.prettify()
        
        # split the html content using html seperator.
        final_sep = ''
        for seperator in config.sep_list:
            orig_html_list = orig_html_content.split(seperator)
            data_list = []
            # remove the table data from html file.
            for line in orig_html_list:
                if (
                    "<table" in line
                    or "<td style" in line
                    or "</td>" in line
                    or "</table>" in line
                ):
                    data_list.append("")
                else:
                    data_list.append(line)
            print(len(data_list))
            if len(data_list)>50:
                final_sep = seperator
                break
            else:
                pass


        data_list = [x for x in data_list if x]
        html_data = final_sep.join(data_list)
        # save the updated html file.
        updated_html_path = os.path.join(temp_file_path, "updated_" + name)
        f = open(updated_html_path, "w", encoding="utf-8")
        f.write(html_data)
        f.close()

        # open the updated html file and read the text.
        f = codecs.open(updated_html_path, "r", "utf-8")
        text_data = BeautifulSoup(f.read(), features="html.parser").get_text()
        clean_text = re.sub(r"\n{2,}", "\n", text_data)
        text_list = clean_text.split("\n")

        text_list = [re.sub(r"\s{2,}", "", x) for x in text_list if x]
        text_list = [x for x in text_list if x]

        # filter the text according the start and end keywords.
        starting_index = 0
        ending_index = 0
        for ind, ele in enumerate(text_list):
            if starting_word in ele:
                starting_index = ind
                # break
            if end_word in ele:
                ending_index = ind
        print(starting_index,ending_index)
        filterd_list = text_list[starting_index:ending_index]
        filtered_text = "\n".join(filterd_list)

        output_file = os.path.join(config.root_folder, "output.txt")
        f = open(output_file, "w", encoding="utf-8")
        f.write(filtered_text)
        print("***************code run successfully********************")
    return filtered_text


if __name__ == "__main__":
    filter_text = text_extract()
