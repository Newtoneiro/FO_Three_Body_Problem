# Symulacja problemu trzech ciał

## Opis problemu

Problem trzech ciał jest zagadnieniem z zakresu dynamiki klasycznej, w którym należy obliczyć trajektorie ruchu trzech ciał poruszających się pod wpływem wzajemnego oddziaływania grawitacyjnego.

## Instrukcja obsługi

Aby uruchomić symulację należy wykonać następujące kroki:

1. Sklonować repozytorium
2. Utworzyć środowisko wirtualne (`python3 -m venv venv`)
3. Aktywować środowisko wirtualne (`source venv/bin/activate`)
4. Zainstalować wymagane biblioteki z pliku requirements.txt (`pip install -r requirements.txt`)
5. Uruchomić plik run.py z odpowiednimi argumentami (opis argumentów poniżej)

Kroki 2 i 3 są opcjonalne, ale zalecane.

## Argumenty

- `--help` - wyświetla pomoc
- `--simulation1` - ustawia parametry symulacji 1
- `--simulation2` - ustawia parametry symulacji 2

Aby program włączył symulację, należy podać parametry pierwszej symulacji.

### Argumenty symulacji

Argumenty należy podać w następującej kolejności:

1. Odległość początkowa
2. Masa ciał
3. Stała grawitacyjna

### Przykładowe użycie

`python3 run.py --simulation1 400 1000 0.4 --simulation2 400 1000 0.3999`

Komenda uruchomi symulację 1 i 2 z parametrami:

- Odległość początkowa: 400 dla obu symulacji
- Masa ciał: 1000 dla obu symulacji
- Stała grawitacyjna: 0.4 dla symulacji 1 i 0.3999 dla symulacji 2

## Kontrola symulacji

Symulacja jest sterowana za pomocą klawiatury. Możliwe akcje:

- `r` - resetuje symulację
- `g` - włącza/wyłącza graf
- `t` - włącza/wyłącza ścieżki
- `v` - włącza/wyłącza wektory prędkości
