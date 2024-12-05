from createTMNFWRHistory import getTMNFTracks
from WRImprovement import WRImprovement, formated_replay_time
import json
import subprocess

GETCURRENTPBSPATH = 'C:/Users/Tobias/Documents/Programmieren/TMNF WR History Challenge/GetTMNFPBs/bin/Debug/net8.0/win-x64/GetTMNFPBs.exe'

class WRHistoryChallenge:
    WRImprovements: list[WRImprovement]
    currentPBs: dict[str, int | None]
    selectedWRImprovementIndex: int = 0

    def __init__(self, WRImprovements: list[WRImprovement]):
        self.WRImprovements = WRImprovements
        self.LoadCurrentPBs()

    def selectNextUnbeatenWRImprovement(self) -> None:
        for i in range(self.selectedWRImprovementIndex + 1, len(self.WRImprovements)):
            improvement = self.WRImprovements[i]
            if self.currentPBs.get(improvement.track_name) is None or improvement.replay_time < self.currentPBs[improvement.track_name]:
                self.selectedWRImprovementIndex = self.WRImprovements.index(improvement)
                return
        print("No unbeaten WR Improvements found")
    
    def GetSkippedWRImprovements(self) -> list[WRImprovement]:
        skippedWRImprovements = []
        for i in range(self.selectedWRImprovementIndex):
            improvement = self.WRImprovements[i]
            if self.currentPBs.get(improvement.track_name) is None or improvement.replay_time < self.currentPBs[improvement.track_name]:
                skippedWRImprovements.append(improvement)
        return skippedWRImprovements
            
    def playSelectedWRImprovement(self) -> None:
        self.WRImprovements[self.selectedWRImprovementIndex].playAgainst()

    def getSelectedWRImprovementInfo(self) -> tuple[str, str, str, int | None]:
        improvement = self.WRImprovements[self.selectedWRImprovementIndex]
        return (improvement.track_name, improvement.user_name, formated_replay_time(improvement.replay_time), formated_replay_time(self.currentPBs.get(improvement.track_name)))
    
    def GetNextUnbeatenWRImprovements(self) -> list[WRImprovement]:
        nextUnbeatenWRImprovements = []
        for i in range(self.selectedWRImprovementIndex + 1, len(self.WRImprovements)):
            improvement = self.WRImprovements[i]
            if self.currentPBs.get(improvement.track_name) is None or improvement.replay_time < self.currentPBs[improvement.track_name]:
                nextUnbeatenWRImprovements.append(improvement)
        return nextUnbeatenWRImprovements

    def LoadCurrentPBs(self) -> dict[str, int | None]:
        subprocess.run([GETCURRENTPBSPATH], creationflags=subprocess.CREATE_NO_WINDOW)
        with open('PBs.json', 'r') as f:
            self.currentPBs = {trackName: pbTime if pbTime != 0 else None for trackName, pbTime in json.load(f).items()}
