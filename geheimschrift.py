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

MijnMotoren = ['Triumph', 'BMW', 'Harley', 'Ýamaha', 'Kawasaki']

test = build_key(MijnMotoren)
print(test)