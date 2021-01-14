import requests
from bs4 import BeautifulSoup

# requests the content of a webpage
r = requests.get("http://www.pyclass.com/example.html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content   # loads the content of the webpage in variable "c"

#print(c)

soup=BeautifulSoup(c,"html.parser")    # displays the content (variable "c") in html format
#print(soup)
#print(soup.prettify())                 # displays the content (variable "c") in html format with indentation

#all=soup.find("div",{"class":"cities"})      # returns only the first division
all=soup.find_all("div",{"class":"cities"})  # returns all divisions

print(all)
#print(all[0])   # returns only the first element of the list

# print(all[0].find_all("h2"))    # returns only the header of the first element in the list, as a list -> [<h2>London</h2>]
# print(all[0].find_all("h2")[0])    # returns the first element of the list, NOT a list -><h2>London</h2>
# print(all[0].find_all("h2")[0].text) # returns just the text of the first element

for item in all:
    print(item.find("h2").text)
    # print(item.find("p").text)      # returns the pragraphs


