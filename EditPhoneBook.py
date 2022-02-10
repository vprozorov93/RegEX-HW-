import csv
from prettytable import PrettyTable
import re


class EditPhoneBook:
    def __init__(self, phonebook_file_name):
        with open(phonebook_file_name) as f:
            rows = csv.reader(f, delimiter=",")
            self.contacts_list = list(rows)

    def print_table(self, save=False):
        x = PrettyTable()

        x.field_names = self.contacts_list[0]
        for row in self.contacts_list[1:]:
            x.add_row(row)
        print(x)
        if save:
            self.save_phone_book()

    def edit_names(self):
        for row in self.contacts_list[1:]:
            for index, name in enumerate(row[:3]):
                if ' ' in name:
                    cache = name.split()
                    count_index = 0
                    for index_e, element in enumerate(cache):
                        row[index + count_index] = element
                        count_index += 1

    def process_doubles(self):
        cache_list = [row[:2] for row in self.contacts_list[1:]]
        double_list = [cache_list.pop(cache_list.index(el)) for el in cache_list if cache_list.count(el) > 1]
        double_list = [row for index, row in enumerate(self.contacts_list) if row[:2] in double_list]

        for row in double_list:
            self.contacts_list.remove(row)

        double_name_dict = {}
        for row in double_list:
            if not double_name_dict.get(row[0] + row[1]):
                double_name_dict[row[0] + row[1]] = [row]
            else:
                double_name_dict[row[0] + row[1]].append(row)

        count_dict = 0
        result = []
        for key, values in double_name_dict.items():
            result.append(values.pop(0))

            for row in values:
                for index, column in enumerate(row):
                    if not result[count_dict][index]:
                        result[count_dict][index] = column
            count_dict += 1

        self.contacts_list.extend(result)

    def reformat_phone_numbers(self):
        regex_pattern = r"(\+7|8)\s?\(?(\d{3})\)?\s?\-?(\d+)s?\-?(\d+)s?\-?(\d+)\s?\(?(доб.)?\s?(\d+)?\)?"
        for row in self.contacts_list[1:]:
            row[5] = re.sub(regex_pattern, r"+7(\2)\3\4\5 \6\7", row[5])

    def save_phone_book(self, phonebook_save_path="phonebook.csv"):
        with open(phonebook_save_path, "w") as f:
            data_writer = csv.writer(f, delimiter=',')
            data_writer.writerows(self.contacts_list)

    def process_and_save_phone_book(self, print_phonebook=False):
        self.edit_names()
        self.process_doubles()
        self.reformat_phone_numbers()
        if print_phonebook:
            self.print_table(True)
        else:
            self.save_phone_book()
