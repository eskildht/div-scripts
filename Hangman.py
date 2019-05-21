bokstaver_gjettet = []
hemmelig_ord = input("Skriv inn hemmelig ord: ")
antall_liv = int(input("Angi antall liv: "))
                 
while antall_liv > 0:
    gjett = input("Gjett: ").lower()
    
    if gjett not in bokstaver_gjettet:
        bokstaver_gjettet.append(gjett)
    else:
        print("Bokstaven er allerede gjettet")
        continue
    
    if gjett in hemmelig_ord:
        print("Stemmer, bokstaven", gjett, "er i ordet")
        c = ""
        for x in range(len(hemmelig_ord)):
            c += hemmelig_ord[x] if hemmelig_ord[x] in bokstaver_gjettet else "*"
        print(c)
        if "*" not in c:
            print("Ordet er gjettet!")
            break
    else:
        antall_liv -= 1
        print("Bokstaven", gjett, "er ikke i ordet")
        print("Antall liv igjen:", antall_liv)
        if antall_liv == 0:
            print("Du har tapt")
            break
