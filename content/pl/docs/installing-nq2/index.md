---
title: "Instalacja NQ2"
description: "Przygotuj Node.js, Mosquitto i zależności systemowe, a następnie zainstaluj aplikację lokalną."
date: 2026-09-29
weight: 2
tags: [nq2, installation]
---
Ta instrukcja opisuje samodzielną instalację NQ2 na Debianie lub Ubuntu. Środowisko uruchomieniowe i broker MQTT przygotowujesz raz, a wybraną wersję aplikacji pobierasz z sekcji [Pliki]({{< relref "/files" >}}). Strony wydań zawierają listę zmian i linki do paczek.

## Wymagania

- Urządzenie i system operacyjny zgodne z architekturą pobieranej paczki. Pierwsza opublikowana paczka jest przeznaczona dla **ARM64**.
- Node.js: w tej instrukcji używamy **22.x**. Notatki instalacyjne projektu wymieniają również **20.x** dla istniejących instalacji.
- Działający **broker MQTT Eclipse Mosquitto**, na tym samym urządzeniu lub na innym dostępnym serwerze.
- Zależności systemowe: `git`, `make`, `g++`, `gcc` i `libsystemd-dev`; dodatkowo `curl` do przygotowania repozytorium oraz `unzip` do rozpakowania paczki.
- Katalog, w którym Twój użytkownik może zapisywać dane aplikacji, oraz uprawnienia administratora do instalowania pakietów systemowych.

ZIP aplikacji nie zawiera Node.js ani Mosquitto. Wybierz **jedną** z poniższych metod instalacji Node.js.

## Node.js przez APT

Dodaj repozytorium NodeSource i zainstaluj Node.js oraz wymagane zależności:

```sh
sudo apt-get update
sudo apt-get install -y curl ca-certificates
curl -fsSL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
sudo -E bash nodesource_setup.sh
sudo apt-get install -y nodejs git make g++ gcc libsystemd-dev unzip
sudo corepack enable

# Verify the installed version; this setup should output v22.x.
node --version
```

