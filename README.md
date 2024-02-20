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
Program `GoogleSerarch` służy do przeprowadzania pasywnych wyszukiwań w Google za pomocą dorków. Dorki to specjalne zapytania, które umożliwiają precyzyjne wyszukiwanie informacji w Google, co może być przydatne w celach badawczych, audytach bezpieczeństwa, pozyskiwaniu danych itp.

Przykładowa komenda użycia programu:
```bash
python pagodo.py -g all_google_dorks.txt -o results.json -s results.txt -p http://myproxy:8080
```

W powyższym przykładzie:
- `-g all_google_dorks.txt` określa plik zawierający dorki, które będą używane do wyszukiwania,
- `-o results.json` definiuje nazwę pliku, do którego zostaną zapisane wyniki w formacie JSON,
- `-s results.txt` określa nazwę pliku, do którego zostaną zapisane wyniki w formacie tekstowym,
- `-p http://myproxy:8080` włącza użycie proxy pod adresem `http://myproxy:8080`.

Po uruchomieniu programu z taką komendą, program rozpocznie przeszukiwanie Google za pomocą dorków zdefiniowanych w pliku `all_google_dorks.txt`. Wyniki wyszukiwania zostaną zapisane do plików `results.json` i `results.txt`. Dodatkowo, program będzie korzystał z proxy pod adresem `http://myproxy:8080`.
Oczywiście, oto kilka przykładowych komend, które możesz użyć w programie `pa
1. Wyszukiwanie dorków dla określonej domeny bez użycia proxy:
```bash
python pagodo.py -g all_google_dorks.txt -d example.com -o results.json -s results.txt
```

2. Wyszukiwanie dorków z określonym opóźnieniem między zapytaniami (np. 30 sekund między każdym zapytaniem):
```bash
python pagodo.py -g all_google_dorks.txt -i 30 -x 60 -o results.json -s results.txt
```

3. Wyszukiwanie dorków z wyłączoną weryfikacją SSL:
```bash
python pagodo.py -g all_google_dorks.txt -l -o results.json -s results.txt
```

4. Wyszukiwanie dorków z ograniczeniem maksymalnej liczby wyników na dork (np. 50 wyników na dork):
```bash
python pagodo.py -g all_google_dorks.txt -m 50 -o results.json -s results.txt
```

5. Wyszukiwanie dorków z wybranymi dorkami zamiast wszystkich (np. tylko dla dorka dotyczącego stron logowania):
```bash
python pagodo.py -g pages_containing_login_portals.dorks -o results.json -s results.txt
```

Pamiętaj, że możesz łączyć różne opcje zgodnie z potrzebami i dostosować parametry do swoich wymagań.
