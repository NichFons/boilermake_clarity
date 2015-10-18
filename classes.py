# Classes.py #################################
# Contains Classes for Persons and Incidents #
# Will also contain class helper             #
# functions and class sorting functions.     #
##############################################

class Incident():
    def __init__(self, perps, date, time, location, victs, crime, people):
        self.date = date		# MM/DD/YYYY
        self.time = time		# HH:MM:SS XM
        self.location = location	# Yeah whatever it says
        self.victs = victs		# List of victs
        self.perps = perps		# List of perps
        self.factions = [[],[]]		# Perp facs, vict facs
        self.crime = crime
        self.alls = self.victs + self.perps
    def up(self, people):
        self.victs = [people[i] for i in self.victs]
        self.perps = [people[i] for i in self.perps]
        self.factions[0] = [i.faction for i in self.victs]
        self.factions[1] = [i.faction for i in self.perps]
#	self.ages = [int((i.birth_date.split('/'))[2]) - int((date.split('/'))[2]) for i in (self.victs + self.perps)]
    def __str__(self):
        return "On " + self.date + " at " + self.time + ", " + " ".join(self.alls) + " were involved "\
               + "with the crime "  + str(self.crime)
        
        

class Person():
    def __init__(self, finger, last, first, gender, faction, vict_case, perp_case, birth_date):
        self.finger = finger
	self.last = last
        self.first = first
        self.gender = gender
        self.faction = faction
        self.vict_case = vict_case
        self.perp_case = perp_case
        self.birth_date = birth_date
    def __str__(self):
        return self.first + " " + self.last + " is a " + self.gender + " of faction " + \
               str(self.faction)

def read_from_vict(filename, people):
    victs = people
    with open(filename) as f:
        f.readline()
        for line in f:
            line.strip('\n')
            splitt = line.split(',')
	    try:
		victs[splitt[2]].vict_case.append(splitt[-1])
	    except KeyError:
                victs[splitt[2]] = Person(splitt[2], splitt[4], splitt[3],
		      splitt[6], 0, [splitt[8]], [], splitt[5])
    return victs

def read_from_arrest(filename, people):
    arrest = people
    with open(filename) as f:
        f.readline()
        for line in f:

            line.strip('\n')
            splitt = line.split(',')
            while type(splitt[3]) != int:
                try:
                    splitt[3] = int(splitt[3])
                except:
#                    print(splitt[3])
                    splitt[2] += splitt.pop(3)
            splitt[3] = str(splitt[3])
#            print(" ".join(splitt))
	    try:
		arrest[splitt[3]].perp_case.append(splitt[-1])
                arrest[splitt[3]].faction = splitt[7]
	    except KeyError:
                if splitt[8] == '': 
		    splitt[8] = 0
                arrest[splitt[3]] = Person(splitt[3], splitt[5], splitt[4],
		      splitt[7], splitt[8],[] , [splitt[-1]], splitt[6])
        
    return arrest

#self, perps, date, time, location, victs, perps, crime):

def read_cases(filename1, filename2, people):
    cases = {}
    with open(filename1) as f:
        f.readline()
        for line in f:
            line.strip("\r\n")

            splitt = line.split(',')
	    splitt[-1] = splitt[-1][:-2]	
	    try:
		cases[splitt[-1]].victs.append(splitt[2])
	    except KeyError:
                cases[splitt[-1]] = Incident([], splitt[1].split()[0], splitt[1].split()[1],
		      '', [splitt[2]], 0, people)
    with open(filename2) as f:
        f.readline()
        for line in f:
            splitt = line.split(',')
            splitt[-1] = splitt[-1][:-2]
            while type(splitt[3]) != int:
                try:
                    splitt[3] = int(splitt[3])
                except:
#                    print(splitt[3])
                    splitt[2] += splitt.pop(3)
            splitt[3] = str(splitt[3])
#
	    try:
		cases[splitt[-1]].perps.append(splitt[3])
                cases[splitt[-1]].location = splitt[2]
                cases[splitt[-1]].crime = splitt[-2]
	    except KeyError:
                cases[splitt[-1]] = Incident([splitt[3]], splitt[1].split()[0], 
                      splitt[1].split()[1], splitt[2], [], splitt[-2], people)
    for key in cases:
        cases[key].up(people)
    return cases

     
if __name__ == '__main__':
    people = {}
    people = read_from_vict("data/FICT_VICTIM_DATA.csv", people)
    people = read_from_arrest("data/FICT_ARREST_DATA.csv", people)
    cases  = read_cases("data/FICT_VICTIM_DATA.csv","data/FICT_ARREST_DATA.csv", people)
#    print(people)
#    print(cases)
    for k, v in cases.items():
        print(v)
    for k, v in people.items():
        print(v)

