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

    def Write_rows(self, list_of_rows):
        with open( self.fileDir, 'w') as csvFile:
            write = csv.writer(csvFile, delimiter=';')
            write.writerows(list_of_rows)
