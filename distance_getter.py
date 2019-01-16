from math import sin, cos, sqrt, atan2, radians
from operator import itemgetter
import csv

def get_lat_and_lon(postal_code):
    for line in zip_code_list_with_coordinates:
        if (line[0] == postal_code):
            return line[-2:]

def get_distance(lat1, lon1, lat2, lon2, A, B):
    R = 6373.0
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    
    return distance



words = []
zip_code_list_with_coordinates = []

with open('FI.txt', 'r') as f:
    for line in f:
        words = line.split("\t")
        stripped_words = list(map(lambda it: it.strip(), words))
        zip_code_list_with_coordinates.append([str(stripped_words[1]), str(stripped_words[9]), str(stripped_words[10])])
f.close()

print (zip_code_list_with_coordinates[110])


stores_dict = {
    "00500":[20, "pks"],
    "13100":[21, "hml"],
    "15110":[22, "lah"],
    "05800":[23, "hyv"],
    "90100":[24, "oul"],
    "40100":[25, "jkl"],
    "33100":[26, "tre"],
    "70100":[27, "kpo"],
    "20500":[28, "tku"],
    "45100":[29, "kvl"],
    "50100":[30, "mli"],
    "48100":[31, "kot"],
    "80100":[32, "jns"]
}

for key, value in stores_dict.items():
    stores_dict[key].append(get_lat_and_lon(key))
print (stores_dict)
   

calculated_customergroups = {}
customergroups = []

with open('customers.csv', newline='') as csvfile:

    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        
        distances = []
        nearest_puff = []
        asno = row['CustomerID']
        aspo = str(row['CustomerPostalCode'])
        if len(aspo) < 5:
            aspo = (5-len(aspo))*str(0) + aspo
        
        if aspo in calculated_customergroups:
            customergroups.append([asno, aspo, calculated_customergroups[aspo]["group"], calculated_customergroups[aspo]["puff"], calculated_customergroups[aspo]["distance"]])
        else:
            try:
                for key, value in stores_dict.items():
                    lat1 = float(stores_dict[key][2][0]) 
                    lon1 = float(stores_dict[key][2][1])
                    latlon2 = get_lat_and_lon(str(aspo))
                    customer_group_code = stores_dict[key][0]
                    customer_group_puff = stores_dict[key][1]
                    distance = [customer_group_code, customer_group_puff, aspo, get_distance(lat1, lon1, float(latlon2[0]), float(latlon2[1]), aspo, customer_group_puff)]

                    distances.append(distance)
                
                nearest_puff = min(distances, key=itemgetter(3)) 
                
                
                        
                calculated_customergroups[aspo] = {"group":nearest_puff[0],"puff":nearest_puff[1],"distance":nearest_puff[3]}
                customergroups.append([asno, aspo, nearest_puff[0], nearest_puff[1], nearest_puff[3]])
            except(TypeError):
                print ("Error with postal code: " + aspo)
                pass
            
        
            
print (calculated_customergroups["44800"])

with open('parsed.csv', 'w') as f:
    for line in customergroups:
        f.write(str(line[0]) + ";" +  str(line[1]) + ";" +  str(line[2]) + ";" + str(line[3]) + ";" + str(line[4]) + "\n") 
f.close()

with open('calc_customers.txt', 'w') as f:
    for key, value in calculated_customergroups.items():
        f.write(str(key) + ":" + str(value) +  "\n") 
f.close()
