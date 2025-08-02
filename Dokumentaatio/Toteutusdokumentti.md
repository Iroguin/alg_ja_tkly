# Toteutuksen rakenne

## Ydinmoduulit:
game.py - Pelin peruslogiikka ja säännöt
play_game.py - Määrittää algorytmin ja depthin ja pelaa pelaa pelin
expectiminimax.py - Pääalgorytmi pelin pelaamista varten
evaluation.py - Pelitilan arviointi ja heuristiikkafunktiot

## Testaus ja mittaus:
Automaattinen pelitestaus eri parametreilla


## Suorituskyky- ja O-analyysivertailu
Expectimax-algoritmi:
Aikavaativuus: O(b^d)
b = haarautumiskerroin
d = hakusyvyys

## Työn mahdolliset puutteet ja parannusehdotukset
projektista puuttuu paljon mittauksia
Saavutettujen pisteiden ja 2048-laatan saavuttamisprotentin mittaus
Suorituskykytestit eri hakusyvyyksillä


## Laajojen kielimallien (ChatGPT yms.) käyttö
Claude on ainoa kielimalli jota olen käyttänyt.
Käytetty:
    - Käytin sitä projektin alussa määrittelydokumenttin laatimista varten
    - Käytin laatiessani testejä esim miten mock toimii ja miten pystyisin testaamaan satunnasta logiikkaa

