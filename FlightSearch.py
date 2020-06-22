from math import sin, cos, sqrt, atan2, radians
from urllib import parse
cityNamesInPath = []
R = 6373.0

class city:
    def __init__(self, name, long, lat):
        self.name = name
        self.long = long
        self.lat = lat
    def calc (self, lat1, lon1, lat2, lon2):
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c / 925
    #    print("Result:", distance)
        return distance

class Flightt:
    def __init__(self, flightSourceCity, flightDestinationCity, flightDepartureTime, flightArrivalTime, flightNumber, flightListOfDays):
        self.flightSourceCity = flightSourceCity
        self.flightDestinationCity = flightDestinationCity
        self.flightDepartureTime = flightDepartureTime
        self.flightArrivalTime = flightArrivalTime
        self.flightNumber = flightNumber
        self.flightListOfDays = flightListOfDays
        self.flightActualDestance = flightArrivalTime - flightDepartureTime
    def getFlightDestance(self):
        return self.flightActualDestance
    def getSourceCity(self):
        return self.flightSourceCity
    def getDesinationCity(self):
        return self.flightDestinationCity        
        
class Graph:

    # Initialize the class
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed

    # Add a link from A and B of given distance
    def connect(self, A:Flightt, distance=1):
        self.graph_dict.setdefault(A.flightSourceCity, {})[A.flightDestinationCity] = distance

    # Get neighbors or a neighbor
    def get(self, a, b=None):
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    # Return a list of nodes in the graph
    def nodes(self):
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

# This class represent a node
class Node:
    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0 # Distance to start node
        self.h = 0 # Distance to goal node
        self.f = 0 # Total cost

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
         return self.f < other.f

    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))

def astar_search(graph, heuristics, start, end):
    open = []
    closed = []

    start_node = Node(start, None)
    goal_node = Node(end, None)

    open.append(start_node)
    while len(open) > 0:
        open.sort()
        current_node = open.pop(0)
        closed.append(current_node)
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.name)
                current_node = current_node.parent
            path.append(start_node.name)
            return path[::-1]
        neighbors = graph.get(current_node.name)

        for key, value in neighbors.items():
            neighbor = Node(key, current_node)
            if(neighbor in closed):
                continue

            neighbor.g = current_node.g + graph.get(current_node.name, neighbor.name)
            neighbor.h = heuristics.get(neighbor.name)
            neighbor.f = neighbor.g + neighbor.h

            if(add_to_open(open, neighbor) == True):
                open.append(neighbor)

    return None

def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node and neighbor.f > node.f):
            return False
    return True

def FlightsTakenFunction(pathCount, FlightList, days, path, fligtsTaken, DistenationCity, flightsTakenII):
    for x in FlightList:
        for i in range(0, pathCount-1):
            if x.flightSourceCity == path[i] and x.flightDestinationCity == path[i+1]:
                fligtsTaken.append(x)
                #print(x.flightListOfDays)
    
    for x in fligtsTaken:
        for d in days:
            if d in x.flightListOfDays and x.flightDestinationCity != DistenationCity:
                flightsTakenII.append(x)
                #print(x.flightListOfDays)
            elif d in x.flightListOfDays and x.flightDestinationCity == DistenationCity:
                flightsTakenII.append(x)
                #print(x.flightListOfDays)
                return
                
