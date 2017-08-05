# searchpdf
It takes as input a non-searchable pdf file or a directory of non-serachable pdf files and creates 
a searchable copy or copies of the aforementioned pdf file or files in the same directory. For example,
if the input path of the non-searchable pdf is **'C:/Users/myrandomdir/myproject.pdf'**, the searchable 
pdf's path will be **'C:/Users/myrandomdir/myproject_new.pdf'**.

# Prerequisites 
Installation of: <br />
1.Ghostscript <br />
2.Tesseract-OCR <br />

# Example:
import searchpdf <br />
input_file=**'C:/Users/myrandomdir/myproject.pdf'**<br />
new_pdf=searchpdf.pdf(input_file).transform()
