# encoding = utf8
import os
from unidecode import unidecode
from random import randint
import time
import matplotlib.pyplot as plt


def read_files(directory):
        # prebere vse fajle in jih vrne v skupni tabeli
        prebraniTxt = []
        for i in os.listdir(directory):
            text = open("vsi_jeziki/" + i, "rt", encoding="utf-8").read()
            prebraniTxt.append([i[0:3], unidecode(text)])

        return prebraniTxt;


class Kmedoids:
    
    def preurediBesedilo(self, besedilo):
        besedilo = besedilo.lower()  # --> da vse v male crke
        prenovljenoBesedilo = ""
        for i in besedilo:
            if i == '.' or i == ',' or i == '\n':
                prenovljenoBesedilo += ' '
            else:
                prenovljenoBesedilo += i
                 
        return prenovljenoBesedilo
    
    def analizirajTrojke(self, besedilo_neur):        
                
        besedilo = self.preurediBesedilo(besedilo_neur)
        tabelaTrojke = {}  # --> tabela sestavljena v obliki slovartja ["hec" : 3] kjer je hec trojka in 3 stevilo ponovitev
        for i in range(len(besedilo) - 3):  # !! err mogoce -2
            trenTrojka = besedilo[i:i + 3]
            if ' ' not in trenTrojka:
                if trenTrojka not in tabelaTrojke: 
                    tabelaTrojke[trenTrojka] = 1
                else:
                    tabelaTrojke[trenTrojka] += 1
                
        return tabelaTrojke     

    def __init__(self, data):
        self.data = data  # --> tabela [['eng', "Universal Declaration..:"], ['czc', "..."]]
        self.stJezikov = len(self.data)
        
        # ISKANJE VSEH TROJK --> tabela kjer imam za vsak jezik svojo tabelo, kjer shranim vse trojke trenutnega jezika in stevilo njihovih ponovitev
        self.trojke = []
        index = 0
        for i in self.data:
            trojkeTabela = self.analizirajTrojke(i[1])
            self.trojke.append([index, i[0], trojkeTabela])  # --> dodamo tabele trojk za vse drzave
            index += 1
    
     #-------------------------------------------------------------------------------------------------------------------#
    
    def kosinusna_razdalja(self, jezik1, jezik2):  # --> !!! Error dela kr neki kar nima smisla , ne deluje pravilno se mi zdi
        str1 = jezik1[1] + jezik2[1]
        str2 = jezik2[1] + jezik1[1]
        
        if str1 in self.razdalje:
            return self.razdalje[str1]
        elif str2 in self.razdalje:
            return self.razdalje[str2]
        else:
        
        # skalarni produkt / zmnozek absolutnih razdalj
        
            jezik1_trojka = jezik1[2]
            jezik2_trojka = jezik2[2]
            produkt = 0
            for i in jezik1_trojka:
                    if i in jezik2_trojka:
                        produkt += jezik1_trojka[i] * jezik2_trojka[i]
                        
            abs1 = 0
            abs2 = 0
            for i in jezik1_trojka:
                abs1 += (jezik1_trojka[i] ** 2)
            abs1 = abs1 ** (1 / 2)        
            for j in jezik2_trojka:
                abs2 += jezik2_trojka[j] ** 2 
            abs2 = abs2 ** (1 / 2)
            if produkt == 0:
                print("error 'produkt == 0' line 71")
            
            kosinPodob = produkt / (abs1 * abs2)
            kosinRazd = 1 - kosinPodob
            
            self.razdalje[str1] = kosinRazd
            return kosinRazd
    
    def najbljizjiVod(self, indexiVod, indexTrenJezika):  # --> Not Tested
        najbljizjiVod = ["", 10000000]  # --> ["ime", razdalja]
        for i in indexiVod:
            # print("tren index: " + str(indexTrenJezika) + "            index voditelja: " + str(i) + "\n")
            razdaljaTrenVoditelj = self.kosinusna_razdalja(self.trojke[i], self.trojke[indexTrenJezika])
            if razdaljaTrenVoditelj < najbljizjiVod[1]:
                najbljizjiVod[0] = self.trojke[i][1]
                najbljizjiVod[1] = razdaljaTrenVoditelj
        
        return najbljizjiVod
    
    def indexJezika(self, imeJezika):
        for i in self.trojke:
            if i[1] == imeJezika:
                return i[0]
        
    def noviVoditelj(self, trenutniCluster):  # --> vrne index in ime voditelja
        trenVoditelj = ""
        minRazdalja = 10000.0
        
        # zracunamo vsoto razdalj od posameznih jezika do vseh ostalih jezikov in tisi, katerega vsota je najmanjsa, je novi voditelj
        for i in trenutniCluster:   
            trenutnaRazdalja = 0.0
            for j in trenutniCluster:
                if i != j:
                    jezik1 = self.trojke[self.indexJezika(i)]
                    jezik2 = self.trojke[self.indexJezika(j)]
                    trenutnaRazdalja += self.kosinusna_razdalja(jezik1, jezik2)
            
            if trenutnaRazdalja < minRazdalja:  
                # if trenutnaRazdalja == 0.0:
                #    print ("error trenRazdalja == 0     line 104 \n")         --> sam pomen da je sam ena drzava v clustru
                trenVoditelj = self.trojke[self.indexJezika(i)][1]
                minRazdalja = trenutnaRazdalja
                # print("trenVoditelj: " + trenVoditelj + "           minRazdalja: " + str(minRazdalja) + "\n")
        
        return trenVoditelj
    
    def enakostTabel(self, tab1, tab2):
        for i in tab1:
            if i not in tab2:
                return False
        return True
    
    def kmemoids(self, stVoditeljev):
        
        # nakljucno zberem "stVoditeljev" stevil od 0 do 21, da dolocim zacetne voditelje
        voditelji = []
        indeksiVoditeljev = []
        while len(voditelji) != stVoditeljev:
            nakljucnoSt = randint(0, self.stJezikov - 1)  # --> self.stJezikov ze pri branju presteje kolk jezikov smo importal
            if nakljucnoSt not in indeksiVoditeljev:
                voditelji.append(self.trojke[nakljucnoSt][1])
                indeksiVoditeljev.append(nakljucnoSt)
        
        # tuki zazenemo sam algoritem
        zakljuciAlgoritem = False
        clustriVoditeljev = {}
        while zakljuciAlgoritem == False:
            # --> nastavimo zacetne clustre voditeljev
            clustriVoditeljev = {}
            for i in voditelji:
                clustriVoditeljev[i] = [i]  # --> dictionary
            
            # prvo oblikujem clustre
            for i in self.trojke:
                if i[1] not in voditelji:
                    iVoditelj = self.najbljizjiVod(indeksiVoditeljev, i[0])
                    clustriVoditeljev[ iVoditelj[0] ].append(i[1])  # --> dodamo v dictionary od clustrov      [index, ime] 
            
            # nato dolocim nove voditelje znotraj clustrov
            noviVoditelji = []
            noviIndVod = []
            for i in clustriVoditeljev:  # --> zravn passi se trenutneVoditelje v funkcijo
                noviVod = self.noviVoditelj(clustriVoditeljev[i])  # --> posljemo cel cluster noter
                noviVoditelji.append(noviVod)
                noviIndVod.append(self.indexJezika(noviVod))
                
            # -->tuki pogledam ce so stari in novi voditelji enaki ker to pomeni da smo zakljucili algoritem
            zakljuciAlgoritem = self.enakostTabel(voditelji, noviVoditelji)
                
            # na koncu posodobimo clustre in voditelje
            voditelji = noviVoditelji
            indeksiVoditeljev = noviIndVod
        
        return clustriVoditeljev
    
    #-------------------------------------------------------------------------------------------------------------------#
    def povprZnotrajSkup(self, jezik, skupina):        
        # if a != jezik, dolzina += jezik
        skupnaDolzina = 0.0
        for i in skupina:
            if i != jezik:
                jezik1 = self.trojke[ self.indexJezika(jezik) ]
                jezik2 = self.trojke[ self.indexJezika(i) ]
                skupnaDolzina += self.kosinusna_razdalja(jezik1, jezik2)
        
        if len(skupina) == 1:
            return 0.0  # --> sam ena drzava v clustru
        else:
            return skupnaDolzina / (len(skupina) - 1)  # delimo z stevilom elemenotov -1, ker samega jezika "jezik" ne stejemo zraven
    
    def povpZunajSkup(self, jezik, clustri):
        minPovpRazdalja = 100000.0
        
        for i in clustri:
            if jezik not in clustri[i]:
                zdruzenCLuster = clustri[i] + [jezik]
                razdalja = self.povprZnotrajSkup(jezik, zdruzenCLuster)
                if razdalja < minPovpRazdalja:
                    minPovpRazdalja = razdalja
        
        return minPovpRazdalja

    def izracSilhueto(self, clustri):
        tabelaPosameznihSilhuet = []
        stSilhuet = 0
        for i in clustri:
            for jezik in clustri[i]:  # --> tok da gremo cez vse jezike in da hkrati vemo v katerem clustu so
                a = self.povprZnotrajSkup(jezik, clustri[i])
                b = self.povpZunajSkup(jezik, clustri)  # if j not in posamezenCluster 
                
                deliZ = max([a, b])
                posameznaSil = (b - a) / deliZ
                tabelaPosameznihSilhuet.append(float(posameznaSil))
                stSilhuet += 1
        
        # sestejem vse silhuete in pol delim s stevilom silhuet
        vsotaSilhuet = 0.0
        for i in tabelaPosameznihSilhuet:
            vsotaSilhuet += i 
        
        return vsotaSilhuet / stSilhuet
    
    #-------------------------------------------------------------------------------------------------------------------# 
    def topJeziki(self, text):
        top3Jeziki = [["", 0.0], ["", 0.0], ["", 0.0]]  # --> [[slo, 0.6] [srb, 0.5], [bih, 0.48]
        # prvo dam tekst v trojke
        text_unidecode = unidecode(text)
        text_trojke = self.analizirajTrojke(text_unidecode)
        for i in self.trojke:
            podobnost = 1 - self.kosinusna_razdalja([-1, "neznan", text_trojke], i)
            if podobnost > top3Jeziki[0][1]:
                top3Jeziki[0][1] = podobnost
                top3Jeziki[0][0] = i[1]
            elif podobnost > top3Jeziki[1][1]:
                top3Jeziki[1][1] = podobnost
                top3Jeziki[1][0] = i[1]
            elif podobnost > top3Jeziki[2][1]:
                top3Jeziki[2][1] = podobnost
                top3Jeziki[2][0] = i[1]
        
        return top3Jeziki
     
    #-------------------------------------------------------------------------------------------------------------------# 
        
    def run(self):
        tabelaSilhuet = []
        # zacetenCas = time.time()
        self.razdalje = {}  # --> belezim razdalje med drzavami da jih ne racunam skos ene in iste
        for i in range(100):
            koncniClustri = self.kmemoids(5)
            trenutnaSilhueta = self.izracSilhueto(koncniClustri)
            tabelaSilhuet.append(trenutnaSilhueta)
            # print(str(trenutnaSilhueta) + "\n")

        tabelaSilhuet.sort()
        tabelaSilZaok = []      
        for i in tabelaSilhuet:
            tabelaSilZaok.append(round(i, 2))
            # print(str(i) + "\n")
            
        # zdj dobimo vn frekvenco posameznih silhuet 
        frekvenceSilhuet = {}  # --> frekvence dejansko ne rabmo ampak je koristno za debugging
        for i in tabelaSilZaok:
            if i in frekvenceSilhuet:
                frekvenceSilhuet[i] += 1
            else:
                frekvenceSilhuet[i] = 1
        
        # zdj zrisemo graf
        xOs = []
        for i in frekvenceSilhuet:
            xOs.append(i)
        
        plt.hist(tabelaSilZaok, xOs, histtype="bar")
        plt.xlabel("Vrednosti silhuet")
        plt.ylabel("Stevilo ponovitev")
        plt.title("Histogram silhuet")   
        plt.legend()

        # koncniCas = time.time()
        # print("Porabu sm " + str(koncniCas - zacetenCas) + " sekund. \n")
             
        plt.show()
        
        print("Sedaj bomo gelde na vneseni tekst poskusili najti vas jezik:\n")
        text = open("neznani.txt", "rt", encoding="cp1252").read()  # --> encoding zbriše žje pa šje pa neki sfuka čje
        top3jeziki = self.topJeziki(text)
        print("Najbolj verjetni jezik je " + top3jeziki[0][0] + " z verjetnostjo " + str(round(top3jeziki[0][1] * 100, 2)) + "%\n")
        print("Drugi najbolj verjetni jezik je " + top3jeziki[1][0] + " z verjetnostjo " + str(round(top3jeziki[1][1] * 100, 2)) + "%\n")
        print("Tretji najbolj verjetni jezik je " + top3jeziki[2][0] + " z verjetnostjo " + str(round(top3jeziki[2][1] * 100, 2)) + "%\n")
        
        
if __name__ == "__main__":
    hc = Kmedoids(read_files("vsi_jeziki"))
    hc.run()

# TODO
"""
    -trojke nastimi tko da bojo v slovarju
    -tabela trojk da bo v slovarju da se ne rabs jebat z indeksi



"""
