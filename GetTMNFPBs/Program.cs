using GBX.NET;
using GBX.NET.Engines.Game;
using GBX.NET.LZO;
using GBX.NET.ZLib;
using System.Text.Json;

// Get folder path from command line argument or use default
string autosavesFolder = args.Length > 0 
    ? args[0] 
    : throw new ArgumentException("Usage: GetTMNFPBs.exe <autosaves_folder>");

if (!Directory.Exists(autosavesFolder))
{
    throw new ArgumentException($"Folder {autosavesFolder} does not exist");
}

Dictionary<string, int> pbs = [];

foreach (string replayFile in Directory.GetFiles(autosavesFolder, "*.Replay.gbx", SearchOption.TopDirectoryOnly))
{
    try
    {
        Gbx.LZO = new MiniLZO();
        Gbx.ZLib = new ZLib();
        CGameCtnReplayRecord replay = Gbx.Parse<CGameCtnReplayRecord>(replayFile); 

        string replayName = Path.GetFileNameWithoutExtension(replayFile);
        string trackName = replayName.Split(['_', '.'])[1];
        int totalMilliseconds = replay.Time?.TotalMilliseconds ?? 0;
        
        // Only add if we got a valid time
        if (totalMilliseconds > 0)
        {
            pbs[trackName] = totalMilliseconds;
        }
    }
    catch (Exception ex)
    {
        Console.Error.WriteLine($"Warning: Failed to process replay file {replayFile}: {ex.Message}");
        continue;
    }
}

// Output JSON to stdout for Python to capture
var options = new JsonSerializerOptions { WriteIndented = true };
Console.WriteLine(JsonSerializer.Serialize(pbs, options));
