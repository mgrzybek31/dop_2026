# dop_2026

## Eksperyment ofiara–drapieżnik

Do uruchomienia potrzeba Pythona 3.11+. Z katalogu projektu zainstaluj projekt
raz, razem z zależnościami do notebooka zadeklarowanymi w `pyproject.toml`:

```powershell
python -m venv venv
venv/Scripts/activate
python -m pip install ".[notebook]"
```

Wersja terminalowa jest dostępna jako `symulacja`. Jeśli katalog skryptów Pythona
nie jest w `PATH`, użyj `python -m src.prey_predator_sim.simulation`.

Otwórz [notebook](eksperymenty.ipynb) w VS Code. W menu **Select Kernel** wybierz
tego samego Pythona, którym wykonano instalację projektu, kliknij **Run All**.
