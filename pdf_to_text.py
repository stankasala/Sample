import os
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import io,pathlib
import re, json
from datetime import datetime
import hashlib

def pdf_to_text(fname, folder_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    fpath=folder_path+'/'+fname +'.pdf'
    with open(fpath, 'rb') as fh:

        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    input= '\n'.join([x.strip() for x in text.splitlines()])
    output =  re.sub(r"^[a-zA-Z0-9.\(\) ]{1,3}\n", "", input,flags=re.MULTILINE)
    final=re.sub(r'\n\s*\n', '\n\n', output)
    checksum=hashlib.md5(final.encode('utf-8')).hexdigest()
    fname = pathlib.Path(fpath)
    #print(fname.stat())
    mtime = datetime.fromtimestamp(fname.stat().st_mtime)
    ctime = datetime.fromtimestamp(fname.stat().st_ctime)
    return final, checksum,mtime.strftime("%m/%d/%Y, %H:%M:%S"), ctime.strftime("%m/%d/%Y, %H:%M:%S")
        

with open("output.json", mode='w', encoding='utf-8') as f:
        json.dump([], f)
        feeds=[]


base_path=''
with open('pdf_list.txt', 'r') as f:
        for i, pdf_path in enumerate(f.readlines()):
            #print(pdf_path, pdf_path.split("/")[-1])
            pdf_path=pdf_path.strip()
            fname=pdf_path.split("/")[-1][:-4]
            folder_path=base_path+  "/".join(pdf_path.split("/")[:-1])
#            print(fname, folder_path)
#            pdf_to_text(fname, folder_path)
            try:
                now = datetime.now()
                pdf_article,checksum, mtime, ctime=pdf_to_text(fname, folder_path)
                print(pdf_article)
                out = {'pdf_article': pdf_article,'md5':checksum, 'pdf_meta_info':'File Path='+pdf_path+'; File CreatedAt='+ctime+'; File ModifiedAt='+mtime+'; Scraped At='+now.strftime("%m/%d/%Y, %H:%M:%S")+';Scraped By = Sashank'}
                feeds.append(out)
                if(i%3==0 and i!=0):
                    
                    print(i)
            except Exception as err:
                print('Failed::', fname, err)


with open("output.json", mode='w', encoding='utf-8') as feedsjson:
    json.dump(feeds, feedsjson)

