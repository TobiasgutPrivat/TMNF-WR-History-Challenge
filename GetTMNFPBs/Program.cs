using GBX.NET;
using GBX.NET.Engines.Game;
using GBX.NET.LZO;
using GBX.NET.ZLib;
using System.Text.Json;

string AutosavesFolder = "C:/Users/Tobias/Documents/TrackMania/Tracks/Replays/Autosaves/";

Dictionary<string, int> PBs = [];

foreach (string replayFile in Directory.GetFiles(AutosavesFolder, "*.Replay.gbx", SearchOption.TopDirectoryOnly)){
    Gbx.LZO = new MiniLZO();
    Gbx.ZLib = new ZLib();
    CGameCtnReplayRecord replay = Gbx.Parse<CGameCtnReplayRecord>(replayFile); 

    string replayName = Path.GetFileNameWithoutExtension(replayFile);
    string TrackName = replayName.Split(['_', '.'])[1];
    int TotalMilliseconds = replay.Time?.TotalMilliseconds ?? 0;
    PBs.Add(TrackName, TotalMilliseconds);
}

string json = JsonSerializer.Serialize(PBs);
File.WriteAllText("PBs.json", json);
