
from bottle import route, run, static_file, template, request
from FinalScrapping import Scrapping

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

    scrapped = Scrapping(username)[0] #pour ne recuperer qu'une seule game

    #inserer fonction de prediction

    #recuperer la game de la bonne personne
    #for i in range(0,len(scrapped)):
    #    if scrapped[i]
    game=scrapped['participants'][0]

    if game['win'] == True:
        result="Win"
    else:
        result="Loose"
    
    kda = str(game['kills']) + ' / ' + str(game['deaths']) + ' / ' + str(game['assists'])

    return template(file, boule=True, result=result,kda=kda)

run(host='localhost', port=8000,debug=True) 

