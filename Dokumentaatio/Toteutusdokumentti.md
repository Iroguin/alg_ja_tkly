# Toteutuksen rakenne

## Ydinmoduulit:
game.py - Pelin peruslogiikka ja säännöt
play_game.py - Määrittää algorytmin ja depthin ja pelaa pelaa pelin
expectiminimax.py - Pääalgorytmi pelin pelaamista varten
evaluation.py - Pelitilan arviointi ja heuristiikkafunktiot
measure.py - Pelien analysointia varten tehty tiedosto (tällä hetkellä ei toimiva)

## Testaus ja mittaus:
Automaattinen pelitestaus eri parametreilla

## Suorituskyky

## O-analyysivertailu

d on hakusyvyys
n on laudan koko (tässä tapauksessa 4)

Pelaajan vuoro (maksimointi):
Tutkii 4 mahdollista siirtoa (UP, DOWN, LEFT, RIGHT)
Jokainen siirto haarautuu

Satunnaisen laatan sijoitus:
Jokaiselle tyhjälle ruudulle on 2 vaihtoehtoa:
Laatan 2 sijoitus (90% todennäköisyys)
Laatan 4 sijoitus (10% todennäköisyys)

Max 16 tyhjää ruutua luo max 32 haaraa

Haarautumiskerroin vaihtelee tasojen välillä:
Pelaajan solmuissa: 4 haaraa (4 suuntaa)
Sattuman solmuissa: 2 × (tyhjien ruutujen määrä) haaraa

Pahimmassa tapauksessa (pelin alussa, paljon tyhjiä ruutuja):
Pelaajan vuoro: 4 haaraa
Sattuman vuoro: ~30-32 haaraa (15-16 tyhjää ruutua × 2 laatta-arvoa)
Tämä antaa pahimman tapauksen haarautumiskertoimeksi noin 4 × 30 = 120 per kokonainen taso (pelaaja + sattuma).

Koska tyhjien ruutujen määrä vaihtelee pelin aikana, vaativuus on:
Pahin tapaus: O((4 × 2n^2)^(d/2)) ≈ O(120^(d/2)) vuorotteleville pelaaja/sattuma solmuille
Keskimääräinen tapaus: O((4 × 2k)^(d/2)) missä k on tyhjien ruutujen keskimäärä
Käytännön vaativuus: Noin O(4^d × n^2) koska laudan operaatiot ovat O(n^2)

Tämän tyhjien ruutujen suuri haaraisuusmäärä on täksi rajoitettu maksimissaan seitsemään.

## Työn mahdolliset puutteet ja parannusehdotukset
Suorituskykytestit eri hakusyvyyksillä
Luulen että expectiminimax algorytmini on melko hidas

## Nykyinen tehokkuus (invoke measure)
500 games with expectiminimax algorithm (depth=3)
==================================================
RESULTS SUMMARY
==================================================
Games played: 500
Total time: 765.31 seconds
Time per game: 1.53 seconds
Game speed: 0.0030 seconds per move

Win rate (2048 reached): 0.8% (4/500)
Average moves per game: 515.5
Average score: 1138.7

Min score: 286 | Max score: 3644
Min moves: 127 | Max moves: 1645

Max tile distribution:
   2048:   4 games (  0.8%) 
   1024:  84 games ( 16.8%) ████████
    512: 214 games ( 42.8%) █████████████████████
    256: 156 games ( 31.2%) ███████████████
    128:  38 games (  7.6%) ███
     64:   4 games (  0.8%)

## Laajojen kielimallien (ChatGPT yms.) käyttö
Claude on ainoa kielimalli jota olen käyttänyt.
Käytetty:
    - Käytin sitä projektin alussa määrittelydokumenttin laatimista varten
    - Käytin laatiessani testejä esim miten mock toimii ja miten pystyisin testaamaan satunnasta logiikkaa
    - Bugejen löytämisessä olen nyt käyttänyt paljon
    - käytin nyt viikolla 6 paljon optimisointien löytämiseen.
