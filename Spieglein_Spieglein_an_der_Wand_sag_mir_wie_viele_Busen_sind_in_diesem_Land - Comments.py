#Just the necessary imports
from bs4 import BeautifulSoup
import urllib.request

#the framework
open('Faust.txt', 'w').close() #necessary because otherwise each new run of the code would add txt
open('FaustSauber.txt', 'w').close() # as above
file_object = open('Faust.txt', 'a')
AllLinks = []
checkLink = 'c'
infile = 'Faust.txt'
outfile = 'FaustSauber.txt'
Busen_Anzahl = 0
GesuchtesWort = 'Busen'

#for finding the sublinks on the webpage
def Find_Sublinks():

    parser = 'html.parser' #could be global but I went for local because of the looks
    resp = urllib.request.urlopen('https://www.projekt-gutenberg.org/goethe/faust1/index.html') #has to be local because later on another resp is used
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset')) #same reason as above

    for link in soup.find_all('a', href=True): #finding all .html links
        subLinks = link['href']
        AllLinks.append(subLinks) #creating a list of all the links
    global chapters #global so we can access it from another variable
    chapters = [idx for idx in AllLinks if idx[0].lower() == checkLink.lower()] #filtering the list of links by using a filter that removes all links that don't start with c
    Go_to_Chapters()

#filtering out the sublinks to the books chapters
def Go_to_Chapters():
    for item in chapters: #for accessing all the chapters of the book
        parser = 'html.parser'
        resp = urllib.request.urlopen('https://www.projekt-gutenberg.org/goethe/faust1/' + item) #new resp that is used to access the chapters
        soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
        file_object.write(str(soup.find_all('p', 'vers'))) #finds all <p> funcs with class ="vers" and writes the content of those funcs into the .txt

#removing all the remaining html code
def Clean_The_Text_file():
    delete_list = ['[<p class="vers">', '<br/>', '</p>]', '<p class="vers">', '</p>', '<span class="regie">', '</span>', '<i>', '</i>'] #all html code that is left
    fin = open(infile)
    fout = open(outfile, 'w+')
    for line in fin: #goes through all lines
        for word in delete_list: #checks each word
            line = line.replace(word, '') #if a word is in delete removes it
        fout.write(line) #rewrites the cleaned line to outfile
    fin.close()          #closing the files for good looks
    fout.close()

#counting the occurences of the word
def Finde_die_Busen():
    with open('FaustSauber.txt', 'r') as f:
        for line in f.readlines():
            words = line.split()
            for i in words:
                if i == GesuchtesWort:
                    global  Busen_Anzahl
                    Busen_Anzahl += 1
                    print(Busen_Anzahl)
    print('Das weibliche Geschlechtsorgan namens Mamma feminina, wird von Goethe sage und schreibe ' + str(Busen_Anzahl) + ' mal erwähnt. Da die Taschenbuchfassung '
+ 'gerade einmal 150 Seiten besitzt, wird also das Wort Busen im Durchschnitt nur alle ' + str(150/Busen_Anzahl) + ' Seiten erwähnt. Weniger als man erwartet!')

#calling all the functions
Find_Sublinks()
file_object.close() #just closing the file
Clean_The_Text_file()
Finde_die_Busen()



