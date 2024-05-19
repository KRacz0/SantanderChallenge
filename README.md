# SantanderChallenge - Parser Logów GC

## Przegląd

Ten skrypt jest zaprojektowany do parsowania plików logów Java Garbage Collector (GC) i wyodrębniania istotnych danych na temat przestrzeni pamięci Eden, Survivors i Heap. Wyodrębnione dane są następnie zapisywane do pliku JSON.

## Funkcje

- Parsowanie plików logów GC w celu wyodrębnienia istotnych metryk przestrzeni pamięci.
- Zapis danych w formacie JSON.

## Wymagania

- Python 3.12

## Instalacja

1. Sklonuj repozytorium lub pobierz skrypt `parse_gc_log.py`.
2. Upewnij się, że masz zainstalowany Python 3.12 na swoim komputerze.

## Użycie

Skrypt wymaga dwóch argumentów:
1. `input_log_file`: Nazwa wejściowego pliku logu GC (np. `gc.log`).
2. `output_json_file`: Nazwa wyjściowego pliku JSON (np. `output.json`).

### Komenda

```bash
python parse_gc_log.py <input_log_file> <output_json_file>
```
## Przykładowy Output
```json
[
  {
    "timestamp": "2024-05-13T14:25:53.606+0200",
    "eden_size": "3664.0",
    "survivors_size": "8",
    "heap_size": "5415.9",
    "GC_name": "GC pause (G1 Evacuation Pause)",
    "phase": "before"
  },
  {
    "timestamp": "2024-05-13T14:25:53.606+0200",
    "eden_size": "0",
    "survivors_size": "8",
    "heap_size": "1705.2",
    "GC_name": "GC pause (G1 Evacuation Pause)",
    "phase": "after"
  },
]
```
