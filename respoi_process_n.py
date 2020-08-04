import json
import sys

import shapefile as sfr
import urllib.request as ur

def process_input_data(prefix, shapefile, respoifile):

    sf = sfr.Reader(shapefile, encoding="latin-1")

    data = list()
    iter = 0
    for s in sf.iterShapeRecords():
        iter = iter + 1
        if iter % 10:
            txt = "Processing Shapefile records " + '{:6.2f}'.format(100.0*iter/sf.numRecords) + "%"
            sys.stdout.write('\r' + txt)

        sha = s.record
        sha[10] = sha[10].replace('kertváros', '0')
        sha[10] = sha[10].replace('zöldövezeti társasház', '1')
        sha[10] = sha[10].replace('lakótelep', '2')
        sha[10] = sha[10].replace('belvárosi zárt beépítés', '3')
        eovx = sha[2]
        eovy = sha[1]
        ret = ur.urlopen('http://www.agt.bme.hu/on_line/etrs2eov/etrs2eov.php?e='+str(eovx)+'&n='+str(eovy)).read()
        ret = ret.decode('ascii').split(' ')
        wgse = float(ret[1])
        wgsn = float(ret[2])

        coordinates = [wgse, wgsn]
        coorditanes_eov = [eovx, eovy]
        places = {'id': sha[0],
                  'type': 2,
                  'subtype': int(sha[10]),
                  'coordinates': coordinates,
                  'coordinates_alt': coorditanes_eov,
                  'area': 10000,
                  'stat': 'ON',
                  'capacity': sha[12],
                  'ageInter': [0, 100],
                  #                   '-14'  '15-18' '19-30' '31-62'  '63-'
                  'ageDistribution': [sha[13], sha[14], sha[15], sha[16], sha[17]]
                  }
        data.append(places)

    adat = {"area": prefix, "places": data}
    with open(respoifile, 'w') as f:
        json.dump(adat, f, indent="\t")

    print(" - file saved")

