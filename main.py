from EditPhoneBook import EditPhoneBook as EPB

if __name__ == "__main__":
    phone_book = EPB("phonebook_raw.csv")
    phone_book.process_and_save_phone_book(True)
