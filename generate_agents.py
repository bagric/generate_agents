import json
import random
import sys
import generate_commuters
import generate_tourists
import useful_library

def between(r, table):
    '''
    Helper function to convert probabilities to indices

    :param r: Actual random value
    :param table: Probability table
    :return: The index of interval calculated based on the table
    '''
    ret = [0] + table
    for i in range(1, len(ret)):
        ret[i] = ret[i] + ret[i - 1]
    for i in range(0, len(ret) - 1):
        if ret[i] <= r < ret[i + 1]:
            return i

def getKey(item):
    return item["actNumberofpeople"]

def get_difference(item1, item2):
    if item1 == item2:
        return 0
    try:
        return (abs(item1 - item2) / item2) * 100.0
    except ZeroDivisionError:
        return 0

def whichgroups(res):
    agroups = []
    for i in range(len(res)):
        if res[i] > 0:
            agroups.append(i)
    return agroups

class DataSet:

    _agegroups = [[0, 14],
                  [15, 18],
                  [19, 30],
                  [31, 62],
                  [63, 90]]
    _agecode = ["F", "M"]

    def __init__(self):
        self._residents = None
        self._people = []
        self._agedist = []
        self._counter = 0
        self._oldhomes = None
        #For statistical check
        self._families = []
        self._subrespoi = {}

    def load_magicnumber(self, filename):
        with open(filename, 'r') as f:
            magics = json.load(f)
            self._magic1 = magics["magic1"]
            self._magic2 = magics["magic2"]
            self._magic3 = magics["magic3"]
            self._magic4 = magics["magic4"]
            self._magic5 = magics["magic5"]
            self._magic6 = magics["magic6"]
            self._magicA = magics["magic_age"]
    
    def load_illnessnumber(self, filename):
        with open(filename, 'r') as f:
            magics = json.load(f)
            self._age_separation = magics["age_separation"]
            self._age_percentage = magics["age_percentage"]
            self._illness_number = magics["illness_number"]
            # self._illness = ["a70", "CV", "CK", "COPD", "DM"]
            self._illness = ["a70", "2", "3", "4", "1"]

    def load_residentdata(self, filename):
        '''
        Load a formatted JSON file with the location of residental houses (100x100 cells)

        :param filename: Name of the file
        '''
        with open(filename, 'r') as f:
            _residents = json.load(f)
            self._residents = _residents["places"]
        self._residents = [v for v in sorted(self._residents, key=lambda item: item["capacity"])]

    def calculate_residentstat(self):
        '''
        Summarizes the residential data
        '''
        agedist = [0, 0, 0, 0, 0]
        counter = 0
        filtered = []
        for res in self._residents:
            if res["stat"] == "ON":
                counter = counter + 1
                agedist = [x + y for x, y in zip(agedist, res["ageDistribution"])]
                res["actNumberofpeople"] = sum(res["ageDistribution"])
                filtered.append(res)
        self._residents = filtered
        self._agedist = agedist
        self._verage = agedist[:]
        self._counter = counter
        for i in range(len(self._magicA)):
            self._magicA[i] = round(self._magicA[i] * sum(agedist))

    def load_oldhomedata(self, filename):
        '''
        Load a formatted JSON file with the location of old homes

        :param filename: Name of the file
        '''
        with open(filename, 'r') as f:
            _residents = json.load(f)
            oldhomes = _residents["places"]
        self._residents = [v for v in sorted(oldhomes, key=lambda item: item["capacity"])] + self._residents

    def statistic_check(self):
        '''
        Check if the algorithm conforms to the first 3 magic numbers
        '''
        _magic1_c = [0, 0, 0, 0]
        _magic2_c = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        _magic3_c = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        #_magic4_c = [[0, 0, 0, 0],[0, 0, 0, 0]]
        #_magic5_c = [0, 0]
        #_magic6_c = [[0, 0],[0, 0],[0, 0],[0, 0]]
        _magicA = []
        for fam in self._families:
            # 0: singlepers,
            if (sum(fam)-fam[6])<2 and (sum(fam)-fam[6])>0:
                _magic1_c[0] = _magic1_c[0]+1
                # numbers ELDERLY
                if fam[4]>0:
                    _magic2_c[0][1] = _magic2_c[0][1]+1
                else:
                    _magic2_c[0][0] = _magic2_c[0][0]+1
                # numbers CHILDREN
                _magic3_c[0][0] = _magic3_c[0][0]+1
            else:
                # 3: other / since only elderly are here
                if fam[0]<1 and fam[1]<1 and fam[2]<1 and fam[3]<1 and fam[4]<1:
                    _magic1_c[3] = _magic1_c[3]+1
                    # numbers ELDERLY
                    if fam[4]>3:
                        _magic2_c[3][3] = _magic2_c[3][3]+1
                    else:
                        _magic2_c[3][fam[4]] = _magic2_c[3][fam[4]]+1
                    # numbers CHILDREN
                    _magic3_c[3][0] = _magic3_c[3][0]+1
                else:
                    # 2: famtwoparent,
                    #if (fam[1]>0 and fam[3]>1) or ((fam[2]>0 or fam[3]>0) and (fam[3]>1 or fam[4]>1 or fam[3]+fam[4]>1)) or (fam[0]>0 and (fam[2]>1 or fam[3]>1 or fam[2]+fam[3]>1)):
                    if ((sum(fam)-2*fam[5])-fam[6] > 1 and (fam[0]<1 and fam[1]<1)) or (sum(fam)-2*(fam[5]+fam[6]) > 1):
                        _magic1_c[2] = _magic1_c[2]+1
                        # numbers ELDERLY
                        if fam[4]>3:
                            _magic2_c[2][3] = _magic2_c[2][3]+1
                        else:
                            _magic2_c[2][fam[4]] = _magic2_c[2][fam[4]]+1
                        # numbers CHILDREN
                        if fam[5]>3:
                            _magic3_c[2][3] = _magic3_c[2][3]+1
                        else:
                            _magic3_c[2][fam[5]] = _magic3_c[2][fam[5]]+1
                    # 1: famoneparent,
                    else:
                        _magic1_c[1] = _magic1_c[1]+1
                        # numbers ELDERLY
                        if fam[4]>3:
                            _magic2_c[1][3] = _magic2_c[1][3]+1
                        else:
                            _magic2_c[1][fam[4]] = _magic2_c[1][fam[4]]+1
                        # numbers CHILDREN
                        if fam[5]>3:
                            _magic3_c[1][3] = _magic3_c[1][3]+1
                        else:
                            _magic3_c[1][fam[5]] = _magic3_c[1][fam[5]]+1
                

        _magic1_c[:] = [x / len(self._families) for x in _magic1_c]
        _magic2_c[:] = [[float(j) / sum(i) if sum(i) else 0 for j in i] for i in _magic2_c]
        _magic3_c[:] = [[float(j) / sum(i) if sum(i) else 0 for j in i] for i in _magic3_c]
        return _magic1_c, _magic2_c, _magic3_c

    def generate_family(self):
        '''
        Generates a family age distribution based on statistical magic numbers

        :return: age ditribution, family type, number of children, number of elderly perople
        '''
        famtype = between(random.uniform(0.0, 1.0), self._magic1)
        # 0: singlep, 1: famoneparent, 2: famtwoparents, 3: other
        elderlynum = between(random.uniform(0.0, 1.0), self._magic2[famtype])
        childnum = between(random.uniform(0.0, 1.0), self._magic3[famtype])
        extrachild = 0

        # ensure
        if famtype == 0:
            childnum = 0
        if childnum > 2:
            extrachild = between(random.uniform(0.0, 1.0), [0.93, 0.05, 0.02])
            # extrachild = between(random.uniform(0.0, 1.0), [0.90, 0.06, 0.02, 0.02])

        hhdist = [0, 0, 0, 0, elderlynum]
        for _ in range(0, childnum + extrachild):
            index = between(random.uniform(0.0, 1.0), self._magic4[famtype - 1]) # 0 1 2 3
            if elderlynum == 0 and index > 2:
                index = index - 1
            hhdist[index] = hhdist[index] + 1
        if famtype == 0:
            if elderlynum == 0:
                index = between(random.uniform(0.0, 1.0), self._magic5)
                hhdist[2 + index] = 1
        elif famtype < 3:
            for _ in range(famtype):
                if hhdist[4] > 0 and (hhdist[0] < 1 and hhdist[1] < 1):
                    if hhdist[4] < famtype or hhdist[4]+hhdist[3] < famtype:
                        #index = between(random.uniform(0.0, 1.0), self._magic6[childnum]) # 0 1
                        #hhdist[3 + index] = hhdist[3 + index] + 1
                        hhdist[3] = hhdist[3] + 1
                else:
                    index = between(random.uniform(0.0, 1.0), self._magic6[childnum]) # 0 1
                    hhdist[2 + index] = hhdist[2 + index] + 1
        return hhdist, famtype, childnum+extrachild, elderlynum

    def match_distribution(self, dista, distb):
        '''
        Compares two age distibution

        :param dista: Distribution A
        :param distb: Distribution B
        :return: True iff A==B
        '''
        return dista == distb


    def check_distribution(self, family, cell, ratio=False):
        '''
        Determines whether a family distribution fits into a cell distribution

        :param family: Age distribution of the family
        :param cell: Age distribution of the cell
        :return: True iff for all i in family[i] <= cell[i]
        '''
        if ratio:
            for i in range(len(family)):
                if family[i] > cell[i]:
                    return False
            fr = [x1/x2 if x2>0 else 0 for (x1, x2) in zip(family, family[1:])]
            cr = [x1/x2 if x2>0 else 0 for (x1, x2) in zip(cell, cell[1:])]
            for i in range(len(fr)):
                if get_difference(cr[i], fr[i]) > 10 :
                    return False
            return True
        else:
            for i in range(len(family)):
                if family[i] > cell[i]:
                    return False
            return True
    
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
        #if age > 70:
            #mégsem kell
            #illness = self._illness[0]
            #self._illness_number[0] = self._illness_number[0] - 1
        #else:
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
            illness = "0"
        return illness

    def new_person(self, locs, sex, age, ft):
        '''
        Construct a person

        :param locs: Residential location
        :param sex: Gender
        :param age: Age
        :return: The new person
        '''
        person = {}
        person['age'] = age
        person['sex'] = self._agecode[sex]
        person['preCond'] = self.gen_illness(age)
        person['SIRD'] = "S"
        person['typeID'] = self.occupation_switch(age)
        person['locations'] = []
        person['locations'].append(dict(locs))
        person['famtype'] = ft
        person['famid'] = len(self._families)
        return person

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

    def create_family(self, hdist, location, famtype, ch_n, el_n):
        '''
        Generates a group of people that humans call family
        The generated people are added to the list of residents

        :param hdist: Age distribution for the group
        :param location: Residence
        :param famtype: Type of the group
        :param ch_n: Number of children
        :param el_n: Number of elderly people
        '''

        # put the fam id here to create residential sub-locations
        famcode = "f" + str(len(self._families)) + "_"
        if self._residents[location]["id"] not in self._subrespoi:
            self._subrespoi[self._residents[location]["id"]] = []
        self._subrespoi[self._residents[location]["id"]].append(famcode)
        # make a local copy
        hdist = hdist[:]
        famage = []
        rloc = {"typeID": self._residents[location]["type"],
                "locID": famcode + self._residents[location]["id"],
                "coordinates": self._residents[location]["coordinates"],
                "coordinates_alt": self._residents[location]["coordinates_alt"]
                }

        # children
        m_child_age = -1
        cur_age_group = 0
        for children in range(1, ch_n+1):
            while hdist[cur_age_group] == 0:
                cur_age_group = cur_age_group + 1
            sex = round(random.uniform(0, 1))
            age = self.create_age(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1], cur_age_group)
            self._people.append(self.new_person(rloc, sex, age, famtype))
            m_child_age = max(m_child_age, age)
            famage.append(age)
            hdist[cur_age_group] = hdist[cur_age_group] - 1

        # if we need parents
        if 0 < famtype < 3:
            a_age = []
            a_sex = []
            mini_par_age = m_child_age + 16
            cur_age_group = 3
            for parents in range(1, famtype + 1):
                # at family generation we let elderly be parents, so here we should let them be as well
                while hdist[cur_age_group] == 0 and cur_age_group > 1:
                    cur_age_group = cur_age_group - 1
                    # this bit is a little bit risky but it should work
                    if cur_age_group == 1 and hdist[4] != 0:
                        cur_age_group = 4
                # if there are two then let's have different gender
                if parents == 2:
                    a_sex.append(1-a_sex[0])
                    m_mi = max(-10, self._agegroups[cur_age_group][0] - a_age[0])
                    m_ma = min( 10, self._agegroups[cur_age_group][1] - a_age[0])
                    if (m_mi + a_age[0]) >= (m_ma + a_age[0]):
                        a_age.append(self.create_age(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1], cur_age_group))
                    else:
                        a_age.append(self.create_age(m_mi + a_age[0], m_ma + a_age[0], cur_age_group))
                else:
                    a_sex.append(round(random.uniform(0, 1)))
                    #m_mi = max(self._agegroups[cur_age_group][0], mini_par_age)
                    # ITT NAGY BAJ VAN! - meg van oldva
                    m_mi = self._agegroups[cur_age_group][0]
                    a_age.append(self.create_age(m_mi, self._agegroups[cur_age_group][1], cur_age_group))

                self._people.append(self.new_person(rloc, a_sex[-1], a_age[-1], famtype))
                if cur_age_group == 4:
                    el_n = el_n - 1
                famage.append(a_age[-1])
                hdist[cur_age_group] = hdist[cur_age_group] - 1

        # elderly
        a_age = []
        a_sex = []
        cur_age_group = 4
        for elderlies in range(1, el_n+1):
            # if there are two then let's have different gender
            if elderlies == 2:
                a_sex.append(1-a_sex[0])
                m_mi = max(-10, self._agegroups[cur_age_group][0] - a_age[0])
                m_ma = min( 10, self._agegroups[cur_age_group][1] - a_age[0])
                if (m_mi + a_age[0]) >=(m_ma + a_age[0]):
                    a_age.append(self.create_age(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1], cur_age_group))
                else:
                    a_age.append(self.create_age(m_mi+a_age[0], m_ma+a_age[0], cur_age_group))
            else:
                a_sex.append(round(random.uniform(0, 1)))
                a_age.append(self.create_age(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1], cur_age_group))

            self._people.append(self.new_person(rloc, a_sex[-1], a_age[-1], famtype))
            famage.append(a_age[-1])
            hdist[cur_age_group] = hdist[cur_age_group] - 1


        # the rest, if any
        for cur_age_group in range(len(hdist)):
            for i in range(0,hdist[cur_age_group]):
                sex = round(random.uniform(0, 1))
                age = self.create_age(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1], cur_age_group)
                self._people.append(self.new_person(rloc, sex, age, famtype))
                famage.append(age)

        return famage

    def remove_from_agestat(self, a):
        m = min(int(a / 5), len(self._magicA) - 1)
        g = 0
        for i in range(0, len(self._agegroups)):
            if self._agegroups[i][0] <= a <= self._agegroups[i][1]:
                g = i
                break
        self._verage[g] = self._verage[g] - 1
        self._magicA[m] = self._magicA[m] - 1

    def find_exact_cell(self, hdist, famtype, ch_n, el_n):
        '''
        Try to find a cell that has the same age distribution pattern as the generated family has
        In case of success, the members of family will be instantiated and added to the list of residents

        :param hdist: Age distribution of family
        :param famtype: Type of family
        :param ch_n: Number of children
        :param el_n: Number of elderly people
        :return: False iff there is no such cell
        '''

        location = -1
        for i in range(len(self._residents)):
            if self.match_distribution(hdist, self._residents[i]["ageDistribution"]):
                location = i
                break
        else:
            return False

        f = self.create_family(hdist, location, famtype, ch_n, el_n)
        for i in f:
            self.remove_from_agestat(i)

        for i in range(len(self._agedist)):
            self._agedist[i] = self._agedist[i] - hdist[i]
        #families for statistic check
        self._families.append(hdist+[ch_n, el_n])
        del self._residents[location]

        return True

    def find_suitable_cell(self, hdist, famtype, ch_n, el_n):
        '''
        Try to find a cell where the generated family fits in
        In case of success, the members of family will be instantiated and added to the list of residents

        :param hdist: Age distribution of family
        :param famtype: Type of family
        :param ch_n: Number of children
        :param el_n: Number of elderly people
        :return: False iff there is no such cell
        '''

        location = -1
        for i in range(len(self._residents)-1, 0, -1):
            if self.check_distribution(hdist, self._residents[i]["ageDistribution"]):
                location = i
                break
        else:
            return False

        f = self.create_family(hdist, location, famtype, ch_n, el_n)
        for i in f:
            self.remove_from_agestat(i)

        for i in range(len(self._agedist)):
            self._residents[location]["ageDistribution"][i] = \
                self._residents[location]["ageDistribution"][i] - hdist[i]
            self._agedist[i] = self._agedist[i] - hdist[i]
        self._residents[location]["actNumberofpeople"] = \
            self._residents[location]["actNumberofpeople"] - sum(hdist)
        if self._residents[location]["actNumberofpeople"] < 1:
            del self._residents[location]
        #families for statistic check
        self._families.append(hdist+[ch_n, el_n])
        return True

    def regroup(self):
        self._residents = sorted(self._residents, key=getKey, reverse=True)
        for i in range(len(self._residents)-1, 0, -1):
            if self._residents[i]["capacity"] > 9:
                currgroups = []
                currgroups = currgroups+whichgroups(self._residents[i]["ageDistribution"])
                for j in range(i-1, 0, -1):
                    if get_difference(self._residents[i]["capacity"], self._residents[j]["capacity"]) < 16:
                        if not (any(map(lambda each: each in currgroups, whichgroups(self._residents[j]["ageDistribution"])))):# or len(currgroups) > 2:
                            if self._residents[i]["actNumberofpeople"] + self._residents[j]["actNumberofpeople"] <= self._residents[i]["capacity"]:
                                for o in range(len(self._residents[i]["ageDistribution"])):
                                    self._residents[i]["ageDistribution"][o] = \
                                        self._residents[i]["ageDistribution"][o] + \
                                            self._residents[j]["ageDistribution"][o]
                                self._residents[i]["actNumberofpeople"] = self._residents[i]["actNumberofpeople"] + self._residents[j]["actNumberofpeople"]
                                #if not (any(map(lambda each: each in currgroups, whichgroups(self._residents[j]["ageDistribution"])))):
                                currgroups = currgroups+whichgroups(self._residents[j]["ageDistribution"])
                                self._residents[j]["capacity"] = 0
                            #elif self._residents[i]["capacity"] - self._residents[i]["actNumberofpeople"] < 3:
                            #    break
        self._residents = [v for v in sorted(self._residents, key=lambda item: item["capacity"])]
        self._residents = [x for x in self._residents if x["capacity"] > 0]
    
    def add_commuters(self, comcsv, comscsv, illness):
        self._people = self._people + generate_commuters.generate_agents(comcsv, comscsv, self._magicA, illness)

    def add_tourists(self, illness):
        self._people = self._people + generate_tourists.generate_agents(self._magicA, illness)

    def savedata(self, f, g):
        '''
        Creates a JSON file with the agents
        :param f: Filename
        '''
        with open(f, 'w') as f:
            json.dump(self._people, f, indent="\t")
        with open(g, 'w') as f:
            json.dump(self._subrespoi, f, indent="\t")


