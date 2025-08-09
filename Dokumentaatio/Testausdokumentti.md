# Testausdokumentti

![alt text](<Coverage_report-5.png>)

Raportin voi saada komennolla
```
poetry run invoke coverage
```

Mitä on testattu, miten tämä tehtiin?
Testatut tiedostot:
    - game.py
    - evaluation.py
    - play_game.py
        - huono coverage score johtuu siitä että sys argumentteja ei testata
    - expecitminimax.py
    - depth_one_move.py

Tiedostot viellä testaamatta:
    - none

Minkälaisilla syötteillä testaus tehtiin?
    - testaus tapahtuu suurimmaksi osaksi eri lauta tilanteilla esim tyhjä lauta

Miten testit voidaan toistaa?
    - Testit voi toistaa komenolla
    ```
    Poetry run invoke test
    ```
    - yksittäisiä testi tiedostoja voi suoritta komenolla
    ```
    Poetry run pytest src/tests/<hakemiston nimi>
    ```
