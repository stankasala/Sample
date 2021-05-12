import os
list_of_pdfs = []
list_of_htmls = []
for root, dirs, files in os.walk("/home/ec2-user/childrenshealthdefense-pdf.org/"):
    for file in files:
        if file.endswith(".pdf"):
             #print(os.path.join(root, file))

             list_of_pdfs.append(os.path.join(root, file))
print(len(list_of_pdfs))

with open("pdf_list.txt","w") as f:
    for item in list_of_pdfs:
        f.write("%s\n" % item)

for root, dirs, files in os.walk("/home/ec2-user/childrenshealthdefense-pdf.org/"):
    for file in files:
        if file.endswith(".html"):
             #print(os.path.join(root, file))

             list_of_htmls.append(os.path.join(root, file))
print(len(list_of_htmls))