Pierwotne polecenie korzysta z `https://deb.nodesource.com/setup_lts.x`. Ten adres wskazuje bieżące wydanie LTS i może zainstalować wersję nowszą niż 20.x lub 22.x. Tutaj używamy `setup_22.x`, aby wynik był przewidywalny. Zobacz [instrukcję instalacji NodeSource](https://github.com/nodesource/distributions).

Jeśli Twoja dystrybucja Node.js nie udostępnia polecenia `corepack`, zainstaluj je przez `sudo npm install --global corepack`, a następnie ponów `sudo corepack enable`. Corepack przygotowuje polecenia menedżerów pakietów; nie uruchamia NQ2. Zobacz [dokumentację Corepack](https://github.com/nodejs/corepack).

## Alternatywa dla Ubuntu: Snap

Na Ubuntu z dostępnym `snapd` możesz zainstalować Node.js przez Snap zamiast metody NodeSource:

```sh
sudo apt-get update
sudo apt-get install -y curl git make g++ gcc libsystemd-dev unzip
sudo snap install node --classic --channel=22/stable
node --version
```

Oczekiwana wersja to `v22.x`. Jeśli Node.js jest już zainstalowany przez Snap, zmień kanał poleceniem `sudo snap refresh node --channel=22/stable`. Zobacz [pakiet Node.js w Snap](https://snapcraft.io/node).

Katalog instalacji Snap jest tylko do odczytu. Utwórz polecenia Corepack w katalogu swojego użytkownika:

```sh
mkdir -p "$HOME/.local/bin"
corepack enable --install-directory "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
```

Zachowaj wpis `PATH` w profilu powłoki, aby polecenia były dostępne w kolejnych sesjach. Jeśli Snap nie udostępnia Corepack, zainstaluj go przez `npm install --global --prefix "$HOME/.local" corepack`, dodaj ten katalog do `PATH` i ponów polecenie.

## Starszy sprzęt i386

Dla starszego, 32-bitowego sprzętu Intel notatki projektu wskazują [nieoficjalne wydania Node.js 20.9.0](https://unofficial-builds.nodejs.org/download/release/v20.9.0/) jako możliwą opcję. To wariant dla starszego sprzętu do sprawdzenia na docelowym urządzeniu, a nie przetestowana instalacja w tej instrukcji. Wymaga paczki aplikacji zgodnej z i386; dostępna paczka ARM64 nie jest przeznaczona dla sprzętu i386.

## Broker MQTT Mosquitto

Jeśli masz już działający serwer Mosquitto, użyj jego adresu i danych logowania. Aby zainstalować broker na tym samym urządzeniu z Debianem lub Ubuntu i systemd:

```sh
sudo apt-get update
sudo apt-get install -y mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
systemctl status mosquitto --no-pager
```

Sprawdź, czy usługa ma stan `active (running)`. Dla brokera na tym samym urządzeniu typowym adresem MQTT jest `mqtt://127.0.0.1:1883`. W połączeniu MQTT aplikacji NQ2 ustaw rzeczywisty adres brokera, port oraz skonfigurowaną nazwę użytkownika i hasło, jeśli są wymagane.

Mosquitto 2 może działać w trybie dostępnym tylko lokalnie. Jeśli NQ2 lub urządzenia MQTT łączą się z innej maszyny, najpierw skonfiguruj nasłuchiwanie w sieci i uwierzytelnianie na brokerze. Sama instalacja pakietu nie gwarantuje dostępu z sieci. Zobacz [opis konfiguracji Mosquitto](https://mosquitto.org/man/mosquitto-conf-5.html) i [instrukcję uwierzytelniania](https://mosquitto.org/documentation/authentication-methods/).

## Pobranie i sprawdzenie aplikacji

Wybierz wersję w sekcji [Pliki]({{< relref "/files" >}}) i pobierz ZIP. Karta pobierania wydania zawiera sumę SHA-256 oraz plik sumy kontrolnej.

Przykładowo dla wersji 1.0.0 umieść ZIP i jego plik `.sha256` w tym samym katalogu i wykonaj:

```sh
sha256sum -c nq2-arm64-local-1.0.0.zip.sha256
```

W systemie Windows oblicz sumę i porównaj ją z wartością na stronie wydania:

```powershell
Get-FileHash ./nq2-arm64-local-1.0.0.zip -Algorithm SHA256
```

Dla innej wersji użyj odpowiednich nazw pobranych plików.

## Instalacja i uruchomienie

1. Rozpakuj ZIP. Zachowaj wszystkie pliki i katalogi, w tym ukryty plik `.env`.
2. Otwórz rozpakowany katalog aplikacji. Dla wersji 1.0.0 jest to `_arm64-local-1.0.0`.
3. Edytuj `.env`: ustaw własne `ADMIN_EMAIL` i `ADMIN_PASSWORD` przed pierwszym uruchomieniem. Wersja 1.0.0 używa `PORT=8080`; zmień tę wartość, jeśli port jest już zajęty.
4. Otwórz terminal w tym katalogu i uruchom aplikację:

   ```sh
   node index.js
   ```

5. Poczekaj na komunikat o uruchomieniu serwera i otwórz `http://localhost:8080` w przeglądarce. Z innego urządzenia w tej samej sieci użyj `http://DEVICE_IP:8080`. Jeśli zmienisz `PORT`, użyj wybranego numeru portu.
6. Zaloguj się danymi administratora z `.env` i skonfiguruj połączenie ze swoim brokerem Mosquitto.

NQ2 działa, dopóki proces jest uruchomiony. Zatrzymasz go skrótem `Ctrl+C` w terminalu. Automatyczne uruchamianie NQ2 po restarcie zależy od systemu operacyjnego i nie jest konfigurowane przez samo rozpakowanie ZIP. Polecenie `systemctl enable` powyżej włącza automatyczny start **Mosquitto**, nie NQ2.
