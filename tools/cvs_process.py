import csv

class CsvDataAccess:
    def __init__( self, file_dir):
        self.file_dir = file_dir

    def read_all_rows(self)->list:
        rows = list
        with open( self.file_dir, newline='', encoding="utf8") as csv_file:
            spamreader = csv.reader(csv_file, delimiter=';', quotechar='|')
            for row in spamreader:
                rows += row
        return rows

    def write_row(self, row):
        with open( self.file_dir, 'a', encoding="utf8") as csv_file:
            header = ['name', 'activity','email', 'province', 'url']
            dic_writer = csv.DictWriter(csv_file, fieldnames = header, delimiter = ';')
            dic_writer.writerow(row)

    @staticmethod
    def safe_in_csv( company_data_and_emails):
        if company_data_and_emails:
            csv_file = CsvDataAccess('GFG.csv')
            for row in company_data_and_emails:
                if bool(row) and row['email'] != []:
                    csv_file.write_row(row)
