# **VYLEPŠENÝ TASK MANAGER**
## **Popis**
Tento projekt je správce úkolů pomocí databáze SQL.
Umožňuje vytváření, zobrazování, mazání úkolů a upravování jejich statusu.
Dále je zde testování pozitivních a negativních vstupů funkcí vytvoření, mazání a upravení statusu.
Správce úkolů běží na produkční databázi, testování potom v testovací databázi.
## **Použité technologie a knihovny**
- Python 3.11.3
- MySQL Connector
- pytest
## **Instalace knihoven**
- Vytvoř nové virtuální prostředí.
- Nainstaluj potřebné knihovny
```bash
$ pip install -r requirements.txt
```
## **Konfigurace databáze**
- Vytvoř soubor `.env` pro produkční databázi a vyplň data:
```
DB_HOST=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=...
```
- Vytvoř soubor `.env.test` pro testovací databázi a vyplň data,
název `DB_NAME=` musí začínat `test_` :
```
DB_HOST=...
DB_USER=...
DB_PASSWORD=...
DB_NAME=...
```
## **Použití/spuštění**
- Pro použití správce úkolů spusť `main.py`.
- Pro spuštění testování otevři `test_functions` a spusť:
```bash
$ pytest test_functions.py
 ```
Autor: Pavel Nováček  
Vytvořeno v rámci kurzu testování s Pythonem.