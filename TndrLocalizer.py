import pynder
#import pickle
import simplekml
import argparse
import lxml
import random
from polycircles import polycircles
from settings import *

class GeoPoint:
    lat=0
    lon=0

class TndrLocalizer:

    def __init__(self, session):
        self.session = session

        self.position_orig_lat= session._api.profile()["pos"]["lat"]
        self.position_orig_lon= session._api.profile()["pos"]["lon"]
        
        self.id_list = []
        self.name_list = []

    def get_matches(self):
        self.matches = self.session._api.matches(None)


        for i in range(len(self.matches)):
            self.id_list.append(self.matches[i]["person"]["_id"])
            self.name_list.append(self.matches[i]["person"]["name"])

        for id in self.id_list:
            print("%s, ID: %s, Last time active: %s" % (self.session._api.user_info(id)["results"]["name"], id, self.session._api.user_info(id)["results"]["ping_time"]))
        return self.id_list, self.name_list

    # Receives multiple points, return distances from all of them to matches
    def get_distances_from_points(self, points):

        i = 0
        distances=[]
        for point in points:
            print ("[INFO] Updated position at: "+point.lat+", "+point.lon )
            res = self.session.update_location(point.lat, point.lon)

            # Sweep matches list and append distance to each match
            for id in self.id_list:
                distances[i].append(self.session._api.user_info(id)["results"]["distance_mi"])
            i+=1

        # Clean position to origin
        res = self.session.update_location(self.position_orig_lat, self.position_orig_lon)

        return distances

    def draw_circles(self, points, distances, radius_size=800):
        
        # GENERATE KML
        kmlObject = []
        i = 0
        for id in self.id_list:
            try:
                ## For each point, draw each polycircle for each distance


                # kmlObject.append(simplekml.Kml())
                # outer_polycircle = polycircles.Polycircle(latitude=lat[0],longitude=lon[0],radius=distance[0][i]*1600+radius_size,number_of_vertices=50)
                # inner_polycircle = polycircles.Polycircle(latitude=lat[0],longitude=lon[0],radius=distance[0][i]*1600-radius_size,number_of_vertices=50)
                # pol = kmlObject[i].newpolygon(name="test0",outerboundaryis=outer_polycircle.to_kml(),innerboundaryis=inner_polycircle.to_kml())
                # pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.red)
                
                # outer_polycircle = polycircles.Polycircle(latitude=lat[1],longitude=lon[1],radius=distance[1][i]*1600+radius_size,number_of_vertices=50)
                # inner_polycircle = polycircles.Polycircle(latitude=lat[1],longitude=lon[1],radius=distance[1][i]*1600-radius_size,number_of_vertices=50)
                # pol = kmlObject[i].newpolygon(name="test1",outerboundaryis=outer_polycircle.to_kml(),innerboundaryis=inner_polycircle.to_kml())
                # pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.yellow)
                
                # outer_polycircle = polycircles.Polycircle(latitude=lat[2],longitude=lon[2],radius=distance[2][i]*1600+radius_size,number_of_vertices=50)
                # inner_polycircle = polycircles.Polycircle(latitude=lat[2],longitude=lon[2],radius=distance[2][i]*1600-radius_size,number_of_vertices=50)
                # pol = kmlObject[i].newpolygon(name="test2",outerboundaryis=outer_polycircle.to_kml(),innerboundaryis=inner_polycircle.to_kml())
                # pol.style.polystyle.color = simplekml.Color.changealphaint(100, simplekml.Color.green)
                
                kmlObject[i].save(parent_folder + "output/" + self.name_list[i] + "_" + id[-4:] + ".kml")
            except Exception as e:
                print(e)
                pass
            i += 1 

    def localize(self):
            id_list, name_list = self.get_matches()

            ## DECLARE AND POSITION POINTS ##
            points = []
            
            distances = self.get_distances_from_points(points)