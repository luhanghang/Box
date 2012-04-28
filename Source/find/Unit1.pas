unit Unit1;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Sockets, IdUDPServer, IdBaseComponent, IdComponent,
  IdUDPBase, IdUDPClient, IdSocketHandle, ScktComp;

type
  TForm1 = class(TForm)
    Memo1: TMemo;
    Button1: TButton;
    IdUDPClient1: TIdUDPClient;
    IdUDPServer1: TIdUDPServer;
    procedure Button1Click(Sender: TObject);
    procedure IdUDPServer1UDPRead(Sender: TObject; AData: TBytes;
      ABinding: TIdSocketHandle);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

{$R *.dfm}

procedure TForm1.Button1Click(Sender: TObject);
begin
  //IdUDPClient1.Active := True;
  IdUDPClient1.Broadcast('*find*',8812);
end;

procedure TForm1.IdUDPServer1UDPRead(Sender: TObject; AData: TBytes;
  ABinding: TIdSocketHandle);
begin
  Memo1.Lines.Append(ABinding.PeerIP);
end;

end.


