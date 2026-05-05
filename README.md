# Mikroserwisowy system logowania (REST + Docker)

Projekt zaliczeniowy z wykorzystaniem mikroserwisów, dockera oraz tokenów JWT. 

## Architektura systemu
System składa się z dwóch niezależnych kontenerów Dockerowych:
1. **auth-service**: Serwis autoryzacyjny z logiką JWT. Nie jest wystawiony na zewnątrz (ukryty w sieci Dockera). Odpowiada za weryfikację loginu/hasła i wydawanie tokenów oraz sprawdzanie ich ważności.
2. **main-service**: Główna aplikacja, wystawiona na porcie publicznym (8000). Chroni dostęp do zasobów (`/tajne-dane`). Przed zwróceniem danych, komunikuje się wewnętrznie z `auth-service` w celu walidacji tokenu.

## Wymagania techniczne (spełnione w projekcie)
- **Rozdzielenie logiki:** 2 osobne kontenery (Microservices).
- **Optymalizacja obrazów:** Użyto odchudzonych obrazów `python:3.11-slim`.
- **Zmienne środowiskowe:** Hasła i klucze wczytywane z pliku `.env` (zakaz hardkodowania).

## Instrukcja uruchomienia
1. Upewnij się, że masz plik `.env` w głównym katalogu projektu.
2. Zbuduj i uruchom kontenery w tle:
   ```bash
   docker-compose up -d --build
