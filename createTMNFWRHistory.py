import requests
from datetime import datetime
from functools import lru_cache
import pickle
from WRImprovement import WRImprovement

WRHistoryFolder = "C:/Users/Tobias/Documents/TrackMania/Tracks/Replays/WRHistory/"

@lru_cache(maxsize=0)
def getMapReplays(mapID: str, afterID: str = None) -> list:
    url = "https://tmnf.exchange/api/replays"
    params = {
        "fields": "ReplayId,ReplayTime,User.Name,ReplayAt",  # Select relevant fields
        "trackId": mapID,  # Replace with the actual track ID
        "count": 1000,
    }
    if afterID != None:
        params["after"] = afterID
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["Results"]
    else:
        raise Exception(f"Request failed with status code: {response.status_code}")

def getAllReplays(mapID: str) -> list:
    AllReplays = []
    results = getMapReplays(mapID)

    AllReplays.extend(results)
    while len(results) == 1000:
        afterID = results[-1]["ReplayId"]
        lastResult = results
        results = getMapReplays(mapID, afterID)
        if lastResult == results:
            break
        AllReplays.extend(results)

    return AllReplays

def createWRImprovement(data) -> WRImprovement:
    replay_at = datetime.fromisoformat(data["ReplayAt"])
    return WRImprovement(
        replay_id = data["ReplayId"],
        replay_time = data["ReplayTime"],
        user_name = data["User"]["Name"],
        replay_at = replay_at,
        track_name = data["TrackName"],
        ReplayPath = WRHistoryFolder + f"{data["TrackName"]}_{replay_at.strftime("%Y-%m-%d")}/"
    )

def getAllWRImprovements(mapID: str) -> list:
    AllImprovements = []
    replays = getAllReplays(mapID)
    print(len(replays))
    replays.sort(key=lambda x: x["ReplayAt"])
    WR = 999999999
    for replay in replays:
        if replay["ReplayTime"] < WR:
            WR = replay["ReplayTime"]
            AllImprovements.append(replay)
    return AllImprovements

def getTMNFTracks() -> list:
    url = "https://tmnf.exchange/api/tracks"
    params = {
        "fields": "TrackId,TrackName",  # Select relevant fields
        "author": "Nadeo",  # Replace with the actual track ID
        "count": 65,
        "after": "10369947" #last Beta Map ID 10369947
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        tracks = data["Results"]
    else:
        raise Exception(f"Request failed with status code: {response.status_code}")
    return tracks

def GetTMNFWRHistory() -> list:
    tracks = getTMNFTracks()
        
    AllWRImprovements = []
    for track in tracks:
        print(track["TrackName"])
        trackImprovements = getAllWRImprovements(track["TrackId"])
        for improvement in trackImprovements:
            improvement["TrackName"] = track["TrackName"]
        AllWRImprovements.extend(trackImprovements)
    AllWRImprovements.sort(key=lambda x: x["ReplayAt"])

    WRImprovements = []
    for entry in AllWRImprovements:
        WRImprovements.append(createWRImprovement(entry))

    return WRImprovements

def SaveWRHistoryAsJson() -> None:
    WRHistory = GetTMNFWRHistory()
    WRImprovements = []

    for entry in WRHistory:
        WRImprovements.append(createWRImprovement(entry))
    
    data = pickle.dumps(WRImprovements)

    with open("WRHistory.pkl", "wb") as file:
        file.write(data)