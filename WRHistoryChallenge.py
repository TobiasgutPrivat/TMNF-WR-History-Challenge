from createTMNFWRHistory import getTMNFTracks
from WRImprovement import WRImprovement, format_time
import json
import os
import subprocess

# Load configuration
with open(os.path.join(os.path.dirname(__file__), 'config.json')) as f:
    CONFIG = json.load(f)

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
        return (improvement.track_name, improvement.user_name, format_time(improvement.replay_time), format_time(self.currentPBs.get(improvement.track_name)))
    
    def GetNextUnbeatenWRImprovements(self) -> list[WRImprovement]:
        nextUnbeatenWRImprovements = []
        for i in range(self.selectedWRImprovementIndex + 1, len(self.WRImprovements)):
            improvement = self.WRImprovements[i]
            if self.currentPBs.get(improvement.track_name) is None or improvement.replay_time < self.currentPBs[improvement.track_name]:
                nextUnbeatenWRImprovements.append(improvement)
        return nextUnbeatenWRImprovements

    def LoadCurrentPBs(self):
        cmd = [os.path.join(os.path.dirname(__file__), CONFIG['paths']['cs_executable'])]
        cmd.append(CONFIG['paths']['replays_folder'])
            
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        self.currentPBs = json.loads(result.stdout)