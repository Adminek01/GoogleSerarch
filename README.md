# GoogleSerarch

Oto kroki do zainstalowania, skonfigurowania i użycia programu z repozytorium GitHub: [GoogleSerarch](https://github.com/Adminek01/GoogleSerarch/tree/main):

### Instalacja:

1. **Pobierz repozytorium:**
   Możesz pobrać repozytorium bezpośrednio ze strony GitHub lub sklonować je za pomocą polecenia Git:
   ```
   git clone https://github.com/Adminek01/GoogleSerarch.git
   ```

2. **Zainstaluj wymagane biblioteki:**
   Przejdź do katalogu `GoogleSerarch` i zainstaluj wymagane biblioteki za pomocą `pip`:
   ```
   cd GoogleSerarch
   pip install -r requirements.txt
   ```

### Konfiguracja:

1. **Przygotuj plik z dorkami:**
   Przygotuj plik tekstowy zawierający dorki, z których chcesz korzystać. Każdy dork powinien być oddzielony nową linią.

2. **Opcjonalnie, skonfiguruj proxy:**
   Jeśli chcesz korzystać z proxy, możesz je skonfigurować, przekazując odpowiednie argumenty do programu. Pamiętaj, żeby używać prawidłowego formatu dla adresów proxy.

### Użycie:

Po zainstalowaniu i skonfigurowaniu programu możesz go użyć w następujący sposób:

```bash
python pagodo.py -g ścieżka/do/pliku/z/dorkami.txt
```

Gdzie `-g` to flaga określająca ścieżkę do pliku z dorkami.

Możesz również dostosować inne opcje w zależności od swoich potrzeb, np.:

- `-d` dla określenia domeny,
- `-o` dla zapisania wyników do pliku JSON,
- `-s` dla zapisania wyników do pliku tekstowego,
- `-p` dla użycia proxy, itp.

Po uruchomieniu programu będziesz mógł monitorować jego postęp, a wyniki zostaną zapisane zgodnie z wybranymi opcjami.
