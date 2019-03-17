import pynder
import simplekml
import argparse
import lxml
import os, sys
import random
from polycircles import polycircles
from settings import *

class GeoPoint():

    def __init__(self,lat,lon):
        #pass or something else
        self.lat=lat
        self.lon=lon

class TndrLocalizer:

    def __init__(self, session):
        self.session = session

        self.position_orig_lat= self.session._api.profile()["pos"]["lat"]
        self.position_orig_lon= self.session._api.profile()["pos"]["lon"]
        
        self.id_list = []
        self.name_list = []

    def get_matches(self):
        self.matches = self.session._api.matches(None)


        for i in range(len(self.matches)):
            self.id_list.append(self.matches[i]["person"]["_id"])
            self.name_list.append(self.matches[i]["person"]["name"])

        for id in self.id_list:
            print("%s, ID: %s" % (self.session._api.user_info(id)["results"]["name"], id))
        return

    # Receives multiple points, return distances from all of them to matches
    def get_distances_from_points(self, points):

        i = 0
        distances = [[] for x in range(0,len(points))]

        for point in points:
            print ("[INFO] Updated position at: "+str(point.lat)+", "+str(point.lon) )
            res = self.session.update_location(point.lat, point.lon)

            # Sweep matches list and append distance to each match
            for id in self.id_list:
                distances[i].append(self.session._api.user_info(id)["results"]["distance_mi"])
            i+=1

        # Clean position to origin
        print ("[INFO] Restored position to original at: "+str(point.lat)+", "+str(point.lon) )
        res = self.session.update_location(self.position_orig_lat, self.position_orig_lon)

        return distances

    def draw_circles(self, points, distances, radius_size=800):
        
        parent_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"
        # GENERATE KML
        kmlObject = []
        i = 0

        for id in self.id_list:
            try:
                ## For each point, draw each polycircle for each distance
                j = 0
                for point in points:
                    kmlObject.append(simplekml.Kml())

                    outer_polycircle = polycircles.Polycircle(latitude=point.lat,longitude=point.lon,radius=distances[j][i]*1600+radius_size/2,number_of_vertices=50)
                    inner_polycircle = polycircles.Polycircle(latitude=point.lat,longitude=point.lon,radius=distances[j][i]*1600-radius_size/2,number_of_vertices=50)
                    pol = kmlObject[i].newpolygon(name="test"+str(j),outerboundaryis=outer_polycircle.to_kml(),innerboundaryis=inner_polycircle.to_kml())
                    pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.red)
                    j += 1 
                
                kmlObject[i].save(parent_folder + "output/" + self.name_list[i] + "_" + id[-4:] + ".kml")
                

            except Exception as e:
                print(e)
                pass

            print ("[INFO] Drawn kml circles at ./output/ for :", self.name_list[i] )
            i += 1 


    def localize(self):
        self.get_matches()

        ## DECLARE AND POSITION POINTS ##
        ## At the moment, this is done manually
        ## Change of lat or lon of 0.002 ~~ 250m, which is pretty noisy to do this fast ;)
        point1=GeoPoint(self.position_orig_lat,  self.position_orig_lon)
        point2=GeoPoint(self.position_orig_lat,  self.position_orig_lon+0.02)
        point3=GeoPoint(self.position_orig_lat+0.02,  self.position_orig_lon)
        points = [point1, point2, point3]
        
        distances = self.get_distances_from_points(points)

        self.draw_circles(points, distances, 400)