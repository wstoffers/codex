#**    This line is 79 characters long.  The 80th character should wrap.   ***\

#imports:
import os, re
import json
import codecs
import pdfplumber

#define:
def pdfExperiment(filePath):
    pdf = pdfplumber.open(filePath)
    fields = pdf.doc.catalog["AcroForm"].resolve()["Fields"]
    form_data = {}
    for field in fields:
        try:
            field_name = field.resolve()["T"]
            field_value = field.resolve()["V"]
        except KeyError:
            #if every box has been checked and every field is typed in
            #    then there are no issues with 'v' missing
            print(f'error entry: {field.resolve()}')
        form_data[field_name] = field_value
#    firstPage = pdf.pages[0]
#    text = firstPage.extract_text()
#    pdf.close()
    return form_data

#run:
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True,
                        help='path to pdf')
    args = parser.parse_args()
    test = pdfExperiment(args.file)
    print(test)
