# Geheimschrift CLI - zonder imports (alleen basis Python)
# test

def normalize(s):
    # consistent maken: trim + lower
    return s.strip().lower()

def build_key(words):
    # words: lijst met 5 kernwoorden
    w = [normalize(x) for x in words]
    if len(w) != 5 or any(x == "" for x in w):
        raise ValueError("Je moet precies 5 niet-lege kernwoorden invullen.")

    # maak 1 sleuteltekst
    key = "|".join(w)

    # extra "mix": herhaal en draai wat om zodat het langer wordt
    # (zodat korte sleutelwoorden toch meer invloed hebben)
    key2 = key + "#" + key[::-1] + "@" + str(len(key) * 7 + 13)

    return key2

def key_value(key, i):
    # haal een getal 0..255 uit de sleutel voor positie i
    ch = key[i % len(key)]
    base = ord(ch)  # 0..(Unicode)
    # maak er een 0..255 van (simpele mix)
    return (base * 31 + i * 17 + (base ^ (i * 13))) % 256

def encrypt_text(plain, key):
    # zet tekst om naar "bytes" achtige waarden (0..255) door per karakter ord() te pakken
    # voor standaard tekst werkt dit prima (ASCII/Europaans). Emoji's kan, maar wordt snel groot.
    nums = []
    for i, ch in enumerate(plain):
        p = ord(ch)  # Unicode codepoint
        # we coderen dit naar twee bytes (0..255) zodat we alles kwijt kunnen:
        # high en low (werkt voor codepoints tot 65535; ruim voldoende voor veel schoolteksten)
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

def decrypt_nums(nums, key):
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

def read_multiline(prompt):
    print(prompt)
    print("(Typ/plak tekst. Eindig met een lege regel en druk Enter.)")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)

def parse_number_list(s):
    # verwacht iets als: [12, 34, 56] of 12,34,56 of "12 34 56"
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1].strip()

    # vervang komma's door spaties en split
    s = s.replace(",", " ")
    parts = [p for p in s.split() if p.strip() != ""]

    nums = []
    for p in parts:
        if not p.isdigit():
            raise ValueError("Ongeldige code: alleen positieve gehele getallen gebruiken.")
        n = int(p)
        if n < 0 or n > 255:
            raise ValueError("Ongeldige code: elk getal moet tussen 0 en 255 zitten.")
        nums.append(n)
    return nums

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
        print(code)  # print als Python-lijst zodat je 'm makkelijk kunt plakken
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
    main()
