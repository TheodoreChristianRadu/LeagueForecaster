
from bottle import route, run, static_file, template, request
from FinalScrapping import Scrapping

file = open("index.html","r",encoding="utf-8").read()



@route('/') 
def index(): 
    name="michel"
    bill=False
    return template(file, predict=name, boule=bill, result="") 
  
@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./serv')

@route('/process_form', method='POST')
def process_form():
    # Access form data from POST request
    username = request.forms.get('username')
    tagline = request.forms.get('tagline')

    

    result = Scrapping(username)[0]

    # Return the result
    print(file)
    return template(file, result=result, boule=True,predict="ta mere")

run(host='localhost', port=8000,debug=True) 

