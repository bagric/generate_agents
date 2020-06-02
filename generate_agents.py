import json
import random
import sys


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

#def getKey(item):
#    return item["actNumberofpeople"]

def get_difference(item1, item2):
    if item1 == item2:
        return 0
    try:
        return (abs(item1 - item2) / item2) * 100.0
    except ZeroDivisionError:
        return 0

def insertion_sort(list, field, number=-1):
    for index in range(len(list)-1, 0, number):
        value = list[index]
        i = index-1
        while i>=0:
            if value[field]<list[i][field]:
                list[i+1]=list[i]
                list[i]=value
                i=i-1
            else:
                break

class DataSet:
    # KSH MAGIC numbers FAMILY
    # 0: singlepers,
    # 1: famoneparent,
    # 2: famtwoparent,
    # 3: other
    _magic1 = [0.433,
               0.139,
               0.434,
               0.028]
    # KSH MAGIC numbers ELDERLY
    #                None   1      2      3+
    _magic2 = [[0.475, 0.525, 0.000, 0.000],
               [0.700, 0.284, 0.015, 0.001],
               [0.640, 0.121, 0.233, 0.006],
               [0.584, 0.285, 0.128, 0.003]]
    # KSH MAGIC numbers CHILDREN
    #           None   1      2      3+
    _magic3 = [[1.000, 0.000, 0.000, 0.000],
               [0.000, 0.668, 0.270, 0.062],
               [0.444, 0.285, 0.206, 0.065],
               [1.000, 0.000, 0.000, 0.000]]
    # Magic: age distribution of children
    _magic4 = [[0.519, 0.481 * 0.28, 0.481 * 0.20, 0.481 * 0.52],
    #           [0.519, 0.481 * 0.28, 0.481 * 0.20, 0.481 * 0.52]]
    #_magic4 = [[0.348, 0.652 * 0.21, 0.652 * 0.44, 0.652 * 0.35],
               [0.534, 0.466 * 0.35, 0.466 * 0.63, 0.466 * 0.02]]
    # Magic: younger single - older single
    _magic5 = [0.20, 0.80]
    # Magic: younger parent - older parent
    _magic6 = [[0.33, 0.67],
               [0.25, 0.75],
               [0.20, 0.80],
               [0.20, 0.80]]
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
        #For statistical check
        self._families = []
        #árvákat talán lerakni egy már meglévő családhoz, ugyanezt idősekre


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
                res["actNumberofpeople"] = sum(agedist)
                filtered.append(res)
        self._residents = filtered
        self._agedist = agedist
        self._counter = counter
    
    def statistic_check(self):
        _magic1_c = [0, 0, 0, 0]
        _magic2_c = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        _magic3_c = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]
        #_magic4_c = [[0, 0, 0, 0],[0, 0, 0, 0]]
        #_magic5_c = [0, 0]
        #_magic6_c = [[0, 0],[0, 0],[0, 0],[0, 0]]
        for fam in self._families:
            # 0: singlepers,
            if (sum(fam)-fam[6])<2:
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
        famtype = between(random.uniform(0.0, 1.0), DataSet._magic1)
        # 0: singlep, 1: famoneparent, 2: famtwoparents, 3: other
        elderlynum = between(random.uniform(0.0, 1.0), DataSet._magic2[famtype])
        childnum = between(random.uniform(0.0, 1.0), DataSet._magic3[famtype])
        extrachild = 0

        # ensure
        if famtype == 0:
            childnum = 0
        #elif famtype < 3:
        #    extrachild = between(random.uniform(0.0, 1.0), [0.93, 0.05, 0.02])
            #extrachild = between(random.uniform(0.0, 1.0), [0.90, 0.06, 0.02, 0.02])

        hhdist = [0, 0, 0, 0, elderlynum]
        for _ in range(0, childnum + extrachild):
            index = between(random.uniform(0.0, 1.0), DataSet._magic4[famtype - 1]) # 0 1 2 3
            if elderlynum == 0 and index > 2:
                index = index - 1
            hhdist[index] = hhdist[index] + 1
        if famtype == 0:
            if elderlynum == 0:
                index = between(random.uniform(0.0, 1.0), DataSet._magic5)
                hhdist[2 + index] = 1
        elif famtype < 3:
            for _ in range(famtype):
                if hhdist[4] > 0 and (hhdist[0] < 1 and hhdist[1] < 1):
                    if hhdist[4] < famtype or hhdist[4]+hhdist[3] < famtype:
                        index = between(random.uniform(0.0, 1.0), DataSet._magic6[childnum]) # 0 1
                        hhdist[3 + index] = hhdist[3 + index] + 1
                else:
                    index = between(random.uniform(0.0, 1.0), DataSet._magic6[childnum]) # 0 1
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

    def new_person(self, locs, sex, age):
        '''
        Construct a person

        :param locs: Residential location
        :param sex: Gender
        :param age: Age
        :return: The new persion
        '''
        person = {}
        person['age'] = age
        person['sex'] = self._agecode[sex]
        person['preCond'] = 0
        person['SIRD'] = "S"
        person['typeID'] = 4
        person['locations'] = []
        person['locations'].append(dict(locs))
        return person

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

        # make a local copy
        hdist = hdist[:]
        rloc = {"typeID": self._residents[location]["type"],
                "locID": self._residents[location]["id"],
                "coordinates": self._residents[location]["coordinates"],
                "coordinates_alt": self._residents[location]["coordinates_alt"]
                }

        # elderly
        a_age = []
        a_sex = []
        cur_age_group = 4
        for elderlies in range(1, el_n+1):
            # if there are two then let's have different gender
            if elderlies == 2:
                a_sex.append(1-a_sex[0])
                m_mi = max(-7, self._agegroups[cur_age_group][0] - a_age[0])
                m = round(random.uniform(m_mi, +7))
                a_age.append(m+a_age[0])
            else:
                a_sex.append(round(random.uniform(0, 1)))
                a_age.append(round(random.uniform(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1])))

            self._people.append(self.new_person(rloc, a_sex[-1], a_age[-1]))
            hdist[cur_age_group] = hdist[cur_age_group] - 1

        # children
        m_child_age = -1
        cur_age_group = 0
        for children in range(1, ch_n+1):
            while hdist[cur_age_group] == 0:
                cur_age_group = cur_age_group + 1
            sex = round(random.uniform(0, 1))
            age = round(random.uniform(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1]))
            self._people.append(self.new_person(rloc, sex, age))
            m_child_age = max(m_child_age, age)
            hdist[cur_age_group] = hdist[cur_age_group] - 1

        # if we need parents
        if 0 < famtype < 3:
            a_age = []
            a_sex = []
            mini_par_age = m_child_age + 16
            cur_age_group = 2
            for parents in range(1, famtype + 1):
                while hdist[cur_age_group] == 0 and cur_age_group + 1 <5:
                    cur_age_group = cur_age_group + 1
                # if there are two then let's have different gender
                if parents == 2:
                    a_sex.append(1-a_sex[0])
                    m_mi = max(-7, self._agegroups[cur_age_group][0] - a_age[0])
                    m = round(random.uniform(m_mi, +7))
                    a_age.append(m+a_age[0])
                else:
                    a_sex.append(round(random.uniform(0, 1)))
                    m_mi = max(self._agegroups[cur_age_group][0], mini_par_age)
                    a_age.append(round(random.uniform(m_mi, self._agegroups[cur_age_group][1])))

                self._people.append(self.new_person(rloc, a_sex[-1], a_age[-1]))
                hdist[cur_age_group] = hdist[cur_age_group] - 1

        # the rest, if any
        for cur_age_group in range(len(hdist)):
            for i in range(hdist[cur_age_group]):
                sex = round(random.uniform(0, 1))
                age = round(random.uniform(self._agegroups[cur_age_group][0], self._agegroups[cur_age_group][1]))
                self._people.append(self.new_person(rloc, sex, age))

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

        self.create_family(hdist, location, famtype, ch_n, el_n)
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
        #self._residents = sorted(self._residents, key=getKey)
        insertion_sort(self._residents, "actNumberofpeople")
        location = -1
        for i in range(len(self._residents)-1, 0, -1):
            if self.check_distribution(hdist, self._residents[i]["ageDistribution"], True):
                location = i
                break
        for i in range(len(self._residents)-1, 0, -1):
            if self.check_distribution(hdist, self._residents[i]["ageDistribution"]):
                location = i
                break
        else:
            return False

        self.create_family(hdist, location, famtype, ch_n, el_n)
        for i in range(len(self._agedist)):
            self._residents[location]["ageDistribution"][i] = \
                self._residents[location]["ageDistribution"][i] - hdist[i]
            self._agedist[i] = self._agedist[i] - hdist[i]
        self._residents[location]["actNumberofpeople"] = \
            self._residents[location]["actNumberofpeople"] - sum(hdist)
        #families for statistic check
        self._families.append(hdist+[ch_n, el_n])
        return True
    
    def savedata(self, f):
        '''
        Creates a JSON file with the agents
        :param f: Filename
        '''
        with open(f, 'w') as f:
            json.dump(self._people, f)


