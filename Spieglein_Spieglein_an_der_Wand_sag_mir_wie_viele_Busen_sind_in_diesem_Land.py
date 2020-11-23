from bs4 import BeautifulSoup
import urllib.request

open('Faust.txt', 'w').close()
open('FaustSauber.txt', 'w').close()
file_object = open('Faust.txt', 'a')
AllLinks = []
checkLink = 'c'
infile = 'Faust.txt'
outfile = 'FaustSauber.txt'
Busen_Anzahl = 0
GesuchtesWort = 'Busen'

def Find_Sublinks():

    parser = 'html.parser'
    resp = urllib.request.urlopen('https://www.projekt-gutenberg.org/goethe/faust1/index.html')
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))

    for link in soup.find_all('a', href=True):
        subLinks = link['href']
        AllLinks.append(subLinks)
    global chapters
    chapters = [idx for idx in AllLinks if idx[0].lower() == checkLink.lower()]
    Go_to_Chapters()

def Go_to_Chapters():
    for item in chapters:
        parser = 'html.parser'
        resp = urllib.request.urlopen('https://www.projekt-gutenberg.org/goethe/faust1/' + item)
        soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
        file_object.write(str(soup.find_all('p', 'vers')))

def Clean_The_Text_file():
    delete_list = ['[<p class="vers">', '<br/>', '</p>]', '<p class="vers">', '</p>', '<span class="regie">', '</span>', '<i>', '</i>']
    fin = open(infile)
    fout = open(outfile, 'w+')
    for line in fin:
        for word in delete_list:
            line = line.replace(word, '')
        fout.write(line)
    fin.close()
    fout.close()

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


Find_Sublinks()
file_object.close()
Clean_The_Text_file()
Finde_die_Busen()



