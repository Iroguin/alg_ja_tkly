# Viikkoraportti - Viikko 2
Projekti: 2048 Peli
Viikon työaika yhteensä: noin 15 tuntia

1. Mitä olen tehnyt tällä viikolla:
Tällä viikolla olen keskittynyt saamaan projektin toimivaan kuntoon, sekä tekemään testit peliä varten.
Projektin ydin on aloitettu nyt kun kaikki on toimimassa.

2. Miten ohjelma on edistynyt?
Pelin koodi toimii ja on suurimmaksi osaksi valmis, sille on myös testejä.
Laudan arvioimista varten on toimiva jos optimoimaton heurestiikka functio jolle ei ole viellä testejä.
Erittäin simppeli algorytmi on tehty joka pystyy pelaamaan peliä käyttäen heurestiikka funktiota. (ei testejä viellä)

3. Mitä opin tällä viikolla / tänään?
Opin paljon expectiminimax functiosta vaikka en ole viellä implementoinnut sitä.
Koodin abstraktio pitää olla mielessä samalla kun koodaa.

4. Mikä jäi epäselväksi tai tuottanut vaikeuksia?
Kaikki on selvää tällä hetkellä

5. Seuraavan viikon tavoitteet (ja muidenkin tulevien viikojen):
Toimiva expectiminimax algorytmi
Hiottu evaluaatio funktio
paljon parempi algorytmi joka pääsisi pidemmälle (nykyinen harvoin pääsee yli 256)
Pylint koodin luettavuuden hiomista varten
Testit kaikille koodin osille
Parempi käyttöliittymä käyttäen flageja
    esim depthin ja pelimäärien päätäminen
    voi vaihtaa eri algorytmien välillä
Dokumentaation parantaminen diagrammeilla jotta näkee mikä puhuu mille
Käytettävä käyttöohje
Readme täytetty hyödyllisellä infolla


6. Tämän viikon tavoitteet
- [x] Pelin peruslogiikan toteutus (varmaan game.py)
- [x] 4x4 pelilaudan käsittely
- [x] Siirtojen toteutus (ylös, alas, vasen, oikea)
- [x] Uusien laattojen generointi
- [x] Pelin päättymisen tunnistus
- [ ] Basic Expectimax-algoritmi (syvyys 2-3)
- [x] Yksinkertainen heuristiikkafunktio (tyhjät ruudut + suurin numero)

- [x] Testausympäristön rakentaminen
- [ ] pelitestaus (peruspelille on testit mutta muulle koodille ei)
