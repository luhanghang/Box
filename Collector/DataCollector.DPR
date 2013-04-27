program DataCollector;

uses
  Forms,
  SDIMAIN in 'SDIMAIN.PAS' {MainFrame},
  FTPClient in 'FTPClient.pas',
  DataPoint in 'DataPoint.pas' {Frame1: TFrame};

{$R *.RES}

begin
  Application.Initialize;
  Application.CreateForm(TMainFrame, MainFrame);
  Application.Run;
end.
 
