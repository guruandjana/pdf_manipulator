# flask_ngrok_example.py
from flask import Flask, render_template, request, render_template_string, send_file,send_from_directory,url_for
from werkzeug.datastructures import WWWAuthenticate
from werkzeug.exceptions import HTTPException
import os,time
import ghostscript
from ocrmypdf import ocr
import pandas as pd
import camelot as cm
from zipfile import ZipFile


app = Flask(__name__)
app.config['FLASK_ENV'] = 'development'
app.config["CLIENT_PDF"] = r"/var/www/mainapp/mainapp/data/"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload_file", methods = ['GET','POST'])
def upload_file():  
    return render_template("upload_file.html")

# @app.route('/success', methods = ['POST'])  
# def success(): 
#   os.chdir('/home/pushkar/projects/flask_app/data/') 
#   if request.method == 'POST':  
#     f = request.files['file']  
#     f.save(f.filename) 
#     global WHAT
#     WHAT = f.filename
#     return render_template_string('<html><body><p>File <strong><em>{{ what }}</em></strong> has been uploaded successfully</p>\
#      <form action = "/extract" method = "post" enctype="multipart/form-data">  \
#      <input type = "submit" value="Extract">  </body> \
#     </html>', what=f.filename)

@app.route('/extract', methods = ['GET','POST'])
def extract():

    os.chdir('/var/www/mainapp/mainapp/data/') 
    if request.method == 'POST':  
        f = request.files['attachment']  
        f.save(f.filename) 
        global WHAT
        WHAT = f.filename
     # Extract data from the zip file[***CHANGE THE FILEPATH***]
    main_folder = "/var/www/mainapp/mainapp/data/"

    # Create a directory for input and output folder
    time_stmp = time.time_ns()
    postfix = f'{WHAT.split(".")[0]}_{str(time_stmp)}'


    os.mkdir(f'input_papers_{postfix}')
    os.mkdir(f'output_papers_{postfix}')

  # Creating data folder to save the extracted files
    global input_folder_path
    global output_folder_path
    input_folder_path = os.path.join(main_folder,f'input_papers_{postfix}')
    output_folder_path = os.path.join(main_folder,f'output_papers_{postfix}')

  
    for i in os.listdir():
      if i[-4:] == '.zip':
        with ZipFile(os.path.join(main_folder, WHAT), 'r') as zip_ref:
            zip_ref.extractall(input_folder_path)


  # Parse the content if not searchable or else pass

    text_post = f'{WHAT.split(".")[0]}'
    print(os.path.join(input_folder_path,text_post))
    files = [file for file in os.listdir(os.path.join(input_folder_path,text_post)) if file.endswith('.pdf')]
    for pdf in files:
          try:
              ocr(f'{os.path.join(input_folder_path,f"{text_post}")}/{pdf}', f'{output_folder_path}/_parsed_{pdf}', deskew=True, skip_text=True)
          except TypeError:
            pass
  

    # Extraction of data from searchable pdf
    df = pd.DataFrame()
    os.chdir(output_folder_path)
    for i in os.listdir():
      if i.endswith(".pdf"):
        pdf_data = cm.read_pdf(i, flavor='lattice', pages='1')
        pdf_data_iter = pdf_data[0].df.T
        pdf_data_iter[19] = i
        df = df.append(pdf_data_iter).drop_duplicates(keep='first', subset = [0,1])
        df.iloc[0,19] = "Filename"
      else:
        pass
    df.to_csv(f"{text_post}_extracted_content.csv",header=None,index=False) 
    return render_template("download.html")

    # return render_template_string('<html><body><p>The Extraction was finished successfully.</p>\
    # <form action = "/download_file" method = "post" enctype="multipart/form-data">  \
    # <input type = "submit" value="Download">  </body></html>') 

@app.route('/download_file' ,methods = ['GET','POST'])
def download_file(main_filename=os.getcwd()):
  extracted_file = os.path.join(main_filename,'data',output_folder_path)
  final_filename = [file for file in os.listdir(extracted_file) if file.endswith('.csv')][0]
  print(final_filename)
  app.config["CLIENT_PDF"] = extracted_file

  try:
    return send_from_directory(app.config["CLIENT_PDF"], path=final_filename, as_attachment=True)
  except FileNotFoundError:
    HTTPException.abort(404) 



# >>>> ESI Extractor goes here <<<<
@app.route("/upload_fileESI", methods = ['GET','POST'])
def upload_fileESI():  
    return render_template("upload_fileESI.html")

@app.route('/extractESI', methods = ['GET','POST'])
def extractESI():
  os.chdir('/var/www/mainapp/mainapp/data/') 
  if request.method == 'POST':  
    f = request.files['attachment']  
    f.save(f.filename) 
    global WHAT
    WHAT = f.filename    
    
    main_folder = "/var/www/mainapp/mainapp/data/"
    # Create a directory for input and output folder
    time_stmp = time.time_ns()
    postfix = f'{WHAT.split(".")[0]}_{str(time_stmp)}'
    os.mkdir(f'input_papers_{postfix}')
    os.mkdir(f'output_papers_{postfix}')


  # Creating data folder to save the extracted files
    global input_folder_path
    global output_folder_path
    input_folder_path = os.path.join(main_folder,f'input_papers_{postfix}')
    output_folder_path = os.path.join(main_folder,f'output_papers_{postfix}')

    for i in os.listdir():
      if i[-4:] == '.zip':
        with ZipFile(os.path.join(main_folder, WHAT), 'r') as zip_ref:
            zip_ref.extractall(input_folder_path)
      else:
          pass

  # Parse the content if not searchable or else pass

    text_post = f'{WHAT.split(".")[0]}'
    # print(os.path.join(input_folder_path,text_post))
    files = [file for file in os.listdir(os.path.join(input_folder_path,text_post)) if file.endswith('.pdf')]
    for pdf in files:
          try:
              ocr(f'{os.path.join(input_folder_path,f"{text_post}")}/{pdf}', f'{output_folder_path}/_parsed_{pdf}', deskew=True, skip_text=True)
          except TypeError:
            pass
  

    # Extraction of data from searchable pdf
    
    df = pd.DataFrame()
    os.chdir(output_folder_path)
    tot = os.listdir()
    print(f"Getting till here...")
    for i in tot:
      if i.endswith("pdf"):
        pdf_data = cm.read_pdf(i,flavor='stream', pages='1', edge_tol=500)
        pdf_data_iter = pdf_data[0].df.T
        pdf_data_iter[10] = i
        df = df.append(pdf_data_iter).drop_duplicates(keep='first',subset =[0,1,2,3,4,5,6,7,8,9])
        df.iloc[0,10] = "Filename"
      else:
	       pass
    df.to_csv(f"{text_post}_extracted_content.csv",header=None,index=False) 
    return render_template("downloadESI.html")

    # return render_template_string('<html><body><p>The Extraction was finished successfully.</p>\
    # <form action = "/download_file" method = "post" enctype="multipart/form-data">  \
    # <input type = "submit" value="Download">  </body></html>')  
   

@app.route('/download_fileESI' ,methods = ['GET','POST'])
def download_fileESI(main_filename=os.getcwd()):
  extracted_file = os.path.join(main_filename,'data',output_folder_path)
  final_filename = [file for file in os.listdir(extracted_file) if file.endswith('.csv')][0]
  print(final_filename)
  app.config["CLIENT_PDF"] = extracted_file

  try:
    return send_from_directory(app.config["CLIENT_PDF"], path=final_filename, as_attachment=True)
  except FileNotFoundError:
    HTTPException.abort(404) 
  

if __name__ == '__main__':
    app.run() 