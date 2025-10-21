; Google Maps Scraper Desktop App - Inno Setup Script
; This script creates a Windows installer for the application

#define MyAppName "Google Maps Scraper"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Google Maps Scraper Team"
#define MyAppURL "https://github.com/yourusername/google-maps-scraper-app"
#define MyAppExeName "GoogleMapsScraper.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
InfoBeforeFile=README.md
OutputDir=installer
OutputBaseFilename=GoogleMapsScraper_Setup_v{#MyAppVersion}
SetupIconFile=resources\icons\app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
MinVersion=6.1sp1
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "vietnamese"; MessagesFile: "compiler:Languages\Vietnamese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\logs"
Type: filesandordirs; Name: "{app}\cache"
Type: files; Name: "{app}\config.ini"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // Check if .NET Framework is installed (if needed)
  // if not IsDotNetDetected('v4.0', 0) then begin
  //   MsgBox('This application requires .NET Framework 4.0 or higher.', mbError, MB_OK);
  //   Result := False;
  // end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  
  // Ask user if they want to keep their data
  if MsgBox('Do you want to keep your configuration and data files?', mbConfirmation, MB_YESNO) = IDNO then begin
    // Remove additional files
    DelTree(ExpandConstant('{app}\logs'), True, True, True);
    DelTree(ExpandConstant('{app}\cache'), True, True, True);
    DeleteFile(ExpandConstant('{app}\config.ini'));
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then begin
    // Create necessary directories
    ForceDirectories(ExpandConstant('{app}\logs'));
    ForceDirectories(ExpandConstant('{app}\cache'));
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  Result := False;
  
  // Skip license page if license file doesn't exist
  if PageID = wpLicense then
    Result := not FileExists(ExpandConstant('{src}\LICENSE'));
    
  // Skip info page if info file doesn't exist  
  if PageID = wpInfoBefore then
    Result := not FileExists(ExpandConstant('{src}\README.md'));
end;
