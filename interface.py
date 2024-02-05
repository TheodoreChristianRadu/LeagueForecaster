
from bottle import route, run, static_file, template, request
from FinalScrapping import Scrapping
from Operationalization import predict

file = open("index.html","r",encoding="utf-8").read()

@route('/') 
def index(): 
    return template(file, boule=1, result="", kda="",input="")
  
@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./serv')

@route('/process_form', method='POST')
def process_form():
    # Access form data from POST request
    username = request.forms.get('username')

    
    data = Scrapping(username) 
    if data =="error":
        return template(file, boule=2, result="", kda="",input="")
    else: 
        
        game = predict(data)

        if game[79] >= 0.5:
            result = "Win"
        else:
            result = "Loose"

        kda = f"{int(game[32])} / {int(game[10])} / {int(game[0])}"

        return template(file, boule=3, result=result,kda=kda,input=f"value={username}")

run(host='localhost', port=8000,debug=True)
