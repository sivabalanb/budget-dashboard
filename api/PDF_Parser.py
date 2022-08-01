import sys, fitz
doc = fitz.open('test.pdf')     # or fitz.Document(filename)
out = open("test.txt", "wb")  # open text output
for page in doc:  # iterate the document pages
    text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
    print("Text", text)
    out.write(text)  # write text of page
    out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
out.close()