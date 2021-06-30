# from tabula import read_pdf
from tabulate import tabulate

# df = read_pdf("pdf2.pdf", pages="8", lattice=True)
# # print(tabulate(df))
# print(df)

from pdf2docx import Converter, parse

# cv = Converter("pdf2.pdf")
# cv.convert("dox.docx")
# parse()
# cv.close()

cv = Converter("pdf2.pdf")
tables = cv.extract_tables(start=7, end=9)
cv.close()

for table in tables[0]:
    print(table)
    print()