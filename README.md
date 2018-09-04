# Scriptd

Scriptd lets you execute a set of preconfigured scripts or executables via HTTP API, securely, without exposing terminal access, and with almost no configurations.

Designed for remote job automation when direct SSH is not desirable, Scriptd helps you deal with situations when your development server is behind firewalls or your corporation's security policy forbids direct SSH access. Write down your code updating / building / deployment commands as scripts and you are good to go with HTTP access only. And no, you are not exposing your server to code injections: only your preconfigured scripts are allowed to run.

## Features

- Setting up preconfigured scripts as HTTP API for remote job automation.
- Almost zero configuration: a work directory with your scripts inside, and a secret key, that's all.
- No terminal exposure: scriptd does not run any code or parameters from client requests, only your preconfigured scripts. No code injection.
- Security: encryption & authentication with AES-256-GCM.

## Usage

### Server

```
scriptd [-h] [-H HOST] [-p PORT] [-k KEY | --key-file KEY_FILE] [-d DIR]

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Host name to listen on, default: 0.0.0.0
  -p PORT, --port PORT  Port to listen on, default: 8182
  -k KEY, --key KEY     Authentication key, default: empty
  --key-file KEY_FILE   Authentication key file. Key will be derived from its hash.
  -d DIR, --dir DIR     Working directory, default: current dir
```

### Client

```
scriptc [-h] [-H HOST] [-p PORT] [-k KEY | --key-file KEY_FILE] command

positional arguments:
  command               Name of the script to run on server

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  Server ip or name, default: 127.0.0.1
  -p PORT, --port PORT  Server port, default: 8182
  -k KEY, --key KEY     Authentication key, default: empty
  --key-file KEY_FILE   Authentication key file. Key will be derived from its hash.
```

### Example usage

On your server, put your scripts in a directory named `~/scriptd_home`. It is strongly advised that you keep this directory and any file under it accessable only to yourself.

Prepare an arbitrary-sized key-file that acts as the secret key. Name it `~/scriptd_home/key` and put it on both client and server.

Run `scriptd --key-file ~/scriptd_home/key -d ~/scriptd_home` to start the server.

You can now invoke scripts in `scriptd_home` remotely from clients with:

```scriptc -H <your-server> --key-file <key-file-path> <script-name>```

 Scripts will be invoked from `~/scriptd_home` on your server. Both stdout and stderr of the invoked script will be sent to your client encrypted.

### Installation

To install scriptd simply run:

```bash
pip install -U scriptd 
```

To install to a Unix global python environment use 

```bash
sudo -H pip install -U scriptd
```
