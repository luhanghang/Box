program Sdiapp;

uses
  Forms,
  SDIMAIN in 'SDIMAIN.pas' {SDIAppForm};

{$R *.RES}

begin
  Application.Initialize;
  Application.CreateForm(TSDIAppForm, SDIAppForm);
  Application.Run;
end.
 
