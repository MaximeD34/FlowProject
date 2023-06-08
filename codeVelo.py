# stdlib imports
import json


# third-party imports (may need installing)
import requests
import csv


def setBikeInfos():

    # Creating csv file
    myfile = open('BikeStations.csv', 'w', newline='')
    csvwriter = csv.writer(myfile) # 2. create a csvwriter object
    csvwriter.writerow(['ID','totalSlotNumber','City','Street','Longitude','Latitude']) ## 4. write the header
    #Looping on every dock station (57 known)
    for i in range(1,60): #60 au lieu de 5
        
        print("loading [" + str(i) + "/60]")
        # Formating URL
        addedstr=str(i)
        if i < 9:
            addedstr = '0'+addedstr
        url='https://portail-api-data.montpellier3m.fr/bikestation?id=urn%3Angsi-ld%3Astation%3A0'+addedstr+'&limit=1'
        # Sending request
        response = requests.get(url)

        # Translating byte response to Python data structures
        response_json = response.json()
        
        if len(response_json)>0:

            # Extracting data from Json
            
            data=[response_json[0]['id'].replace(":","%3"),
                response_json[0]['totalSlotNumber']['value'],
                response_json[0]['address']['value']['addressLocality'],
                response_json[0]['address']['value']['streetAddress'],
                response_json[0]['location']['value']['coordinates'][0],
                response_json[0]['location']['value']['coordinates'][1],
                response_json[0]['availableBikeNumber']['value']
                ]
            # Wrinting Values in csv
            csvwriter.writerow(data) # 5. write the rest of the data
    myfile.close()



def getBikeInfos():
    
    marker_data = []

    with open('BikeStations.csv', 'r') as f:
    # Créer un objet csv à partir du fichier
        obj = csv.reader(f)
        
        isFirstLine = True
        for ligne in obj:
            if isFirstLine:
                isFirstLine = False
                continue
            dico = {}
            dico["ID"] = ligne[0]
            dico["nbVelos"] = int(ligne[1])
            dico["City"] = ligne[2]
            dico["Street"] = ligne[3]
            dico["longitude"] = float(ligne[4])
            dico["latitude"] = float(ligne[5])
            dico["dispos"] = int(ligne[6])
            marker_data.append(dico)    

    return marker_data

import math

def getClosestPosition(lat, lon, data):
    #print(data)
    min = -1
    minPosition = {}
    for position in data:
        
        if position['dispos'] == 0:
            continue
        
        #print("POSITION : ", position)
        lonData = position['longitude']
        latData = position['latitude']
        x = (lonData-lon)*math.cos((lat+latData)/2)
        y = latData-lat
        z = math.sqrt(x**2 + y**2)
        d = 1852*60*z

        if min == -1 or d < min :
            min = d
            minPosition = position
    
    if min == -1:
        return None

    return minPosition