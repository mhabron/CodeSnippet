import csv
import simplekml

inputfile = csv.reader(open('example.csv', 'r'))
kml = simplekml.Kml()

for row in inputfile:
    kml.newpoint(name = row[0],
                 description= '<img src="' + row[4]
                 + '" alt="picture" width="100" height="100" align="left" />'
                 + row[1],
                 coords=[(row[3], row[2])])

kml.save('example_events.kml')
