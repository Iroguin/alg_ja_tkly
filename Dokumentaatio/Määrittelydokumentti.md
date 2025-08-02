# 2048 Peli - Määrittelydokumentti
## Perustiedot
Luotu ja viimmeksi muokattu viikolla 1

Opinto-ohjelma: Tietojenkäsittelytieteen kandidaatti (TKT)
Dokumentaatio Kieli: Suomi
Ohjelmointikieli: Python
Muita hallitsemia kieliä: None

## Ongelma ja tavoite
Ongelman kuvaus: 2048 on peli, jossa pelaaja liikuttaa numerolaattoja 4x4-ruudukossa. 
Tavoitteena on yhdistää samanarvoiset numerot suuremmiksi ja päästä 2048-laattaan. 
Peli päättyy, kun ruudukko täyttyy eikä liikkeitä ole enää mahdollista tehdä.

## Harjoitustyön ydin
Projektin ydin on tekoälyalgoritmin toteutus ja optimointi, ei 2048-pelin käyttöliitymän ohjelmointi. 
Vaikka toimiva käyttöliittymä tarvitaan tekoälyn testaamiseen, se on vain tukikomponentti. 
Aiheen ydin koostuu algoritmejen implementoinnista.
Suurin osa kehitysajasta kuluisi algoritmin hienosäätöön ja erilaisten heuristiikkayhdistelmien kokeiluun. 
Pelin toteutus pidetään mahdollisimman yksinkertaisena, jotta fokus pysyy tekoälyssä.

### Ratkaistavat haasteet:
Pelin logiikan toteutus (liikkeet, yhdistämiset, uusien laattojen generointi)
Tekoälyn kehittäminen joka pelaa peliä optimaalisesti
Pelitilan evaluointi ja parhaan siirron valinta

## Algoritmit ja tietorakenteet
### Pääalgoritmit:
-Expectimax-algoritmi
Käsittelee pelaajan siirtoja ja satunnaisia tapahtumia
Expectimax Soveltuu paremmin kuin Minimax satunnaisuutta sisältäviin peleihin
-Heuristiikkafunktiot
Monotonisuus-heuristiikka (suurimmat numerot kulmissa/reunoilla)
Sujuvuus-heuristiikka (pienet erot vierekkäisten laattojen välillä)
Tyhjien ruutujen heuristiikka

## Tietorakenteet:
2D-matriisi (lista listoista)
Pelilaudan tallentamiseen (4x4)
Tila-avaruuden koko: 2^16 mahdollista tilaa
Hakupuu
Implisiittinen puurakenne Expectimax-algoritmin hakuun
Prioriteettijono/lista
Mahdollisten siirtojen järjestämiseen heuristiikan mukaan

## Syötteet ja niiden käyttö
### Syötteet:
Pelitila (4x4 matriisi numeroita)
Sallitut siirrot (ylös, alas, vasen, oikea)
Hakusyvyys (konfiguroitava parametri)
Heuristiikkapainot (säädettävät kertoimet)
### Syötteiden käyttö:
Pelitila toimii Expectimax-algoritmin juurisolmuna
Algoritmi generoi rekursiivisesti kaikki mahdolliset seuraavat tilat
Heuristiikkafunktiot arvioivat jokaisen tilan arvon

## Aika- ja tilavaativuudet
Expectimax-algoritmi:
Aikavaativuus: O(b^d)
b = haarautumiskerroin
d = hakusyvyys
Käytännössä ~18^6 ≈ 34 miljoonaa solmua syvyydellä 6

Tilavaativuus: O(d)
Selvitä myöhemmin
Aikavaativuus parannus: O(b^(d/2)) parhaassa tapauksessa kai

## Lähteet
https://en.wikipedia.org/wiki/Expectiminimax
https://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf
