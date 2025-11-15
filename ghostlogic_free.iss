[Setup]
AppName=GhostLogic Free
AppVersion=1.0.0
AppPublisher=GhostLogic
AppPublisherURL=https://ghostlogic.ai
DefaultDirName={pf}\GhostLogic Free
DefaultGroupName=GhostLogic Free
OutputDir=.
OutputBaseFilename=GhostLogic-Free-Installer
Compression=lzma
SolidCompression=yes
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\icon.ico

[Files]
Source: "dist\ghostlogic_free.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\dashboard.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\watchdog.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "utils.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "process_snapshot.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "upload_r2.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "upload_kv.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "events.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "agent.py"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\watch"

[Icons]
Name: "{group}\GhostLogic Free Agent"; Filename: "{app}\ghostlogic_free.exe"
Name: "{group}\GhostLogic Dashboard"; Filename: "{app}\dashboard.exe"
Name: "{group}\GhostLogic Watchdog"; Filename: "{app}\watchdog.exe"
Name: "{group}\Uninstall GhostLogic Free"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\watch\testfile.txt"; Flags: shellexec skipifdoesntexist postinstall skipifsilent; Description: "View test file"

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  TestFilePath: String;
begin
  if CurStep = ssPostInstall then
  begin
    TestFilePath := ExpandConstant('{app}\watch\testfile.txt');
    SaveStringToFile(TestFilePath, 'GhostLogic Free Edition - Test File' + #13#10, False);
  end;
end;