adatok = DataSet()
adatok.load_residentdata("Szeged_adat_new.json")
adatok.calculate_residentstat()

iter = 0
while True:
    iter = iter + 1
    if iter % 250 == 0:
        txt = str(iter) + " iteration: SUM" + str(adatok._agedist) + " = " + str(sum(adatok._agedist))
        sys.stdout.write('\r' + txt)

    (hdist, ftype, ch_n, el_n) = adatok.generate_family()
    if not adatok.find_exact_cell(hdist, ftype, ch_n, el_n):
        if not adatok.find_suitable_cell(hdist, ftype, ch_n, el_n):
            break

txt = str(iter) + " iteration: SUM" + str(adatok._agedist) + " = " + str(sum(adatok._agedist))
sys.stdout.write('\r' + txt)
#for res in adatok._residents:
#    print(str(res["ageDistribution"]) + " with id: " + str(res["id"]))
m1, m2, m3 = adatok.statistic_check()
with open("prob_check.txt", "w") as txt_file:
    txt_file.write(str(m1) + "\n")
    txt_file.write('\n')
    for line in m2:
        txt_file.write('[%s]' % ', '.join(map(str, line)) + "\n")
    txt_file.write('\n')
    for line in m3:
        txt_file.write('[%s]' % ', '.join(map(str, line)) + "\n")
adatok.savedata("Szeged_adat_agentsB.json")