import json


def write(dt: dict):
    json_object = json.dumps(dt, indent=len(dt))
    with open("config.json", "w") as file:
        file.write(json_object)


def read():
    with open("config.json", "r") as file:
        loaded = json.load(file)
        return loaded


sizer = 3
testdict = {"hallo": 5,
            "world": 5,
            "sizer": sizer}

resetdict = {"sizer": 3,
             "framerate": 120,
             "highscore": 0
             }

if __name__ == "__main__":
    write(resetdict)

