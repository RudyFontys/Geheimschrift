# Geheimschrift CLI - zonder imports libraries etc (alleen basis Python)

#MijnMotoren = "  YaMaha "

# Invoer consistent maken
def normalize(s):
    return s.strip().lower()

#test = normalize(MijnMotoren)
#print(test)


# Key maken
def build_key(words):
     w = [normalize(x) for x in words]
     if len(w) != 5 or any(x == "" for x in w):
         raise ValueError("Je moet precies 5 niet-lege kernwoorden invullen.")

     # maak een nieuwe sleuteltekst (soort van salt & pepper)
     key = "|".join(w)
     key2 = key + "#" + key[::-1] + "@" + str(len(key) * 7 + 13)
     return key2

# MijnMotoren = ['Triumph', 'BMW', 'Harley', 'Ýamaha', 'Kawasaki']

# test = build_key(MijnMotoren)
# print(test) 
# uitkomst is triumph|bmw|harley|ýamaha|kawasaki#ikasawak|ahamaý|yelrah|wmb|hpmuirt@251

# om van de key getallen te maken heb ik AI de vraag gesteld om een stukje code te genereren die dit doet
# tevens was de vraag om hier een kleine versleuteling in te maken (simpele mix)
# de uitkomst was voor mij best complex, ik heb flink moeten zoeken hoe het werkt...

def key_value(key, i): # De waarde van i komt uit de "encrypt_text(plain, key)" functie
    # haal een getal 0..255 uit de sleutel voor positie i
    ch = key[i % len(key)]
    base = ord(ch)  # 0..(Unicode)
    # maak er een 0..255 van (simpele mix)
    return (base * 31 + i * 17 + (base ^ (i * 13))) % 256

key = 'triumph|bmw|harley|ýamaha|kawasaki#ikasawak|ahamaý|yelrah|wmb|hpmuirt@251' # Dit is de sleutel
# Ieder opeenvolgend karakter versleuteld een opeenvolgend karakter in de tekst die verzonden wordt
# Na 73 karakters in de kekst beging de sleutel weer bij karakter 0 
# i = positie in de key waarvan een nummer gemaakt wordt
# % zorgt dat je sleutel in een lus blijft draaien

keylengte = len(key)
print(keylengte)
# uitkomst = 73

i = 0
test = key_value(key,i)
print(test) 
# uitkomst = 128 -> t in unicode = 116 dus ingevuld:
# (116 * 31 + 0 * 17 + (116 ^ (0 * 13))) % 256 =  (3596 + 0 + ((116 ^ 0) =116)) = 3712 % 256 = 128
# voor XOR kun je de calculator gebruiken op https://xor.pw/
# Uitleg %:
# 3712 % 256 betekent: wat is de rest als je 3712 deelt door 256? -> 128


