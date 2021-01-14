# Use RightClik on the element you want to from the webpage -> Inspect, in order to see how the element looks in html format 

import requests, pandas
from bs4 import BeautifulSoup

r = requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content    # load the content of the webpage in variable "c"
#print(c)

soup=BeautifulSoup(c,"html.parser")
#print(soup.prettify())   # display the content in a nice indented format

all=soup.find_all("div",{"class":"propertyRow"})
page_number=soup.find_all("a",{"class":"Page"})[-1].text    # returns the total number of webpages that need to be parsed for data 
print(page_number)
print(all[0])
print(all[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")) # for the first element ([0]) in the "all" list\
                                                                                     # it displays just the text from header4 (h4)/ class:propPrice\
                                                                                     # and removes the newlines and blank spaces
l=[]     # creates an empty list in which to store the dictionaries
base_url="http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

for page in range(0,int(page_number)*10,10):         #  this loop goes through all the webpages corresponding to the selection (4 pages in this case; 0 to 30, with a step of 10) 
    #print(base_url+str(page)+".html")
    r = requests.get(base_url+str(page)+".html", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    #print(soup.prettify())
    all=soup.find_all("div",{"class":"propertyRow"})
    #print(all)

    for item in all:
        d={}            # creates an empty dictionary
        d["Price"]=item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")
        d["Address"]=item.find_all("span",{"class":"propAddressCollapse"})[0].text     # finds the 1st ([0]) element in the list corresponding to the search criteria
        try:
            d["City"]=item.find_all("span",{"class":"propAddressCollapse"})[1].text    # finds the 2nd ([1]) element in the list corresponding to the search criteria 
        except:                                                                        # in case the search has no result ("None"), move to the next step
            d["City"]=None    
        try:                                                                           
            d["Beds"]=item.find("span",{"class":"infoBed"}).find("b").text  
        except:
            d["Beds"]=None
        try:                                                                     
            d["Baths"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text  
        except:
            d["Baths"]=None
        try:                                                                     
            d["Square Feet"]=item.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Square Feet"]=None
        try:                                                                     
            d["Half Baths"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text  
        except:
            d["Half Baths"]=None
        for column_group in item.find_all("div",{"class":"columnGroup"}):   # this for loop returns the "Lot size"
            # from each division it selects classes "featureGroup" and "featureName"
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot size" in feature_group.text:
                    d["Lot zise"]=(feature_name.text)
        l.append(d)    # appends the dictionary to a list

#print(l)

df=pandas.DataFrame(l)    # inserts the list into a dataframe
#print(df)
df.to_csv("Output.csv")

