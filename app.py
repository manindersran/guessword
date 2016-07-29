# http://lepidllama.net/blog/how-to-push-an-existing-cloud9-project-to-github/
# git@github.com:manindersran/wordguess.git
from flask import Flask, render_template, request, url_for, make_response, redirect
from lxml import html
from bs4 import BeautifulSoup
import requests, random

# Download IMDB's Top 250 data
url = 'http://www.imdb.com/chart/top'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')

app = Flask(__name__)

# ==========================================================
imdb=[]

for index in range(0, len(movies)):
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    data = movie_title
    imdb.append(data)
# print(imdb)
# ==========================================================
randWord=""
guessed = []

def foo():
    global guessed
    guessed =[]
    
# Define a route for the default URL, which loads the form
@app.route('/')
def form():
        randWord =""
        randWord = random.choice(imdb).upper().replace(" ", "_").replace(":", "_").replace("'", "_")
        global randWord
        foo()
        print(randWord)
        # problem with having this inside a view function, creates new random value everytime
        blanks = '_ ' * len(randWord)
        return render_template('index.html', blanks=blanks)
    
@app.route('/', methods=['POST'])
def guess():
            newBlanks = ""
            guess=request.form['guess'].upper()
            guessed.append(guess)
                    
            if guess in randWord:
                newBlanks = " ".join(C if C in guessed else "_" for C in randWord)
                newb = "".join(C if C in guessed else "_" for C in randWord)
                if newb == randWord :
                    win = 'You Found it'
                    return render_template('index.html', win=win,newBlanks=newBlanks)
                
                return render_template('index.html',newBlanks=newBlanks)
            
            else:
                newBlanks = " ".join(C if C in guessed else "_" for C in randWord)
                wrong = 'Wrong Input!! Try again'
                return render_template('index.html',newBlanks=newBlanks,wrong=wrong)

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=8080)