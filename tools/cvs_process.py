import csv

class Csv_data_access:
    def __init__( self, file_dir):
        self.fileDir = file_dir

    def Read_All_Rows(self)->list:
        rows=[]
        with open( self.fileDir, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                rows += row
        return rows

    def Write_row(self, row):
        with open( self.fileDir, 'a') as csvFile:
            header =['name', 'activity','email', 'province', 'url']
            dicWriter = csv.DictWriter(csvFile, fieldnames=header, delimiter=';')
            dicWriter.writerow(row)
