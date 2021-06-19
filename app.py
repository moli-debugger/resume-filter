from IPython.core import magic
from flask import Flask,render_template,request
from werkzeug.utils import secure_filename
import spacy
from spacy import displacy
import re
import pytesseract
import  PyPDF2

app = Flask(__name__)
#pytesseract.pytesseract.tesseract_cmd= r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text=[]
text_format=''
DATE=[]
org=[]
email=''


def extraction(name):
    with open(name,'rb') as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        for page_number in range(number_of_pages):   # use xrange in Py2
            page = read_pdf.getPage(page_number)
            page_content = page.extractText()
            text.append(page_content)
    return text
def analysis(data):
    global email
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(data)
    p=displacy.render(doc, style="ent")
    for i in doc.ents:
        if(i.label_=='DATE'):
            DATE.append(i)
        if(i.label_=="ORG"):
            org.append(i)
    email=re.findall(r'\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', data,re.I)
    return p



@app.route('/')
def initial():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        filename=f.filename
        data=extraction(filename)
        for text_data in data:
           text_format=''+text_data
        p=analysis(text_format)
        return render_template("uploader.html")

@app.route('/date')
def date():
    return render_template("uploader.html",DATE=DATE,msg=org,email=email)



if __name__ == '__main__':
    app.run(debug=True)
