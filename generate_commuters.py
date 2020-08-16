import csv
import json
import random
import sys
import useful_library

class DataSet:

    _agegroups = [[6, 14],
                  [15, 18],
                  [19, 30],
                  [31, 62]]
    _agecode = ["F", "M"]

    def __init__(self):
        self._residents = None
        self._people = []

    def load_magicnumber(self, magic):
        self._magicA = magic
    
    def load_illnessnumber(self, filename):
        with open(filename, 'r') as f:
            magics = json.load(f)
            self._age_separation = magics["age_separation"]
            self._age_percentage = magics["age_percentage"]
            self._illness_number = magics["illness_number"]
            self._illness = ["a70", "CV", "CK", "COPD", "DM"]

    def process_input_data(self, comcsv, comscsv):
        data = []

        with open(comcsv, encoding="UTF-8") as csvfile:
            cfile = csv.reader(csvfile, dialect='excel', delimiter=";")
            skip = True
            for row in cfile:
                if skip:
                    skip = False
                    continue
                places = {'id': row[0],
                        'type': 2,
                        'subtype': 0,
                        'coordinates': [21.1, 47.1],
                        'coordinates_alt': [120000, 740000],
                        'area': 0,
                        'stat': 'ON',
                        'capacity': int(row[1])
                        }
                data.append(places)
                rloc = {"typeID": 2,
                        "locID": row[0],
                        "coordinates": [21.1, 47.1],
                        "coordinates_alt": [120000, 740000]
                        }
                for i in range(int(row[1])):
                    self._people.append(self.new_person(rloc, -1))
        self._residents = data
        dummy_loc_for_students = data[0]['id']
        schools = []
        with open(comscsv, encoding="UTF-8") as csvfile:
            cfile = csv.reader(csvfile, dialect='excel', delimiter=";")
            skip = True
            for row in cfile:
                if skip:
                    skip = False
                    continue
                schools.append(int(row[1]))
                schools.append(int(row[2]))
                schools.append(int(row[3]))
                schools.append(int(row[4]))
                schools.append(int(row[5]))
                rloc = {"typeID": 2,
                        "locID": dummy_loc_for_students,
                        "coordinates": [21.1, 47.1],
                        "coordinates_alt": [120000, 740000]
                        }
                for j in range(len(schools)):
                    for i in range(schools[j]):
                        self._people.append(self.new_person(rloc, j))
        
    
    def occupation_switch(self, i):
        switcher=useful_library.Switch({
            range(0, 3):1, #Infant
            range(3, 7):2, #Kindergarden student
            range(7, 15):3, #Elemntary school student
            range(15, 19):4, #Highschool student
            #:5, #University student (just temp now)
            range(19, 65):6, #Full time worker, standard 9-17 schedule, fixed workplace
            #:7, #Afternoon shift worker
            range(65, 200):8 #Stay-at-home schedule
            })
        return switcher[i]
    
    def gen_illness(self, age):
        illness = ''
        if age > 70:
            illness = self._illness[0]
            self._illness_number[0] = self._illness_number[0] - 1
        else:
            i = 0
            for a_sep in self._age_separation:
                if age <= a_sep:
                    ill = useful_library.choose_percentage(self._age_percentage[i])
                    if ill and len(self._illness[1:])>0:
                        illness = random.choice(self._illness[1:])
                        self._illness_number[self._illness.index(illness)] = \
                            self._illness_number[self._illness.index(illness)] - 1
                        if self._illness_number[self._illness.index(illness)] == 0:
                            self._illness_number.remove(0)
                            self._illness.remove(illness)
                    break
                i = i + 1
        if illness == '':
            illness = 0
        return illness
    
    def create_age(self, agemin, agemax, ageg):
        counter = 0
        while True:
            a = round(random.uniform(agemin, agemax))
            m = min(int(a/5), len(self._magicA)-1)
            if self._magicA[m]>0:
                break
            else:
                counter = counter + 1
                if counter > 50:
                    break

        g = 0
        for i in range(0, len(self._agegroups)):
            if self._agegroups[i][0] <= a <= self._agegroups[i][1]:
                g = i
                break

        # if not (ageg == g):
        #     print("Baj van: requested: ", ageg, " generated: ", g, " min: ", agemin, " max: ", agemax, " age: ", a)

        return a

    def new_person(self, locs, kid_age):
        '''
        Construct a person

        :param locs: Residential location
        :param sex: Gender
        :param age: Age
        :return: The new person
        '''
        cur_age_group = random.choice(range(2, 4))
        if kid_age == 0:
            cur_age_group = 0
        if kid_age > 0:
            cur_age_group = 1
        age = self.create_age(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1], cur_age_group)
        person = {}
        person['age'] = age
        person['sex'] = self._agecode[round(random.uniform(0, 1))]
        person['preCond'] = self.gen_illness(age)
        person['SIRD'] = "S"
        person['typeID'] = self.occupation_switch(age)
        person['locations'] = []
        person['locations'].append(dict(locs))
        person['famtype'] = 0
        person['famid'] = -1
        return person
    
    def get_people(self):
        return self._people


def generate_agents(comcsv, comscsv, magic, illness):

    adatok = DataSet()
    adatok.load_magicnumber(magic)
    adatok.load_illnessnumber(illness)
    adatok.process_input_data(comcsv, comscsv)
    return adatok.get_people()

