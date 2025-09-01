# Testausdokumentti

![Report png](<coverage_reports/Coverage_report_final.png>)

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

Tehokkuuta voi testata komennolla
    ```
    poetry run invoke measure
    ```
    standardina on 100 peliä ja syvyys 3 mutta nämä voi muuttaa:
    Esim: invoke measure --games=200 --depth=4

vimmeisin testaukseni:
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