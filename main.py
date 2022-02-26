# htmls = ["01_GEN-changes.html", "02_EXO-changes.html", "03_LEV-changes.html", "04_NUM-changes.html", "05_DEU-changes.html", "06_JOS-changes.html", "07_JDG-changes.html", "08_RUT-changes.html", "09_1SA-changes.html", "10_2SA-changes.html", "11_1KI-changes.html", "12_2KI-changes.html", "13_1CH-changes.html", "14_2CH-changes.html", "15_EZR-changes.html", "16_NEH-changes.html", "17_EST-changes.html", "18_JOB-changes.html", "19_PSA-changes.html", "20_PRO-changes.html", "21_ECC-changes.html", "22_SNG-changes.html", "23_ISA-changes.html", "24_JER-changes.html", "25_LAM-changes.html", "26_EZK-changes.html", "27_DAN-changes.html", "28_HOS-changes.html", "29_JOL-changes.html", "30_AMO-changes.html", "31_OBA-changes.html", "32_JON-changes.html", "33_MIC-changes.html", "34_NAM-changes.html", "35_HAB-changes.html", "36_ZEP-changes.html", "37_HAG-changes.html", "38_ZEC-changes.html", "39_MAL-changes.html", "40_MAT-changes.html", "41_MRK-changes.html", "42_LUK-changes.html", "43_JHN-changes.html", "44_ACT-changes.html", "45_ROM-changes.html", "46_1CO-changes.html", "47_2CO-changes.html", "48_GAL-changes.html", "49_EPH-changes.html", "50_PHP-changes.html", "51_COL-changes.html", "52_1TH-changes.html", "53_2TH-changes.html", "54_1TI-changes.html", "55_2TI-changes.html", "56_TIT-changes.html", "57_PHM-changes.html", "58_HEB-changes.html", "59_JAS-changes.html", "60_1PE-changes.html", "61_2PE-changes.html", "62_1JN-changes.html", "63_2JN-changes.html", "64_3JN-changes.html", "65_JUD-changes.html", "66_REV-changes.html"]
# htmls = [htmls[59]]
from bs4 import BeautifulSoup as bs

htmls = ["40_MAT-thNCV.html", "41_MRK-thNCV.html"]
changes = {}

for html in htmls:
    HTMLFile = open(html, "r", encoding="utf-16")
    index = HTMLFile.read()

    index = index.replace('<div class="unchanged">','<div class="unchanged"><span>\c</span>' )

    soupfile = bs(index, 'lxml')
    spans = soupfile.find_all('span')

    adtn =0
    dltn = 0
    bk = html[3:6]
    changes[bk] = {}
    ch = 0
    v  = 0
    tot = len(spans)
    vchanges = []
    actiontype = ""
    
    print("\n\nCurrently processing {}\t".format(bk))

    for tag in spans:
        try:
            if(tag.attrs['class']):
                tag_attribute = str(tag.attrs['class'][0])
        except:
            pass
        tag_data = str(tag.text)
        if(tag_data)=="\c":
            ch += 1
            print(ch, end=" ")
            v = 0
            changes[bk][ch] = {}
        if(tag_data)=="\\v":
            v += 1
            changes[bk][ch][v] = []
        if tag_attribute not in ['changebar', 'marker', 'usfm_v', 'usfm_wj', "-"]:
            if tag_attribute=="diffadd":
                actiontype="+"
                adtn +=1
            else:
                actiontype="-"
                dltn +=1
            tag_data = "&SPACE;" if tag_data == " " else tag_data
            tag_attribute = "+" if tag_attribute == "diffadd" else "-"
            try:
                changes[bk][ch][v].append((tag_data, tag_attribute))
            except:
                pass
#                 try:
#                     changes[bk][ch][v]=((tag_data, tag_attribute))
#                 except:
#                     try:
#                         changes[bk][ch]={v}
#                         changes[bk][ch][v]=((tag_data, tag_attribute))
#                     except:
#                         try:
#                             changes[bk]={ch}
#                             changes[bk][ch]={v}
#                             changes[bk][ch][v]=((tag_data, tag_attribute))
#                         except:
#                             Print("Error Processing Data!\n\t{} {}:{} {}\t{}".format(bk, ch, v, tag_data, tag_attribute))
#                             pass
        changes[bk]["Additions"] = adtn
        changes[bk]["Deletions"] = dltn
        changes[bk]["Total"]     = tot

with open("changes.txt", mode="w", encoding="utf-16") as o:
    for k in changes.keys():
        o.write("\n\n=====Summary of changes in {}=====".format(k))
        adtn = changes[k]["Additions"]
        dltn = changes[k]["Deletions"]
        totl = changes[k]["Total"]

        o.write("\nInsertions: {}\nDeletions: {}\nPerc. of Changes: {}%\n-----".format(adtn, dltn, round((max(adtn, dltn)/totl)*100,2)))
        for c in changes[k].keys():
            if c not in ["Additions", "Deletions", "Total"]:
                o.write("\n\n=====Chapter: {}=====".format(c))
                for v in changes[k][c].keys():
                    o.write("\n\n{} {}:{}\n-----".format(k,c,v))
                    for item in changes[k][c][v]:
                        if item:
                            ac = "Insertion" if item[1] == "+" else "Deletion"
                            o.write("\n\t{}:\t{}".format(ac,item[0]))

#                         print("{}\t{}".format(ac, item[0]))