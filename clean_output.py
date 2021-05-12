import json
import re
from langdetect import DetectorFactory, detect
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0
def detect_lang(text):
    try:
        detect(text)
        return detect(text)
    except LangDetectException:
        return "UNK"

with open("output.json", 'r') as f:
    data= f.read()

# data = data.replace('\\n', '\n')
print(data[:1000])


json_data= json.loads(data)
for i in range (len(json_data)):
    if i%3==0:
        # break
        print(i)
    artcl=json_data[i]['pdf_article']

    #Language
    json_data[i]['language']= detect_lang(artcl)
    print(json_data[i]['language'])

    pattern3 = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    urls = re.findall(pattern3, artcl)
    artcl= re.sub(pattern3, 'URL', artcl)
    json_data[i]['urls_list']= urls

    pattern1 = "\(cid:[0-9]+\)" #pattern for find (cid:dd) (cid :55)
    artcl =re.sub(pattern1, '', artcl)

    pattern2 = r"([a-zA-Z0-9.]*)\1{3,}"
    artcl= re.sub(pattern2, r'\1', artcl)


    # print(artcl)
    json_data[i]['pdf_article']= artcl

with open("cleaned_output.json", 'w') as fw:
    # fw.write(json.dumps(json.loads(data), indent=4))
    fw.write(json.dumps(json_data))
