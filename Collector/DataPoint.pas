unit DataPoint;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, ExtCtrls, StdCtrls, msxml, DB, ADODB, StrUtils, FTPClient;

type
  TDataPoint = class(TFrame)
    ListBox1: TListBox;
    ADOQuery1: TADOQuery;
    ADOConnection1: TADOConnection;
    Timer1: TTimer;
    Panel1: TPanel;
    Button1: TButton;
    ADOQuery2: TADOQuery;
    Label1: TLabel;
    procedure log(str:String);
    procedure fetchData(lastRecord:String);
    procedure Timer1Timer(Sender: TObject);
    procedure connectDB;
    procedure Init;
    procedure InitDB;
    procedure InitFTP;
    procedure GetFile(path:String;fileName:String);
    function TestConnection:Boolean;
    procedure Button1Click(Sender: TObject);
    function WriteRecord:Boolean;
  private
    { Private declarations }
    FConfig:IXMLDOMNode;
    inited:Boolean;
//    dbInited:Boolean;
//    ftpInited:Boolean;
    fc: TFTPClient;
    fileRoot: String;
  public
    { Public declarations }
    procedure Start;
    procedure Stop;
    property Config:IXMLDOMNode
    read FConfig write FConfig;
  end;

var
  tableInf: IXMLDOMNode;
  fieldsInf: IXMLDOMNodeList;
  keyField: String;
  ftpField: String;
  limit: String;
  interval: String;
  ftp: String;

implementation
{$R *.dfm}
uses SDIMAIN;

procedure TDataPoint.Init;
begin
  tableInf := config.selectSingleNode('Table');
  fieldsInf := tableInf.selectNodes('Field');
  ftp := config.attributes.getNamedItem('ftp').text;
  keyField := tableInf.attributes.getNamedItem('keyField').text;
  ftpField := tableInf.attributes.getNamedItem('ftpField').text;
  limit := tableInf.attributes.getNamedItem('limit').text;
  interval := tableInf.attributes.getNamedItem('interval').text;
  InitDB;
  if ftp = 'true' then
    InitFTP;

  Timer1.Interval := StrToInt(interval) * 1000;
  inited := True;
end;

procedure TDataPoint.InitDB;
var
  dbInfo:IXMLDOMNode;
begin
  dbInfo := Config.selectSingleNode('dbserver');
  ADOConnection1.ConnectionString := 'Provider=MSDASQL.1;Persist Security Info=True;'
    + 'Data Source=' + dbInfo.selectSingleNode('dsname').text + ';'
    + 'User ID=' + dbInfo.selectSingleNode('username').text + ';'
    + 'Password=' +  dbInfo.selectSingleNode('passwd').text+ ';QTO=F';
//  dbInited := True;
end;

procedure TDataPoint.Button1Click(Sender: TObject);
begin
  if Button1.Caption = '开始' then
    Start
  else
    Stop;
end;

procedure TDataPoint.connectDB;
begin
  Timer1.Enabled := False;
  log('正在连接' + config.selectSingleNode('name').text + '数据库');
  try
    ADOConnection1.Connected := True;
    ADOConnection1.KeepConnection := True;
    Timer1.Enabled := True;
    log('成功连接数据库，开始读取数据...');
  Except
    on E:Exception do
    begin
      log('无法连接数据库:' + E.Message);
      Stop;
    end;
  end;
end;

function TDataPoint.TestConnection;
begin
  result := False;
  if Not inited then
    Init;
  log('测试' + config.selectSingleNode('name').text + 'FTP服务连接');
  if fc.Connect then
  begin
    fc.Disconnect;
    log('FTP服务连接成功');
  end
  else
  begin
    log('无法连接FTP服务');
    Exit;
  end;
  log('测试' + config.selectSingleNode('name').text + '数据库连接');
  try
    ADOConnection1.Connected := True;
    ADOConnection1.KeepConnection := True;
    log('数据库连接成功');
    result := True;
    Button1.Enabled := True;
  Except
    on E:Exception do
      log('无法连接数据库:' + E.Message);
  end;
end;

procedure TDataPoint.Start;
begin
  if Not inited then
    Init;
  ADOQuery2.Connection := MainFrame.ADOConnection1;
  Timer1.Enabled := True;
  Button1.Caption := '停止';
