from WRHistoryChallenge import WRHistoryChallenge
import ttkbootstrap as ttk
from createTMNFWRHistory import GetTMNFWRHistory
from UI import WRHistoryChallengeUI
import pickle

if __name__ == "__main__":
    # with open('WRHistory.pkl', 'wb') as f:
    #     pickle.dump(GetTMNFWRHistory(),f)
    with open('WRHistory.pkl', 'rb') as f:
        WRImprovements = pickle.loads(f.read())

    root = ttk.Window()
    WRHistoryChallengeUI(root, WRHistoryChallenge(WRImprovements))

    root.mainloop()