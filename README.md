# Palworld no one pause
A simple script that pauses the Palworld server when no players are online.

***Time isn't passing in the world of Palserver.***

## Features
* Pauses the server when no players are online
* Checks for players on the server every minute
* Automatically restarts when all players have left

## Requirements
* python 3.7+
* <a href="https://npcap.com/#download" target="_blank">Npcap</a> (Windows users)
* tcpdump (Linux users)

## Usage
**This script requires administrator(root) privileges as it uses real-time sniffing to detect when players join the server.**

This script uses the Palserver RCON. Please set `RCONEnable=True` in the <a href="https://tech.palworldgame.com/settings-and-operation/configuration" target="_blank">Palserver configuration</a>.

Before running the script, make sure the settings are correctly saved in the config.ini file.

**config.ini**
- program_path: Enter the path to the Palserver.
- program_args: Execution arguments for the Palserver.
- ip: Server IP, usually 127.0.0.1
- port: Server Port, default 8211
- rcon_port: Rcon Port, default 25575
- rcon_pwd: Enter if you set an RCON password

**Windows users**
- After installing Npcap, restart your computer.
- Then, run start.bat to execute the script.

**Linux users**:
- Enter your root password in the root_pwd field under the Unix section of the config.ini file.
- Then, run start.sh to execute the script.

Or, you can run this script manually like:
```console
cd {script_directory}
pip install psutil scapy
python3 noone_pause.py
```

## Acknowledgement
<a href="https://github.com/thijsvanloef/palworld-server-docker/issues/32#issuecomment-1926103919" target="_blank">hoonlight's Palserver Docker pause script</a>
