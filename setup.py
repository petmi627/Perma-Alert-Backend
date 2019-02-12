import os, sys, json

base = os.path.dirname(__file__)

print("Creating required directories in /data and /config")
def create_folders(folder):
    if not os.path.isdir(folder):
        os.mkdir(folder)

create_folders(os.path.join(base, 'config/secrets'))

print("Generating secret keys config file")
secret_keys = {
  "weather_api": "",
  "google_api": "",
  "google_maps_key": "",

  "instagram_api_user": {
    "username": "",
    "password": ""
  },

  "calendarId": ""
}
with open(os.path.join(base, 'config/secrets/secret_keys.json'), 'w') as outfile:
    json.dump(secret_keys, outfile)

print("Download missing dependencies")
os.system("pip install -r requirements.txt")
# Windows
if sys.platform == "win32" or sys.platform == "cygwin":
    print("please download the mysql client version needed from: "
          "https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient")
    print("->  Try installing it with: pip install mysqlclient‑1.4.1‑VERSION.whl")
# Linux & Mac OSx
else:
    print("please install the mysql client with: pip install mysqlclient")
    print("If the installation doesn't work, retry by installing mysql-client and libmysqlclient-dev with: "
          "sudo apt install mysql-client libmysqlclient-dev")

print("Done")