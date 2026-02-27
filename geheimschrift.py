# Geheimschrift CLI - zonder imports libraries etc (alleen basis Python)
# Door Rudy

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

# Doel van onderstaande functie = van leesbare tekst naar gecodeerde lijst met getallen
def encrypt_text(plain, key):
    # zet tekst om naar "bytes" achtige waarden (0..255) door per karakter ord() te pakken
    # voor standaard tekst werkt dit prima (ASCII/Europaans). Emoji's kan, maar wordt snel groot.
    nums = []
    for i, ch in enumerate(plain):
        p = ord(ch)  # Unicode codepoint
        # we coderen dit naar twee bytes (0..255) zodat we alles kwijt kunnen:
        # high en low (256x256 werkt tot 65535; ruim voldoende voor tekens uit de Unicode standaard)
        hi = (p // 256) % 256
        lo = p % 256

        k1 = key_value(key, 2*i)
        k2 = key_value(key, 2*i + 1)

        # simpele verschuiving + extra mixing
        c1 = (hi + k1) % 256
        c2 = (lo + k2 + c1) % 256  # c1 beïnvloedt c2

        nums.append(c1)
        nums.append(c2)
    return nums

plain = "Dit is de standaard tekst van mij die ik als geheim bericht wil versturen met diverse tekens!"

VersleuteldeTekst = encrypt_text(plain, key)
print(VersleuteldeTekst) 

# Doel van onderstaande functie = van gecodeerde lijst met getallen naar  leesbare tekst
def decrypt_nums(nums, key):
# controle of de versleutelde tekst goed gekopieerd is. 
# het aantal getallen in de lijst moet deelbaar door 2 zijn.
# per karakter worden nl 2 getallen gegenereerd. nl eerste getal = c1 & tweede getal = c2
# als iemand fout kopieerd [12, 44, 90, 33, 17], dan zijn dat 5 getallen en dat kan dus niet
    if len(nums) % 2 != 0:
        raise ValueError("Ongeldige code: aantal getallen moet even zijn.")

    chars = []
    for i in range(0, len(nums), 2):
        c1 = nums[i]
        c2 = nums[i+1]

        k1 = key_value(key, i)
        k2 = key_value(key, i+1)

        hi = (c1 - k1) % 256
        lo = (c2 - k2 - c1) % 256  # c1 zat in encryptie bij c2

        codepoint = hi * 256 + lo
        chars.append(chr(codepoint))
    return "".join(chars)

nums = VersleuteldeTekst
OntsleuteldeTekst = decrypt_nums(nums, key)
print(OntsleuteldeTekst) 

def read_multiline(prompt): # promt is een stuk tekst uit het hoofdprogramma
                            # er zijn nl 2 modi mogelijk, C of D (coderen of decoderen)
    print(prompt)
    print("(Typ/plak tekst. Eindig met een lege regel en druk Enter.)")
    lines = []
    while True:
        line = input()
        if line == "": # dit is waarom het programma een "lege regel" nodig heeft...
            break
        lines.append(line) # regel toevoegen aan de input
    return "\n".join(lines) # \n gebruiken voor "newline"

# Dit stukje heb ik door AI moeten laten maken, ik kwam er niet uit. In de comments wat het doet,
    def parse_number_list(s):
    # verwacht iets als: [12, 34, 56] of 12,34,56 of "12 34 56"
    s = s.strip()       # spaties aan begin en einde verwijseren
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1].strip() # "[" en "]" aan begin en eidne van de tekst verwijderen

    # vervang komma's door spaties en split
    s = s.replace(",", " ")
    parts = [p for p in s.split() if p.strip() != ""] # Dit “[p for p in s.split()]” doet: 
                             # Voor elk element p uit s.split(), stop p in een nieuwe lijst.
                             # p.strip() verwijdert spaties aan begin en eind van een stukje tekst.
                             # daarna: Neem alleen p mee als het na het strippen niet leeg is. (dus “22” wel en “” niet)

    nums = []
    for p in parts:  # controle regels
        if not p.isdigit():
            raise ValueError("Ongeldige code: alleen positieve gehele getallen gebruiken.")
        n = int(p)
        if n < 0 or n > 255:
            raise ValueError("Ongeldige code: elk getal moet tussen 0 en 255 zitten.")
        nums.append(n)
    return nums

# De hoofdcode
def main():
    print("=== Geheimschrift CLI (zonder imports) ===")
    mode = input("Wil je coderen of decoderen? (C/D): ").strip().lower()
    if mode not in ("c", "d"):
        print("Ongeldige keuze. Kies C of D.")
        return

    print("\nVul 5 kernwoorden in (beide kanten exact hetzelfde).")
    words = []
    for i in range(1, 6):
        words.append(input(f"Kernwoord {i}: "))

    try:
        key = build_key(words)
    except ValueError as e:
        print("Fout:", e)
        return

    if mode == "c":
        text = read_multiline("\nTekst om te CODEREN:")
        if text == "":
            print("Geen tekst ontvangen.")
            return
        code = encrypt_text(text, key)
        print("\n--- GECODEERDE TEKST (kopieer alles) ---")
        print(code)  # print als Python-lijst zodat deze makkelijk te plakken is
        print("--------------------------------------")

    else:
        coded = read_multiline("\nPlak de GECODEERDE code (lijst met getallen):")
        coded = coded.strip()
        if coded == "":
            print("Geen code ontvangen.")
            return
        try:
            nums = parse_number_list(coded)
            text = decrypt_nums(nums, key)
        except ValueError as e:
            print("Fout:", e)
            return

        print("\n--- GEDECODERDE TEKST ---")
        print(text)
        print("--------------------------")

if __name__ == "__main__":
    main() # Dit start het programma