def generate_agents(respoi, magic, illness, tempout, tempstat, ohpoi, comcsv=None, comscsv=None, tempfamlocation=None):

    adatok = DataSet()
    adatok.load_magicnumber(magic)
    adatok.load_illnessnumber(illness)
    adatok.load_residentdata(respoi)
    adatok.load_oldhomedata(ohpoi)
    adatok.calculate_residentstat()
    print(adatok._agedist, sum(adatok._agedist))

    last_fam = []
    pop = sum(adatok._agedist)


    iter = 0
    redo_counter = 0
    redo_thrashold = 5000
    while True:
        iter = iter + 1
        if iter % 250 == 0:
            txt = "Generating agents - " + '{:6.2f}'.format(100.0*(pop-sum(adatok._agedist))/pop) + "%"
            # ll = [adatok._magicA[0] + adatok._magicA[1] + adatok._magicA[2],
            #       adatok._magicA[3],
            #       adatok._magicA[4] + adatok._magicA[5],
            #       adatok._magicA[6] + adatok._magicA[7] + adatok._magicA[8] + adatok._magicA[9] + adatok._magicA[10] + adatok._magicA[11],
            #       adatok._magicA[12] + adatok._magicA[13] + adatok._magicA[14] + adatok._magicA[15] + adatok._magicA[16] +
            #       adatok._magicA[17]
            #       ]

            # txt = str(adatok._agedist) + "/" + str(adatok._verage) + " Der: " + str(ll)
            # txt = str(adatok._magicA)
            sys.stdout.write('\r' + txt)


        (hdist, ftype, ch_n, el_n) = adatok.generate_family()
        if not adatok.find_exact_cell(hdist, ftype, ch_n, el_n):
            if not adatok.find_suitable_cell(hdist, ftype, ch_n, el_n):
                if redo_counter < redo_thrashold:
                    redo_counter = redo_counter + 1
                else:
                    adatok.regroup()
                    if not adatok.find_exact_cell(hdist, ftype, ch_n, el_n):
                        if not adatok.find_suitable_cell(hdist, ftype, ch_n, el_n):
                            last_fam = hdist
                            break

    txt = "Generating agents - " + '{:6.2f}'.format(100.0 * (pop-sum(adatok._agedist)) / pop) + "%"
    sys.stdout.write('\r' + txt + " - done. Calculating statistics")

    m1, m2, m3 = adatok.statistic_check()
    with open(tempstat, "w") as txt_file:
        txt_file.write(str(m1) + "\n")
        txt_file.write('\n')
        for line in m2:
            txt_file.write('[%s]' % ', '.join(map(str, line)) + "\n")
        txt_file.write('\n')
        for line in m3:
            txt_file.write('[%s]' % ', '.join(map(str, line)) + "\n")
        txt_file.write('\n'+str(last_fam)+'\n')
        for res in adatok._residents:
            txt_file.write(str(res["ageDistribution"])+" id: "+str(res["id"])+" capacity: "+str(res["capacity"])+"\n")

    sys.stdout.write(" - done. Saving")
    #adatok._people = useful_library.order_by_place(adatok._people, 0)
    if comcsv != None and comscsv != None:
        adatok.add_commuters(comcsv, comscsv, illness)
    adatok.add_tourists(illness)

    adatok.savedata(tempout, tempfamlocation)

    print(" - done.")
    print(adatok._magicA)

