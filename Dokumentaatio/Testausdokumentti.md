# Testausdokumentti

![alt text](<coverage_reports/Coverage_report-6.png>)

Raportin voi saada komennolla
```
poetry run invoke coverage
```

Mitä on testattu, miten tämä tehtiin?
Testatut tiedostot:
    - game.py
    - evaluation.py
    - play_game.py
    - expecitminimax.py
    - depth_one_move.py
    - measure.py

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
