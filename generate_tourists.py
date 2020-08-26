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

    def process_input_data(self):
        for i in range(1,6000):
            self._people.append(self.new_person())

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
                    if ill and len(self._illness[1:]) > 0:
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

    def create_age(self, agemin, agemax):
        counter = 0
        while True:
            a = round(random.uniform(agemin, agemax))
            m = min(int(a / 5), len(self._magicA) - 1)
            if self._magicA[m] > 0:
                break
            else:
                counter = counter + 1
                if counter > 50:
                    break

        for i in range(0, len(self._agegroups)):
            if self._agegroups[i][0] <= a <= self._agegroups[i][1]:
                break

        return a

    def new_person(self):
        '''
        Construct a person

        :param locs: Residential location
        :param sex: Gender
        :param age: Age
        :return: The new person
        '''
        cur_age_group = random.choice(range(2, 4))
        age = self.create_age(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1])
        person = {}
        person['age'] = age
        person['sex'] = self._agecode[round(random.uniform(0, 1))]
        person['preCond'] = self.gen_illness(age)
        person['SIRD'] = "S"
        person['typeID'] = 9
        person['locations'] = []
        person['famtype'] = 0
        person['famid'] = -1
        return person

    def get_people(self):
        return self._people


def generate_agents(magic, illness):
    adatok = DataSet()
    adatok.load_magicnumber(magic)
    adatok.load_illnessnumber(illness)
    adatok.process_input_data()
    return adatok.get_people()

