import json
import sys

import shapefile as sfr
import urllib.request as ur

def process_input_data(prefix, shapefile, respoifile):

    sf = sfr.Reader(shapefile)

    data = list()
    iter = 0
    for s in sf.iterShapeRecords():
        iter = iter + 1
        if iter % 10:
            txt = "Processing Shapefile records " + '{:6.2f}'.format(100.0*iter/sf.numRecords) + "%"
            sys.stdout.write('\r' + txt)

        sha = s.record
        sha[-1] = sha[-1].replace('kertv�ros', '0')
        sha[-1] = sha[-1].replace('z�ld�vezeti t�rsash�z', '1')
        sha[-1] = sha[-1].replace('lak�telep', '2')
        sha[-1] = sha[-1].replace('belv�rosi z�rt be�p�t�s', '3')
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
                  'subtype': int(sha[-1]),
                  'coordinates': coordinates,
                  'coordinates_alt': coorditanes_eov,
                  'area': 10000,
                  'stat': 'ON',
                  'capacity': sha[4],
                  'ageInter': [0, 100],
                  #                   '-14'  '15-18' '19-30' '31-62'  '63-'
                  'ageDistribution': [sha[5], sha[6], sha[7], sha[8], sha[9]]
                  }
        data.append(places)

    adat = {"area": prefix, "places": data}
    with open(respoifile, 'w') as f:
        json.dump(adat, f)

    print(" - file saved")
