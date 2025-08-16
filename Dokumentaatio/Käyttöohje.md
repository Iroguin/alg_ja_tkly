# Käyttöohje:
## Ohjelman asentaminen

Kloonaa repositorio

Repositiossa asenna poetry komennolla:
```
pip install poetry
```
Asenna seuraavaksi projektin riippuvuudet komennolla:
```
poetry install

```
## Shell ympäristö

Shell ympäristöön voi päästä komennolla:
```
poetry shell
```
poetryn uudemmissa versioissa voit käyttää komentoa:
```
eval $(poetry env activate)
```
Jos olet shell ympäristössä kaikkista komennoista voi lyhentää pois "poetry run" osan

## Ohjelman käyttäminen

ohjelman voi aloittaa komennolla:
```
poetry run invoke play
```
Tämä pelaa pelin expectimax algorytmillä ja syvyydellä 3. 


Tarkempia ohjeita voi antaa komenolla:
```
poetry run invoke play --algorithm=<algorytmin nimi> --depth=<syvyys>
```
esimerkkinä expectiminimax on algorytmin nimi ja numero 4 on syvyys. depth_one on toinen käytettävä algorytmi.

## Muita komentoja / testaus

Muita komentoja joita voi käyttää ovat esimerkiksi: 
Koodin testien suorittaminen:
```
Poetry run invoke test
```
Coverage raportin voi saada shell ympäristössä komennolla:
```
Poetry run invoke coverage
```
Koodin linttaus taoimii komennolla:
```
Poetry run invoke lint
```
Suuren pelimäärän analysointi:
```
invoke measure --games=<pelimäärä> --algorithm=<slgorytmin nimi> --depth=<syvyys>
```
