---
title: "Installing NQ2"
description: "Prepare Node.js, Mosquitto, and system dependencies, then install the local application."
date: 2026-09-29
weight: 2
tags: [nq2, installation]
---
This guide covers a standalone NQ2 installation on Debian or Ubuntu. Prepare the runtime and MQTT broker once, then download the application version you want from [Files]({{< relref "/files" >}}). Release pages contain the changelog and package links.

## Requirements

- A device and operating system matching the architecture of the downloaded package. The first published package is **ARM64**.
- Node.js: use **22.x** for this setup. The project's installation notes also list **20.x** for existing installations.
- A running **Eclipse Mosquitto MQTT broker**, either on the same device or on another accessible server.
- `git`, `make`, `g++`, `gcc`, and `libsystemd-dev` as system dependencies; `curl` to prepare the repository and `unzip` to extract the package.
- A directory where your user can write application data, and administrator access for installing system packages.

The application ZIP does not include Node.js or Mosquitto. Choose **one** of the Node.js installation methods below.

## Node.js through APT

Set up the NodeSource repository and install Node.js and the required dependencies:

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

The original command uses `https://deb.nodesource.com/setup_lts.x`. That address follows the current LTS release and can install a version newer than 20.x or 22.x. This guide pins `setup_22.x` to keep the result consistent. See the [NodeSource installation instructions](https://github.com/nodesource/distributions).

If `corepack` is missing from your Node.js distribution, install it with `sudo npm install --global corepack`, then repeat `sudo corepack enable`. Corepack prepares package-manager commands; it does not start NQ2. See the [Corepack documentation](https://github.com/nodejs/corepack).

## Ubuntu alternative: Snap

On Ubuntu with `snapd` available, you can install Node.js through Snap instead of the NodeSource method:

```sh
sudo apt-get update
sudo apt-get install -y curl git make g++ gcc libsystemd-dev unzip
sudo snap install node --classic --channel=22/stable
node --version
```

The expected version is `v22.x`. If Node.js is already installed through Snap, switch its channel with `sudo snap refresh node --channel=22/stable`. See the [Node.js Snap package](https://snapcraft.io/node).

Snap's installation directory is read-only. Create Corepack's launchers in your user directory:

```sh
mkdir -p "$HOME/.local/bin"
corepack enable --install-directory "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
```

Keep the `PATH` entry in your shell profile to use these launchers in future sessions. If the Snap does not provide Corepack, install it with `npm install --global --prefix "$HOME/.local" corepack`, then retry after adding that directory to `PATH`.

## Older i386 hardware

For older 32-bit Intel hardware, the project notes suggest the [unofficial Node.js 20.9.0 builds](https://unofficial-builds.nodejs.org/download/release/v20.9.0/) as a possible option. This is a legacy path to verify on the target device, not a tested installation in this guide. It requires an application package compatible with i386; the available ARM64 package is not intended for i386 hardware.

## Mosquitto MQTT broker

If you already have a working Mosquitto server, use its address and credentials. To install one on the same Debian/Ubuntu device with systemd:

```sh
sudo apt-get update
sudo apt-get install -y mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
systemctl status mosquitto --no-pager
```

Confirm that the service is `active (running)`. For a broker on the same device, the usual MQTT endpoint is `mqtt://127.0.0.1:1883`. Configure NQ2's MQTT connection with the actual broker address, port, and any configured username and password.

Mosquitto 2 can run in local-only mode. If NQ2 or MQTT devices connect from another machine, configure a network listener and authentication on the broker first. Installing the package alone does not guarantee network access. See the [Mosquitto configuration reference](https://mosquitto.org/man/mosquitto-conf-5.html) and [authentication guide](https://mosquitto.org/documentation/authentication-methods/).

## Download and verify the application

Choose a version in [Files]({{< relref "/files" >}}) and download its ZIP. The release's download card includes a SHA-256 value and a checksum file.

For example, place the 1.0.0 ZIP and its `.sha256` file in the same directory and run:

```sh
sha256sum -c nq2-arm64-local-1.0.0.zip.sha256
```

On Windows, calculate the checksum and compare it with the value on the release page:

```powershell
Get-FileHash ./nq2-arm64-local-1.0.0.zip -Algorithm SHA256
```

Use the corresponding file names when downloading another version.

## Install and run

1. Extract the ZIP. Keep all files and folders, including the hidden `.env` file.
2. Open the extracted application folder. For version 1.0.0, it is `_arm64-local-1.0.0`.
3. Edit `.env`: set your own `ADMIN_EMAIL` and `ADMIN_PASSWORD` before the first start. Version 1.0.0 uses `PORT=8080`; change it if the port is already in use.
4. Open a terminal in that folder and start the application:

   ```sh
   node index.js
   ```

5. Wait for the server startup message, then open `http://localhost:8080` in your browser. From another device on the same network, use `http://DEVICE_IP:8080`. If you changed `PORT`, use your configured port instead.
6. Sign in with the administrator credentials from `.env` and configure the connection to your Mosquitto broker.

NQ2 runs while the process is active. Press `Ctrl+C` in the terminal to stop it. Automatic startup of NQ2 after a reboot depends on the operating system and is not configured by extracting the ZIP. The `systemctl enable` command above enables automatic startup of **Mosquitto**, not NQ2.