end;

procedure TDataPoint.Stop;
begin
  Timer1.Enabled := False;
  ADOConnection1.Connected := False;
  Button1.Caption := '开始';
end;

procedure TDataPoint.Timer1Timer(Sender: TObject);
begin
  if ADOConnection1.Connected then
    fetchData(config.attributes.getNamedItem('lastRecord').text)
  else
    ConnectDB();
end;

procedure TDataPoint.fetchData(lastRecord: string);
var
  ftpInf: String;
  fromNum: String;
  tableName :String;
  path: TStringList;
  pathStr: String;
  I:Integer;
begin
  Timer1.Enabled := false;
  tableName := tableInf.attributes.getNamedItem('from').text;
  fromNum := '0';
  if Trim(lastRecord) <> '' then
  begin
    ADOQuery1.SQL.Text := 'select * from (select rownum as rn,' + keyField + ',' + ftpField + ' from ' + tableName +
      ') where ' + keyField + ' = ''' + lastRecord + '''';
    ADOQuery1.Open;
    if not ADOQuery1.Eof then
    begin
      ADOQuery1.First;
      fromNum := ADOQuery1.FieldByName('rn').Text;
    end;
    ADOQuery1.Close;
  end;
  ADOQuery1.SQL.Text := 'select * from (select rownum as rn, a.* from ' + tableName + ' a where rownum <= ' + IntToStr(StrToInt(fromNum) + StrToInt(limit)) + ') where rn > ' + fromNum;
  ADOQuery1.Open;

  path := TStringList.Create;
  path.Delimiter := '/';
  pathStr := '';
  if Not ADOQuery1.Eof then
  begin
    log('本次将从第' + fromNum + '条记录开始读取' + IntToStr(ADOQuery1.RecordCount) + '条记录');
    log('正在连接' + config.selectSingleNode('name').text + 'FTP服务');
    if fc.Connect then
    begin
      log('成功连接FTP服务');
      ADOQuery1.First;
      while Not ADOQuery1.Eof do
      begin
        ftpInf := ADOQuery1.FieldByName(ftpField).Text;
        ftpInf := StringReplace(ftpInf,'\','/',[rfReplaceAll]);
        ftpInf := StringReplace(ftpInf,'//','/',[rfReplaceAll]);
        path.DelimitedText := ftpInf;

        for I := 2 to path.Count - 3 do
        begin
          pathStr := pathStr + path.Strings[I] + '/';
        end;

        pathStr := pathStr + path.Strings[path.Count - 2];

        if WriteRecord then
          begin
            GetFile(pathStr, path.Strings[path.Count - 1])
          end;
        //log(path.Strings[3] + '/' + path.Strings[4] + '*' + path.Strings[5]);
        config.attributes.getNamedItem('lastRecord').text := ADOQuery1.FieldByName(keyField).Text;
        ADOQuery1.Next;
      end;
      log('本次数据读取完成');
      fc.Disconnect;
      Timer1.Enabled := True;
    end
    else
    begin
      log('无法连接FTP服务:' + fc.Host + ':' + IntToStr(fc.Port));
      Stop;
    end;
  end
  else
  begin
    log('没有发现新数据');
    Timer1.Enabled := True;
  end;
  ADOQuery1.Close;
end;

procedure TDataPoint.InitFTP;
var
  ftpInf: IXMLDOMNode;
begin
  ftpInf := config.selectSingleNode('ftpserver');
  fc := TFTPClient.Create;
  fc.Host := ftpInf.selectSingleNode('address').text;
  fc.Port := StrToInt(ftpInf.selectSingleNode('port').text);
  fc.UserName := ftpInf.selectSingleNode('username').text;
  fc.Password := ftpInf.selectSingleNode('passwd').text;
  fileRoot := SDIMAIN.localInf.selectSingleNode('fileroot').text;
//  ftpInited := True;
end;

procedure TDataPoint.GetFile(path:String;fileName: string);
begin
  //if
  fc.DownloadFile(PChar(path + '/' + fileName),PChar(fileRoot + '/' + path + '/' + fileName));
  // then
    //log('成功下载文件' + fileName)
  //else
    //log('无法下载文件' + fileName);
end;

procedure TDataPoint.log(str: string);
begin
  if ListBox1.Items.Count = SDIMAIN.maxLog then
    ListBox1.Items.Clear;
  ListBox1.Items.Add(FormatDateTime('yyyy.mm.dd hh:mm:ss  ', now()) + str);
  ListBox1.Selected[ListBox1.Items.Count - 1] := true;
end;

function TDataPoint.WriteRecord;
var
  I:Integer;
  sql, fieldName, valueText:String;
  blobField:String;
  stream: TMemoryStream;
begin
  if Not ADOQuery2.Connection.Connected then
  begin
    try
      ADOQuery2.Connection.Connected := True;
    except
      on E:Exception do
      begin
        log('本地数据库连接失败');
        result := False;
        Exit;
      end;
    end;
  end;
  ADOQuery2.SQL.Clear;

  ADOQuery2.SQL.Text := 'select ' + keyfield + ' from ' + tableInf.attributes.getNamedItem('to').text + ' where ' + keyfield + '=''' + ADOQuery1.FieldByName(keyField).Text + '''';
  ADOQuery2.Open;
  if not ADOQuery2.Eof then
  begin
    ADOQuery2.Close;
    ADOQuery2.SQL.Clear;
    Result := False;
  end
  else
  begin
    ADOQuery2.Close;
    ADOQuery2.SQL.Clear;
    sql := 'insert into ' + tableInf.attributes.getNamedItem('to').text + ' (';
  for I := 0 to fieldsInf.length - 2 do
  begin
    sql := sql + fieldsInf.item[I].attributes.getNamedItem('to').text + ',';
  end;
  sql := sql + fieldsInf.item[I].attributes.getNamedItem('to').text + ')';
  sql := sql + ' values (';
  for I := 0 to fieldsInf.length - 1 do
  begin
    fieldName := fieldsInf.item[I].attributes.getNamedItem('from').text;
    case MainFrame.DataType(fieldsInf.item[I].attributes.getNamedItem('type').text) of
    0:
    begin
      if fieldsInf.item[I].attributes.getNamedItem('value') = Nil then
      begin
        if ADOQuery1.FieldByName(fieldName).Text = '' then
        begin
          valueText := 'null';
        end
        else
        begin
          valueText := ADOQuery1.FieldByName(fieldName).Text;
        end;
      end
      else
      begin
        valueText := fieldsInf.item[I].attributes.getNamedItem('value').text;
      end;
    end;
    1:
    begin
      valueText := 'TO_DATE(''' + ADOQuery1.FieldByName(fieldName).Text + ''', ''YYYY/MM/DD HH24:MI:SS'')';
    end;
    2:
    begin
      valueText := ':blob';
      blobField := fieldName;
    end;
    else
    begin
      valueText := ':' + fieldName;
    end;
    end;
    sql := sql + valueText + ',';
  end;

  sql := LeftStr(sql, length(sql) - 1);
  Sql := sql + ')';

  ADOQuery2.SQL.Add(sql);
  Adoquery2.Prepared := true;

  for I := 0 to fieldsInf.length - 1 do
  begin
    if MainFrame.DataType(fieldsInf.item[I].attributes.getNamedItem('type').text) = -1 then
    begin
      if fieldsInf.item[I].attributes.getNamedItem('value') = Nil then
        ADOQuery2.Parameters.ParamByName(fieldsInf.item[I].attributes.getNamedItem('to').text).Value := ADOQuery1.FieldByName(fieldsInf.item[I].attributes.getNamedItem('from').text).Text
      else
        ADOQuery2.Parameters.ParamByName(fieldsInf.item[I].attributes.getNamedItem('to').text).Value := fieldsInf.item[I].attributes.getNamedItem('value').text;
    end;
  end;
  stream := TMemoryStream.Create;
  TBlobField(ADOQuery1.FieldByName(blobField)).SaveToStream(stream);
  ADOQuery2.Parameters.ParamByName('blob').LoadFromStream(stream, ftBlob);
  stream.Free;
  try
    ADOQuery2.ExecSQL;
    Result := True;
  except
    on E:Exception do
    begin
      log('数据写入失败:' + E.Message);
      Result := False;
      //Stop;
    end;
    end;
  end;
end;

end.
