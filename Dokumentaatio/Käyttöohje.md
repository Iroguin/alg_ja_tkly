# Käyttöohje:

Kloonaa repositorio

Asenna poetry komennolla:
```
pip install poetry
```
Asenna seuraavaksi projektin riippuvuudet komennolla:
```
poetry install
```
Shell ympäristöön voi päästä komennolla:
```
poetry shell
```

## Ohjelman käyttäminen

Jos olet shell ympäristössä ohjelman voi aloittaa komennolla:
```
invoke play
```
Tämä pelaa pelin expectimax algorytmillä ja syvyydellä 3. 
Muuten shell ympäristön ulkopuolella pelin voi aloittaa komennolla:
```
poetry run invoke play
```

Tarkempia ohjeita voi antaa komenolla:
```
python play_game.py expectiminimax 4
```
esimerkkinä expectiminimax on algorytmin nimi ja numero 4 on syvyys. depth_one on toinen käytettävä algorytmi.

## Muita komentoja / testaus

Muita komentoja joita voi käyttää ovat esimerkiksi: 
```
Invoke Test
```
muuten
```
Poetry run invoke test
```
Coverage raportin voi saada shell ympäristössä komennolla:

```
Invoke coverage
```
muuten
```
Poetry run invoke coverage
```
