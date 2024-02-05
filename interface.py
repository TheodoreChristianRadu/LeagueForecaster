
from bottle import route, run, static_file, template, request
from FinalScrapping import Scrapping
from Operationalization import predict

file = open("index.html","r",encoding="utf-8").read()

@route('/') 
def index(): 
    return template(file, boule=False, result="", kda="")
  
@route('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root='./serv')

@route('/process_form', method='POST')
def process_form():
    # Access form data from POST request
    username = request.forms.get('username')

    data = Scrapping(username) #pour ne recuperer qu'une seule game

    #inserer fonction de prediction

    #recuperer la game de la bonne personne
    #for i in range(0,len(scrapped)):
    #    if scrapped[i]
    game = predict(data)

    if game[79] >= 0.5:
        result = "Win"
    else:
        result = "Loose"
    
    kda = f"{int(game[32])} / {int(game[10])} / {int(game[0])}"

    return template(file, boule=True, result=result,kda=kda)

run(host='localhost', port=8000,debug=True)