def main():
    graph = Graph()
    ############################################ObjectsOnly#########################################
    f1 = Flightt ("Alexandria","Aswan",11,12.15,"MS005",[3, 4, 5])
    f2 = Flightt ("Alexandria","Aswan",15.15,16.3,"MS004",[1, 0])
    f3 = Flightt ("Alexandria","Cairo",9.15,10,"MS003",[3, 4, 5])
    f4 = Flightt ("Alexandria","Cairo",12.3,13.15,"MS001",[1, 2])
    f5 = Flightt ("Alexandria","Cairo",17,17.45,"MS002",[1, 3, 6, 0])
    f6 = Flightt ("Alexandria","London",19.3,0.32,"MS006",[1, 2, 6, 0])
    f7 = Flightt ("Alexandria","NewYork",2,15.14,"MS007",[2, 4, 6])

    f8 = Flightt ("Aswan","Cairo",10.2,11.4,"MS022",[1, 2, 3, 5])
    f9 = Flightt ("Aswan","PortSaid",7.05,8.18,"MS023",[4, 6, 0])
    
    f10 = Flightt ("Cairo","Alexandria",13,13.45,"MS008",[2, 3, 5])
    f11 = Flightt ("Cairo","Alexandria",20.15,21,"MS009",[6, 0])
    f12 = Flightt ("Cairo","Aswan",8,9.2,"MS010",[2, 5])
    f13 = Flightt ("Cairo","Aswan",17.15,18.35,"MS011",[1, 4, 6])
    f14 = Flightt ("Cairo","London",10,15.1,"MS014",[2, 3, 4])
    f15 = Flightt ("Cairo","London",15.15,20.25,"MS015",[1, 5, 6])
    f16 = Flightt ("Cairo","NewYork",3,15.05,"MS016",[1, 2, 5])
    f17 = Flightt ("Cairo","NewYork",19.3,7.35,"MS017",[3, 4, 0])
    f18 = Flightt ("Cairo","Paris",2,6.55,"MS018",[5, 6, 0])
    f19 = Flightt ("Cairo","Paris",5,9.55,"MS019",[1, 3])
    f20 = Flightt ("Cairo","PortSaid",11,11.2,"MS013",[3])
    f21 = Flightt ("Cairo","PortSaid",19.3,19.5,"MS012",[1, 2, 5, 6])
    f22 = Flightt ("Cairo","Rome",6,9.3,"MS021",[1, 2, 4, 6])
    f23 = Flightt ("Cairo","Shanghai",5.3,19,"MS020",[1, 2, 3, 5])

    f24 = Flightt ("Chicago","London",8,18.32,"DL050",[2, 4, 6, 0])
    f25 = Flightt ("Chicago","London",12.1,22.42,"DL051",[1, 3, 5])
    f26 = Flightt ("Chicago","Miami",10,14.2,"DL046",[1, 2, 3 ,0])
    f27 = Flightt ("Chicago","Miami",17.2,21.4,"DL047",[2, 4])
    f28 = Flightt ("Chicago","NewYork",9,11.18,"DL044",[1, 3, 5, 0])
    f29 = Flightt ("Chicago","NewYork",15,17.18,"DL045",[2, 4])
    f30 = Flightt ("Chicago","Paris",5,16.55,"DL052",[1, 2, 4, 6])
    f31 = Flightt ("Chicago","SanFrancisco",16,22.1,"DL048",[6, 0])
    f32 = Flightt ("Chicago","SanFrancisco",20,2.1,"DL049",[2, 3, 4])
    f33 = Flightt ("Edinburgh","London",7,8.15,"BA128",[1, 2, 3, 4, 5, 6, 0])
    f34 = Flightt ("Edinburgh","London",19.15,20.3,"BA129",[1, 2, 3, 4, 5, 6, 0])
    f35 = Flightt ("Edinburgh","Paris",14,15.5,"BA130",[1, 3, 4, 5, 0])
    f36 = Flightt ("Edinburgh","SanFrancisco",3,15.1,"BA131",[1, 2, 3, 6])
    f37 = Flightt ("Liverpool","London",4.3,5.3,"BA125",[5, 6, 0])
    f38 = Flightt ("Liverpool","London",10,11,"BA123",[1, 2, 3, 4, 5, 6, 0])
    f39 = Flightt ("Liverpool","London",16,17,"BA124",[1, 2, 3])
    f40 = Flightt ("London","Alexandria",6,11.2,"BA149",[2, 3, 5])
    f41 = Flightt ("London","Cairo",10,14.4,"BA143",[1, 2, 4, 0])
    f42 = Flightt ("London","Cairo",20,0.4,"BA144",[4, 6])
    f43 = Flightt ("London","Chicago",4,12.5,"BA147",[1, 2, 3, 4, 5, 6, 0])
    f44 = Flightt ("London","Edinburgh",5,6.15,"BA134",[1, 2, 3, 4, 5, 6, 0])
    f45 = Flightt ("London","Edinburgh",17,18.15,"BA135",[2, 5, 0])
    f46 = Flightt ("London","Liverpool",8.4,9.4,"BA132",[1, 2, 3, 4, 5, 6, 0])
    f47 = Flightt ("London","Liverpool",21,22,"BA133",[2, 3, 6, 0])

    f48 = Flightt ("London","Lyon",15,16.35,"BA150",[4, 5, 6, 0])
    f49 = Flightt ("London","Manchester",10,11,"BA136",[1, 2, 3, 4, 5, 6, 0])
    f50 = Flightt ("London","NewYork",5,13,"BA138",[1, 2, 3, 4, 5, 6, 0])
    f51 = Flightt ("London","NewYork",14,22,"BA145",[1, 2, 3, 4, 5, 6, 0])
    f52 = Flightt ("London","Paris",6.3,7.4,"BA140",[3, 4, 6, 0])
    f53 = Flightt ("London","Paris",16,17.1,"BA139",[1, 2, 3, 4, 5, 6, 0])
    f54 = Flightt ("London","Rome",17,19.2,"BA141",[1, 2, 3, 4, 5, 6, 0])
    f55 = Flightt ("London","SanFrancisco",15.3,2.3,"BA146",[1, 2, 3, 4, 5, 6, 0])
    f56 = Flightt ("London","Shanghai",4.3,15.3,"BA142",[3, 4, 0])
    f57 = Flightt ("London","Shanghai",11,22,"BA137",[1, 2, 3, 4, 5, 6, 0])
    f58 = Flightt ("London","Tokyo",14,1.4,"BA148",[1, 2, 5, 6])
    f59 = Flightt ("Lyon","Nice",2.1,3,"AF122",[1, 2, 3, 4, 5, 6, 0])
    f60 = Flightt ("Lyon","Nice",13.3,14.2,"AF121",[1, 4, 5, 6, 0])
    f61 = Flightt ("Lyon","Paris",9,10.05,"AF119",[1, 2, 3, 4, 5, 6, 0])
    f62 = Flightt ("Lyon","Paris",18,19.05,"AF120",[1, 2, 3, 4, 5, 6, 0])
    f63 = Flightt ("Manchester","London",11.3,12.3,"BA126",[1, 2, 3, 4, 5, 6, 0])
    f64 = Flightt ("Manchester","London",18.3,19.3,"BA127",[1, 2, 3, 4, 5])

    f65 = Flightt ("Miami","Chicago",8,12.2,"DL056",[3, 5, 0])
    f66 = Flightt ("Miami","NewYork",10,12.55,"DL053",[2, 3 ,4])
    f67 = Flightt ("Miami","NewYork",16,18.55,"DL054",[5, 6, 0])
    f68 = Flightt ("Miami","SanFrancisco",10,16.25,"DL055",[1, 2, 3, 5])

    f69 = Flightt ("Milan","London",14,15.5,"AZ103",[1, 2, 3, 4, 5, 6, 0])
    f70 = Flightt ("Milan","Paris",10,11.2,"AZ101",[1, 2, 4, 5])
    f71 = Flightt ("Milan","Paris",16,17.2,"AZ102",[3, 0])
    f72 = Flightt ("Milan","Rome",1,2.05,"AZ104",[3, 6, 0])
    f73 = Flightt ("Milan","Rome",7,8.05,"AZ099",[1, 2, 3, 4, 5, 6, 0])
    f74 = Flightt ("Milan","Rome",17,18.05,"AZ100",[1, 2, 3, 4, 5, 6, 0])
    
    f75 = Flightt ("NewYork","Chicago",7,9.18,"DL028",[1, 3, 4])
    f76 = Flightt ("NewYork","Chicago",13.2,15.38,"DL029",[1, 2, 6])
    f77 = Flightt ("NewYork","Edinburgh",6,15.05,"DL038",[2, 5, 0])
    f78 = Flightt ("NewYork","London",4,10.5,"DL037",[1, 3, 4, 6])
    f79 = Flightt ("NewYork","Lyon",13,22.12,"DL041",[1, 3, 4])
    f80 = Flightt ("NewYork","Miami",1,3.55,"DL036",[4])
    f81 = Flightt ("NewYork","Miami",7.15,10.1,"DL035",[5, 6, 0])
    f82 = Flightt ("NewYork","Miami",12,14.55,"DL034",[1, 2, 3])
    f83 = Flightt ("NewYork","Paris",11,17.5,"DL040",[2, 5, 6, 0])
    f84 = Flightt ("NewYork","Rome",10.15,18.3,"DL039",[1, 3, 4, 6])
    f85 = Flightt ("NewYork","SanFrancisco",8,14.32,"DL030",[2, 3])
    f86 = Flightt ("NewYork","SanFrancisco",10,16.32,"DL031",[5, 0])
    f87 = Flightt ("NewYork","SanFrancisco",18,0.32,"DL032",[6])
    f88 = Flightt ("NewYork","SanFrancisco",23.3,6.02,"DL033",[1, 4])
    f89 = Flightt ("NewYork","Shanghai",5,19.5,"DL043",[1, 3, 5, 0])
    f90 = Flightt ("NewYork","Tokyo",0,13.45,"DL042",[1, 2, 4, 6])

    f91 = Flightt ("Nice","Lyon",20,20.5,"AF118",[1, 2, 3, 4, 5, 6, 0])
    f92 = Flightt ("Nice","Paris",5,6.2,"AF117",[1, 2, 3, 4, 5, 6, 0])
    f93 = Flightt ("Nice","Paris",14.3,15.5,"AF116",[1, 2, 0])

    f94 = Flightt ("Paris","London",9,10.05,"AF105",[1, 2, 3, 4, 5, 6, 0])
    f95 = Flightt ("Paris","London",22,23.05,"AF106",[1, 2, 3, 4, 5, 6, 0])
    f96 = Flightt ("Paris","Lyon",7,8.1,"AF114",[3, 4, 5, 6])
    f97 = Flightt ("Paris","Lyon",14,15.1,"AF115",[1, 2, 3, 4, 5, 6, 0])
    f98 = Flightt ("Paris","NewYork",12,20.3,"AF107",[1, 2, 3, 4, 5, 6, 0])
    f99 = Flightt ("Paris","NewYork",17.3,2,"AF108",[1, 2, 0])
    f100 = Flightt ("Paris","Nice",11,12.2,"AF112",[1, 2, 3, 4, 5, 6, 0])
    f101 = Flightt ("Paris","Nice",16,17.2,"AF113",[1, 2, 3, 4, 5, 6, 0])
    f102 = Flightt ("Paris","Rome",10,12,"AF110",[1, 2, 3, 4, 5, 6, 0])
    f103 = Flightt ("Paris","Rome",18,20,"AF109",[2, 4, 5, 0])
    f104 = Flightt ("Paris","Shanghai",4,15.55,"AF111",[1, 3])

    f105 = Flightt ("PortSaid","Alexandria",12,12.3,"MS026",[2, 3, 5])
    f106 = Flightt ("PortSaid","Alexandria",14.45,15.15,"MS027",[1, 4, 6])
    f107 = Flightt ("PortSaid","Cairo",11,11.2,"MS024",[1, 3])
    f108 = Flightt ("PortSaid","Cairo",14.1,14.3,"MS025",[5, 0])

    f109 = Flightt ("Rome","London",1,3.3,"AZ091",[1, 2, 3, 4, 5, 6, 0])
    f110 = Flightt ("Rome","London",11.3,14,"AZ090",[1, 2, 3, 4, 5, 6, 0])
    f111 = Flightt ("Rome","Milan",8,9.05,"AZ094",[1, 2, 3, 4, 5, 6, 0])
    f112 = Flightt ("Rome","Milan",22,23.05,"AZ095",[3, 5, 6, 0])
    f113 = Flightt ("Rome","NewYork",4,13.48,"AZ088",[1, 2, 3, 4, 5, 6, 0])
    f114 = Flightt ("Rome","NewYork",17,2.48,"AZ089",[4, 5, 0])
    f115 = Flightt ("Rome","Paris",8,10,"AZ086",[1, 2, 3, 4, 5, 6, 0])
    f116 = Flightt ("Rome","Paris",20,22,"AZ087",[3, 4, 6, 0])
    f117 = Flightt ("Rome","Venice",11,12,"AZ092",[1, 2, 3, 4, 5, 6, 0])
    f118 = Flightt ("Rome","Venice",18,19,"AZ093",[1, 3, 5, 0])

    f119 = Flightt ("SanFrancisco","Chicago",7,13.1,"DL059",[4, 5, 6])
    f120 = Flightt ("SanFrancisco","Chicago",14,20.1,"DL060",[1, 2, 0])
    f121 = Flightt ("SanFrancisco","Miami",11,17.25,"DL061",[2, 3 ,5, 6])
    f122 = Flightt ("SanFrancisco","NewYork",6,12.32,"DL057",[5, 6, 0])
    f123 = Flightt ("SanFrancisco","NewYork",13,19.32,"DL058",[1, 2, 3])

    f124 = Flightt ("Shanghai","Cairo",2,16.3,"CA070",[1, 2, 3, 4, 5, 6, 0])
    f125 = Flightt ("Shanghai","Cairo",7,21.3,"CA068",[1, 2, 3, 4, 5, 6, 0])
    f126 = Flightt ("Shanghai","Cairo",13.3,4,"CA069",[1, 2, 3, 4, 5, 6, 0])
    f127 = Flightt ("Shanghai","Chicago",6,19.45,"CA080",[1, 2, 3, 4, 5, 6, 0])
    f128 = Flightt ("Shanghai","Chicago",15,4.45,"CA081",[1, 2, 3, 4, 5, 6, 0])
    f129 = Flightt ("Shanghai","London",0.4,13.2,"CA071",[1, 2, 3, 4, 5, 6, 0])
    f130 = Flightt ("Shanghai","London",5.3,18.1,"CA072",[1, 2, 3, 4, 5, 6, 0])
    f131 = Flightt ("Shanghai","London",14,2.4,"CA073",[1, 2, 3, 4, 5, 6, 0])
    f132 = Flightt ("Shanghai","NewYork",1,15.5,"CA079",[1, 2, 3, 4, 5, 6, 0])
    f133 = Flightt ("Shanghai","NewYork",10,0.5,"CA078",[1, 2, 3, 4, 5, 6, 0])
    f134 = Flightt ("Shanghai","Paris",2,14.25,"CA076",[1, 2, 3, 4, 5, 6, 0])
    f135 = Flightt ("Shanghai","Paris",8,20.25,"CA077",[1, 2, 3, 4, 5, 6, 0])
    f136 = Flightt ("Shanghai","Rome",6,19.1,"CA074",[1, 2, 3, 4, 5, 6, 0])
    f137 = Flightt ("Shanghai","Rome",17,6.1,"CA075",[1, 2, 3, 4, 5, 6, 0])
    f138 = Flightt ("Shanghai","Tokyo",5,7.5,"CA085",[1, 2, 3, 4, 5, 6, 0])
    f139 = Flightt ("Shanghai","Tokyo",12,14.5,"CA082",[1, 2, 3, 4, 5, 6, 0])
    f140 = Flightt ("Shanghai","Tokyo",16,18.5,"CA083",[1, 2, 3, 4, 5, 6, 0])
    f141 = Flightt ("Shanghai","Tokyo",21,23.5,"CA084",[1, 2, 3, 4, 5, 6, 0])

    f142 = Flightt ("Tokyo","SanFrancisco",12,21.05,"JL066",[1, 2, 3, 5, 6])
    f143 = Flightt ("Tokyo","SanFrancisco",22,7.05,"JL067",[1, 3, 4, 6, 0])
    f144 = Flightt ("Tokyo","Shanghai",0,2.5,"JL063",[2, 4, 6, 0])
    f145 = Flightt ("Tokyo","Shanghai",6.1,9,"JL064",[2, 3, 4, 5])
    f146 = Flightt ("Tokyo","Shanghai",9,11.5,"JL065",[1, 6, 0])
    f147 = Flightt ("Tokyo","Shanghai",20,22.5,"JL062",[1, 2, 3, 5])

    f148 = Flightt ("Venice","Rome",5,6,"AZ096",[1, 2, 3, 4, 5, 6, 0])
    f149 = Flightt ("Venice","Rome",14,15,"AZ097",[1, 2, 3, 4, 5, 6, 0])
    f150 = Flightt ("Venice","Rome",19.4,20.4,"AZ098",[1, 2, 3, 4, 5, 6, 0])

    FlightList = []

    FlightList.append(f1)
    FlightList.append(f2)
    FlightList.append(f3)
    FlightList.append(f4)
    FlightList.append(f5)
    FlightList.append(f6)
    FlightList.append(f7)
    FlightList.append(f8)
    FlightList.append(f9)
    FlightList.append(f10)
    FlightList.append(f11)
    FlightList.append(f12)
    FlightList.append(f13)
    FlightList.append(f14)
    FlightList.append(f15)
    FlightList.append(f16)
    FlightList.append(f17)
    FlightList.append(f18)
    FlightList.append(f19)
    FlightList.append(f20)
    FlightList.append(f21)
    FlightList.append(f22)
    FlightList.append(f23)
    FlightList.append(f24)
    FlightList.append(f25)
    FlightList.append(f26)
    FlightList.append(f27)
    FlightList.append(f28)
    FlightList.append(f29)
    FlightList.append(f30)
    FlightList.append(f31)
    FlightList.append(f32)
    FlightList.append(f33)
    FlightList.append(f34)
    FlightList.append(f35)
    FlightList.append(f36)
    FlightList.append(f37)
    FlightList.append(f38)
    FlightList.append(f39)
    FlightList.append(f40)
    FlightList.append(f41)
    FlightList.append(f42)
    FlightList.append(f43)
    FlightList.append(f44)
    FlightList.append(f45)
    FlightList.append(f46)
    FlightList.append(f47)
    FlightList.append(f48)
    FlightList.append(f49)
    FlightList.append(f50)
    FlightList.append(f51)
    FlightList.append(f52)
    FlightList.append(f53)
    FlightList.append(f54)
    FlightList.append(f55)
    FlightList.append(f56)
    FlightList.append(f57)
    FlightList.append(f58)
    FlightList.append(f59)
    FlightList.append(f60)
    FlightList.append(f61)
    FlightList.append(f62)
    FlightList.append(f63)
    FlightList.append(f64)
    FlightList.append(f65)
    FlightList.append(f66)
    FlightList.append(f67)
    FlightList.append(f68)
    FlightList.append(f69)
    FlightList.append(f70)
    FlightList.append(f71)
    FlightList.append(f72)
    FlightList.append(f73)
    FlightList.append(f74)
    FlightList.append(f75)
    FlightList.append(f76)
    FlightList.append(f77)
    FlightList.append(f78)
    FlightList.append(f79)
    FlightList.append(f80)
    FlightList.append(f81)
    FlightList.append(f82)
    FlightList.append(f83)
    FlightList.append(f84)
    FlightList.append(f85)
    FlightList.append(f86)
    FlightList.append(f87)
    FlightList.append(f88)
    FlightList.append(f89)
    FlightList.append(f90)
    FlightList.append(f91)
    FlightList.append(f92)
    FlightList.append(f93)
    FlightList.append(f94)
    FlightList.append(f95)
    FlightList.append(f96)
    FlightList.append(f97)
    FlightList.append(f98)
    FlightList.append(f99)
    FlightList.append(f100)
    FlightList.append(f101)
    FlightList.append(f102)
    FlightList.append(f103)
    FlightList.append(f104)
    FlightList.append(f105)
    FlightList.append(f106)
    FlightList.append(f107)
    FlightList.append(f108)
    FlightList.append(f109)
    FlightList.append(f110)
    FlightList.append(f111)
    FlightList.append(f112)
    FlightList.append(f113)
    FlightList.append(f114)
    FlightList.append(f115)
    FlightList.append(f116)
    FlightList.append(f117)
    FlightList.append(f118)
    FlightList.append(f119)
    FlightList.append(f120)
    FlightList.append(f121)
    FlightList.append(f122)
    FlightList.append(f123)
    FlightList.append(f124)
    FlightList.append(f125)
    FlightList.append(f126)
    FlightList.append(f127)
    FlightList.append(f128)
    FlightList.append(f129)
    FlightList.append(f130)
    FlightList.append(f131)
    FlightList.append(f132)
    FlightList.append(f133)
    FlightList.append(f134)
    FlightList.append(f135)
    FlightList.append(f136)
    FlightList.append(f137)
    FlightList.append(f138)
    FlightList.append(f139)
    FlightList.append(f140)
    FlightList.append(f141)
    FlightList.append(f142)
    FlightList.append(f143)
    FlightList.append(f144)
    FlightList.append(f145)
    FlightList.append(f146)
    FlightList.append(f147)
    FlightList.append(f148)
    FlightList.append(f149)
    FlightList.append(f150)

    Cities = ["Alexandria", "Aswan", "Cairo", "Chicago", "Edinburgh", 
                "Liverpool", "London", "Lyon", "Manchester", "Miami", 
                "Milan", "NewYork", "Nice", "Paris", "PortSaid", 
                "Rome", "SanFrancisco", "Shanghai", "Tokyo", "Venice"]
    CitiesCity = []
    Alex = city("Alexandria", 31.2, 29.95)
    Aswan = city("Aswan", 24.0875, 32.8989)
    Cairo = city("Cairo", 30.05, 31.25)
    Chicago = city("Chicago", 41.8373, -87.6862)
    Edinburgh = city("Edinburgh", 55.9483, -3.2191)
    Liverpool = city("Liverpool", 53.416, -2.918)
    London = city("London", 51.5, 31.25)
    Lyon = city("Lyon", 45.77, 4.83)   
    Manchester = city("Manchester", 53.5004, -2.248)
    Miami = city("Miami", 25.7839, -80.2102)
    Milan = city("Milan", 45.47, 9.205)
    NewYork = city("NewYork", 40.6943, -73.9249)
    Nice = city("Nice", 43.715, 7.265)
    Paris = city("Paris", 48.8667, 2.3333)
    PortSaid = city("PortSaid", 31.26, 32.29)
    Rome = city("Rome", 41.896, 12.4833)
    SanFrancisco = city("SanFrancisco", 37.7562, -122.443)
    Shanghai = city("Shanghai", 31.2165, 121.4365)
    Tokyo = city("Tokyo", 35.685, 139.7514)
    Venice = city("Venice", 45.4387, 12.335)

    CitiesCity.append(Alex)
    CitiesCity.append(Aswan)
    CitiesCity.append(Cairo)
    CitiesCity.append(Chicago)
    CitiesCity.append(Edinburgh)
    CitiesCity.append(Liverpool)
    CitiesCity.append(London)
    CitiesCity.append(Lyon)
    CitiesCity.append(Manchester)
    CitiesCity.append(Miami)
    CitiesCity.append(Milan)
    CitiesCity.append(NewYork)
    CitiesCity.append(Nice)
    CitiesCity.append(Paris)
    CitiesCity.append(PortSaid)
    CitiesCity.append(Rome)
    CitiesCity.append(SanFrancisco)
    CitiesCity.append(Shanghai)
    CitiesCity.append(Tokyo)
    CitiesCity.append(Venice)

    # Here takes the input and splits it
    list_of_inputs = input("Please enter Source City, Destination City and Days all separated by a space: ").split()

    SourceCity = list_of_inputs[0]
    DistenationCity = list_of_inputs[1]
    list_of_inputs = list_of_inputs[2:]

    listOfDays = []
    for i in range(len(list_of_inputs)):
        listOfDays.append(list_of_inputs[i])
    #print(listOfDays)

    days = []
    for i in listOfDays:
        if i == "Friday":
            days.append(0)
        elif i == "Saturday":
            days.append(1)
        elif i == "Sunday":
            days.append(2)
        elif i == "Monday":
            days.append(3)
        elif i == "Tuesday":
            days.append(4)
        elif i == "Wednesday":
            days.append(5)
        elif i == "Thursday":
            days.append(6)

    cityNamesInPath.append(SourceCity)
    DistenationCityi = Cities.index(DistenationCity)  

    graph.connect(f1,f1.getFlightDestance())
    graph.connect(f2,f2.getFlightDestance())
    graph.connect(f3,f3.getFlightDestance())
    graph.connect(f4,f4.getFlightDestance())
    graph.connect(f5,f5.getFlightDestance())
    graph.connect(f6,f6.getFlightDestance())
    graph.connect(f7,f7.getFlightDestance())
    graph.connect(f8,f8.getFlightDestance())
    graph.connect(f9,f9.getFlightDestance())
    graph.connect(f10,f10.getFlightDestance())
    graph.connect(f11,f11.getFlightDestance())
    graph.connect(f12,f12.getFlightDestance())
    graph.connect(f13,f13.getFlightDestance())
    graph.connect(f14,f14.getFlightDestance())
    graph.connect(f15,f15.getFlightDestance())
    graph.connect(f16,f16.getFlightDestance())
    graph.connect(f17,f17.getFlightDestance())
    graph.connect(f18,f18.getFlightDestance())
    graph.connect(f19,f19.getFlightDestance())
    graph.connect(f20,f20.getFlightDestance())
    graph.connect(f21,f21.getFlightDestance())
    graph.connect(f22,f22.getFlightDestance())
    graph.connect(f23,f23.getFlightDestance())
    graph.connect(f24,f24.getFlightDestance())
    graph.connect(f25,f25.getFlightDestance())
    graph.connect(f26,f26.getFlightDestance())
    graph.connect(f27,f27.getFlightDestance())
    graph.connect(f28,f28.getFlightDestance())
    graph.connect(f29,f29.getFlightDestance())
    graph.connect(f30,f30.getFlightDestance())
    graph.connect(f31,f31.getFlightDestance())
    graph.connect(f32,f32.getFlightDestance())
    graph.connect(f33,f33.getFlightDestance())
    graph.connect(f34,f34.getFlightDestance())
    graph.connect(f35,f35.getFlightDestance())
    graph.connect(f36,f36.getFlightDestance())
    graph.connect(f37,f37.getFlightDestance())
    graph.connect(f38,f38.getFlightDestance())
    graph.connect(f39,f39.getFlightDestance())
    graph.connect(f40,f40.getFlightDestance())
    graph.connect(f41,f41.getFlightDestance())
    graph.connect(f42,f42.getFlightDestance())
    graph.connect(f43,f43.getFlightDestance())
    graph.connect(f44,f44.getFlightDestance())
    graph.connect(f45,f45.getFlightDestance())
    graph.connect(f46,f46.getFlightDestance())
    graph.connect(f47,f47.getFlightDestance())
    graph.connect(f48,f48.getFlightDestance())
    graph.connect(f49,f49.getFlightDestance())
    graph.connect(f50,f50.getFlightDestance())
    graph.connect(f51,f51.getFlightDestance())
    graph.connect(f52,f52.getFlightDestance())
    graph.connect(f53,f53.getFlightDestance())
    graph.connect(f54,f54.getFlightDestance())
    graph.connect(f55,f55.getFlightDestance())
    graph.connect(f56,f56.getFlightDestance())
    graph.connect(f57,f57.getFlightDestance())
    graph.connect(f58,f58.getFlightDestance())
    graph.connect(f59,f59.getFlightDestance())
    graph.connect(f60,f60.getFlightDestance())
    graph.connect(f61,f61.getFlightDestance())
    graph.connect(f62,f62.getFlightDestance())
    graph.connect(f63,f63.getFlightDestance())
    graph.connect(f64,f64.getFlightDestance())
    graph.connect(f65,f65.getFlightDestance())
    graph.connect(f66,f66.getFlightDestance())
    graph.connect(f67,f67.getFlightDestance())
    graph.connect(f68,f68.getFlightDestance())
    graph.connect(f69,f69.getFlightDestance())
    graph.connect(f70,f70.getFlightDestance())
    graph.connect(f71,f71.getFlightDestance())
    graph.connect(f72,f72.getFlightDestance())
    graph.connect(f73,f73.getFlightDestance())
    graph.connect(f74,f74.getFlightDestance())
    graph.connect(f75,f75.getFlightDestance())
    graph.connect(f76,f76.getFlightDestance())
    graph.connect(f77,f77.getFlightDestance())
    graph.connect(f78,f78.getFlightDestance())
    graph.connect(f79,f79.getFlightDestance())
    graph.connect(f80,f80.getFlightDestance())
    graph.connect(f81,f81.getFlightDestance())
    graph.connect(f82,f82.getFlightDestance())
    graph.connect(f83,f83.getFlightDestance())
    graph.connect(f84,f84.getFlightDestance())
    graph.connect(f85,f85.getFlightDestance())
    graph.connect(f86,f86.getFlightDestance())
    graph.connect(f87,f87.getFlightDestance())
    graph.connect(f88,f88.getFlightDestance())
    graph.connect(f89,f89.getFlightDestance())
    graph.connect(f90,f90.getFlightDestance())
    graph.connect(f91,f91.getFlightDestance())
    graph.connect(f92,f92.getFlightDestance())
    graph.connect(f93,f93.getFlightDestance())
    graph.connect(f94,f94.getFlightDestance())
    graph.connect(f95,f95.getFlightDestance())
    graph.connect(f96,f96.getFlightDestance())
    graph.connect(f97,f97.getFlightDestance())
    graph.connect(f98,f98.getFlightDestance())
    graph.connect(f99,f99.getFlightDestance())
    graph.connect(f100,f100.getFlightDestance())
    graph.connect(f101,f101.getFlightDestance())
    graph.connect(f102,f102.getFlightDestance())
    graph.connect(f103,f103.getFlightDestance())
    graph.connect(f104,f104.getFlightDestance())
    graph.connect(f105,f105.getFlightDestance())
    graph.connect(f106,f106.getFlightDestance())
    graph.connect(f107,f107.getFlightDestance())
    graph.connect(f108,f108.getFlightDestance())
    graph.connect(f109,f109.getFlightDestance())
    graph.connect(f110,f110.getFlightDestance())
    graph.connect(f111,f111.getFlightDestance())
    graph.connect(f112,f112.getFlightDestance())
    graph.connect(f113,f113.getFlightDestance())
    graph.connect(f114,f114.getFlightDestance())
    graph.connect(f115,f115.getFlightDestance())
    graph.connect(f116,f116.getFlightDestance())
    graph.connect(f117,f117.getFlightDestance())
    graph.connect(f118,f118.getFlightDestance())
    graph.connect(f119,f119.getFlightDestance())
    graph.connect(f120,f120.getFlightDestance())
    graph.connect(f121,f121.getFlightDestance())
    graph.connect(f122,f122.getFlightDestance())
    graph.connect(f123,f123.getFlightDestance())
    graph.connect(f124,f124.getFlightDestance())
    graph.connect(f125,f125.getFlightDestance())
    graph.connect(f126,f126.getFlightDestance())
    graph.connect(f127,f127.getFlightDestance())
    graph.connect(f128,f128.getFlightDestance())
    graph.connect(f129,f129.getFlightDestance())
    graph.connect(f130,f130.getFlightDestance())
    graph.connect(f131,f131.getFlightDestance())
    graph.connect(f132,f132.getFlightDestance())
    graph.connect(f133,f133.getFlightDestance())
    graph.connect(f134,f134.getFlightDestance())
    graph.connect(f135,f135.getFlightDestance())
    graph.connect(f136,f136.getFlightDestance())
    graph.connect(f137,f137.getFlightDestance())
    graph.connect(f138,f138.getFlightDestance())
    graph.connect(f139,f139.getFlightDestance())
    graph.connect(f140,f140.getFlightDestance())
    graph.connect(f141,f141.getFlightDestance())
    graph.connect(f142,f142.getFlightDestance())
    graph.connect(f143,f143.getFlightDestance())
    graph.connect(f144,f144.getFlightDestance())
    graph.connect(f145,f145.getFlightDestance())
    graph.connect(f146,f146.getFlightDestance())
    graph.connect(f147,f147.getFlightDestance())
    graph.connect(f148,f148.getFlightDestance())
    graph.connect(f149,f149.getFlightDestance())
    graph.connect(f150,f150.getFlightDestance())

    ##################################################################################
    heuristics = {}
    heuristics['Alexandria'] = Alex.calc(Alex.lat, Alex.long, CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Aswan'] = Aswan.calc(Aswan.lat, Aswan.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Cairo'] = Cairo.calc(Cairo.lat, Cairo.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Chicago'] = Chicago.calc(Chicago.lat, Chicago.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Edinburgh'] = Edinburgh.calc(Edinburgh.lat, Edinburgh.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Liverpool'] = Liverpool.calc(Liverpool.lat, Liverpool.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['London'] = London.calc(London.lat, London.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Lyon'] = Lyon.calc(Lyon.lat, Lyon.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Manchester'] = Manchester.calc(Manchester.lat, Manchester.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Miami'] = Miami.calc(Miami.lat, Miami.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Milan'] = Milan.calc(Milan.lat, Milan.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['NewYork'] = NewYork.calc(NewYork.lat, NewYork.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Nice'] = Nice.calc(Nice.lat, Nice.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Paris'] = Paris.calc(Paris.lat, Paris.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['PortSaid'] = PortSaid.calc(PortSaid.lat, PortSaid.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Rome'] = Rome.calc(Rome.lat, Rome.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['SanFrancisco'] = SanFrancisco.calc(SanFrancisco.lat, SanFrancisco.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Shanghai'] = Shanghai.calc(Shanghai.lat, Shanghai.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Tokyo'] = Tokyo.calc(Tokyo.lat, Tokyo.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)
    heuristics['Venice'] = Venice.calc(Venice.lat, Venice.long,CitiesCity[DistenationCityi].lat, CitiesCity[DistenationCityi].long)

    # Run the search algorithm
    path = astar_search(graph, heuristics, SourceCity, DistenationCity)
    #print(path)
    
    days.sort()
    fligtsTaken = []
    fligtsTakenSorted = []
    pathCount = len(path)
    daysFlights = []

    flightsTakenII = []
    FlightsTakenFunction(pathCount, FlightList, days, path, fligtsTaken, DistenationCity, flightsTakenII)

    for k in range(0, len(flightsTakenII)-1):
        for d in days:
            if d in flightsTakenII[k].flightListOfDays and d in flightsTakenII[k+1].flightListOfDays: # 
                if flightsTakenII[k].flightArrivalTime < flightsTakenII[k+1].flightDepartureTime and len(fligtsTakenSorted) != 0 and fligtsTakenSorted[k-1].flightSourceCity != flightsTakenII[k].flightSourceCity:
                    firstFlight = flightsTakenII[k]
                    fligtsTakenSorted.append(firstFlight)
                    daysFlights.append(d)
                elif flightsTakenII[k+1].flightArrivalTime < flightsTakenII[k].flightDepartureTime and len(fligtsTakenSorted) != 0 and fligtsTakenSorted[k-1].flightSourceCity != flightsTakenII[k+1].flightSourceCity:
                    firstFlight = flightsTakenII[k+1]
                    fligtsTakenSorted.append(firstFlight)
                    daysFlights.append(d)
            elif d in flightsTakenII[k].flightListOfDays: # 
                firstFlight = flightsTakenII[k]
                fligtsTakenSorted.append(firstFlight)
                daysFlights.append(d)
                break
            elif d in flightsTakenII[k+1].flightListOfDays: # 
                secondFlight = flightsTakenII[k+1]
                fligtsTakenSorted.append(secondFlight) 
                daysFlights.append(d)
                break

    for d in days:
        if d in flightsTakenII[len(flightsTakenII)-1].flightListOfDays and len(flightsTakenII) == 1:
            fligtsTakenSorted.append(flightsTakenII[len(flightsTakenII)-1])
            daysFlights.append(d)
            break

    daysReverse = []
    for i in daysFlights:
        if i == 0:
            daysReverse.append("Friday")
        elif i == 1:
            daysReverse.append("Saturday")       
        elif i == 2:
            daysReverse.append("Sunday")
        elif i == 3:
            daysReverse.append("Monday")
        elif i == 4:
            daysReverse.append("Tuesday")
        elif i == 5:
            daysReverse.append("Wednesday")
        elif i == 6:
            daysReverse.append("Thursday")

    if len(fligtsTakenSorted) > 1:
        if fligtsTakenSorted[len(fligtsTakenSorted)-1].flightDestinationCity == DistenationCity:
            for x in range(0, len(fligtsTakenSorted)):
                i = x + 1
                print( "Step", i, ": on", daysReverse[x], 
                    "use flight", fligtsTakenSorted[x].flightNumber, "from", fligtsTakenSorted[x].flightSourceCity, "to",
                    fligtsTakenSorted[x].flightDestinationCity, ". Departure Time", fligtsTakenSorted[x].flightDepartureTime, 
                    "and arrival time", fligtsTakenSorted[x].flightArrivalTime, "." )
        else:
            print("No path was found on the specified cities or days!")
    elif len(fligtsTakenSorted) == 1 and fligtsTakenSorted[0].flightDestinationCity == DistenationCity and fligtsTakenSorted[0].flightSourceCity == SourceCity: 
        print( "Step", 1, ": on", daysReverse[0], 
                    "use flight", fligtsTakenSorted[0].flightNumber, "from", fligtsTakenSorted[0].flightSourceCity, "to",
                    fligtsTakenSorted[0].flightDestinationCity, ". Departure Time", fligtsTakenSorted[0].flightDepartureTime, 
                    "and arrival time", fligtsTakenSorted[0].flightArrivalTime, "." )
    else:
        print("No path was found on the specified cities or days!")

# Tell python to run main method
if __name__ == "__main__": main()