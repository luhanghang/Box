unit SDIMAIN;

interface

uses Windows, Classes, Graphics, Forms, Controls, Menus,
  Dialogs, StdCtrls, Buttons, ExtCtrls, ComCtrls, ImgList, StdActns,
  ActnList, ToolWin, DB, ADODB, DataPoint, msxml, SysUtils;

type
  TMainFrame = class(TForm)
    StatusBar: TStatusBar;
    Panel1: TPanel;
    Button1: TButton;
    Button3: TButton;
    PageControl1: TPageControl;
    Timer1: TTimer;
    ListBox1: TListBox;
    Panel2: TPanel;
    ADOConnection1: TADOConnection;
    Timer2: TTimer;
    Button2: TButton;
    procedure Button1Click(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure FormCloseQuery(Sender: TObject; var CanClose: Boolean);
    procedure Button3Click(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure SaveConfig;
    procedure Button2Click(Sender: TObject);
    procedure Timer2Timer(Sender: TObject);
  private
    { Private declarations }
    dbInited: Boolean;
    dbConnected: Boolean;
    procedure InitDB;
    //procedure ConnectToDB;
    function TestConnection:Boolean;
    procedure log(str:String);
  public
    { Public declarations }
    function DataType(t: string):Integer;
  end;

var
  MainFrame: TMainFrame;
  isRunning: Boolean;
  config:IXMLDOMDocument;
  dps: Array of TDataPoint;
  //tableInf: IXMLDOMNode;
  //fieldsInf: IXMLDOMNodeList;
  //keyField: String;
  //ftpField: String;
  //limit: String;
  //interval: String;
  miscConfig: IXMLDOMNode;
  localInf: IXMLDOMNode;
  maxLog: Integer;
  types: Array[0..2] Of String = ('number','date','blob');
  //curWin: Integer;

implementation

uses FTPClient;

{$R *.dfm}
var
  ts: Array of TTabSheet;
  ps: IXMLDOMNodeList;

procedure TMainFrame.Button1Click(Sender: TObject);
var
  I: Integer;
  canStart: Boolean;
begin
  canStart := True;
  isRunning:= not isRunning;
  if isRunning = True then
  begin
    (Sender as TButton).Caption := '全部停止';
    for I := 0 to High(dps) do
    begin
      if Not dps[I].TestConnection then
        canStart := False;
    end;
    if canStart then
    begin
      for I := 0 to High(dps) do
        dps[I].Start;
      Timer1.Enabled := True;
    end
    else
    begin
      (Sender as TButton).Caption := '全部开始';
      ShowMessage('测试未通过,不能全部开始');
    end;
  end
  else
  begin
    for I := 0 to length(dps) - 1 do
    begin
      dps[I].Stop;
    end;
    (Sender as TButton).Caption := '全部开始';
    Timer1.Enabled := False;
  end;
end;

procedure TMainFrame.Button2Click(Sender: TObject);
begin
  if Button2.Caption = '窗口轮询' then
  begin
    Button2.Caption := '停止轮询';
    Timer2.Enabled := True;
  end
  else
  begin
     Button2.Caption := '窗口轮询';
     Timer2.Enabled := False;
  end;
end;

procedure TMainFrame.Button3Click(Sender: TObject);
begin
  close;
end;

procedure TMainFrame.FormCloseQuery(Sender: TObject; var CanClose: Boolean);
var
  I:Integer;
begin
  if MessageBox(Handle,'确定要退出吗？','退出', MB_ICONQUESTION or MB_OKCANCEL) = IDOK then
  begin
    ADOConnection1.Connected := False;
    ADOConnection1.Free;
    Timer1.Enabled := False;
    Timer1.Free;
    Timer2.Free;
    if dps <> Nil then
    begin
      for I := 0 to length(dps) - 1 do
      begin
        if dps[I] <> Nil then
        begin
          dps[I].Stop;
          dps[I].Free;
        end;
      end;
    end;
    if dbConnected then
      SaveConfig();
    CanClose := true;
    Self.Hide;
  end
  else
  begin
    CanClose := false;
  end;
end;

procedure TMainFrame.FormCreate(Sender: TObject);
var
  I: Integer;
begin
  dbConnected := False;
  config := CoDOMDocument.Create;
  config.async := false;
  config.load(ExtractFilePath(paramStr(0)) + 'config.xml');
  localInf := config.selectSingleNode('/Config/Local/DataSource');

  miscConfig := config.selectSingleNode('/Config/Misc');
  maxLog := StrToInt(miscConfig.selectSingleNode('MaxLog').text);

  Timer2.Interval := StrToInt(miscConfig.selectSingleNode('Polling').text) * 1000;
  isRunning := False;

  ps := config.selectNodes('/Config/Remote/DataSource[@enabled="1"]');
  SetLength(dps,ps.length);
  SetLength(ts,ps.length);

  for I := 0 to ps.length - 1 do
  begin
    ts[I] := TTabSheet.Create(PageControl1);
    ts[I].PageControl := PageControl1;
    ts[I].Caption := ps.item[I].selectSingleNode('name').text;

    dps[I] := TDataPoint.Create(Nil);
    dps[I].Parent := ts[I];
    dps[I].Config := ps.item[I];
    dps[I].Align := alClient;
    dps[I].Label1.Caption := ts[I].Caption;
  end;
end;

procedure TMainFrame.Timer1Timer(Sender: TObject);
begin
  if dbConnected then
    SaveConfig()
  else
    dbConnected := TestConnection;
end;

procedure TMainFrame.Timer2Timer(Sender: TObject);
begin
  Pagecontrol1.SelectNextPage(True);
end;

procedure TMainFrame.SaveConfig;
begin
  Timer1.Enabled := False;
  Config.save(ExtractFilePath(paramStr(0)) + 'config.xml');
  Timer1.Enabled := True;
end;

procedure TMainFrame.InitDB;
var
  dbInfo:IXMLDOMNode;
begin
  dbInfo := localInf.selectSingleNode('dbserver');
  ADOConnection1.ConnectionString := 'Provider=MSDASQL.1;Persist Security Info=True;'
    + 'Data Source=' + dbInfo.selectSingleNode('dsname').text + ';'
    + 'User ID=' + dbInfo.selectSingleNode('username').text + ';'
    + 'Password=' +  dbInfo.selectSingleNode('passwd').text+ ';QTO=F';
  dbInited := True;
end;

//procedure TMainFrame.ConnectToDB;
//begin
//  if Not dbInited then
//    InitDB;
//  log('正在连接本地数据库');
//  try
//    ADOConnection1.Connected := True;
//    ADOConnection1.KeepConnection := True;
//    log('成功连接数据库，开始接收数据...');
//  Except
//    on E:Exception do
//    begin
//      log('无法连接数据库:' + E.Message);
//    end;
//  end;
//end;

function TMainFrame.TestConnection:Boolean;
begin
  result := False;
  if Not dbInited then
    InitDB;
  log('正在连接本地数据库');
  try
    ADOConnection1.Connected := True;
    ADOConnection1.KeepConnection := True;
    log('数据库连接成功');
    Button1.Enabled := True;
    Button2.Enabled := True;
    PageControl1.Enabled := True;
    Result := True;
  Except
    on E:Exception do
      log('无法连接数据库:' + E.Message);
  end;
end;

procedure TMainFrame.log(str: string);
begin
  if ListBox1.Items.Count = maxLog then
    ListBox1.Items.Clear;
  ListBox1.Items.Add(FormatDateTime('yyyy.mm.dd hh:mm:ss  ', now()) + str);
  ListBox1.Selected[ListBox1.Items.Count - 1] := true;
end;

function TMainFrame.DataType(t: string):Integer;
var
  I:Integer;
begin
  for I := 0 to length(types) - 1 do
  begin
    if CompareText(t, types[I]) = 0 then
    begin
      result := I;
      break;
    end;
    result := -1;
  end;
end;

end.
