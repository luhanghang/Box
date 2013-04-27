unit SDIMAIN;

interface

uses Windows, Classes, Graphics, Forms, Controls, Menus,
  Dialogs, StdCtrls, Buttons, ExtCtrls, ComCtrls, ImgList, StdActns,
  ActnList, ToolWin,SysUtils, DB, ADODB,msxml, StrUtils;

type
  TSDIAppForm = class(TForm)
    Button1: TButton;
    Timer1: TTimer;
    ListBox1: TListBox;
    ADOConnection1: TADOConnection;
    ADOQuery1: TADOQuery;
    ADOQuery2: TADOQuery;
    procedure FileNew1Execute(Sender: TObject);
    procedure Timer1Timer(Sender: TObject);
    procedure FormCreate(Sender: TObject);
    procedure Button1Click(Sender: TObject);
    procedure FormCloseQuery(Sender: TObject; var CanClose: Boolean);
    function DataType(t:String):Integer;
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  SDIAppForm: TSDIAppForm;

implementation

uses about;
{$R *.dfm}

var
  config:IXMLDOMDocument;
  fields: IXMLDOMNodeList;
  lastRecord:Integer;
  types: Array[0..2] Of String = ('number','date','blob');

procedure TSDIAppForm.Button1Click(Sender: TObject);
begin
  Self.ListBox1.Items.Append('正在连接数据库...');
  Self.ADOConnection1.Connected := true;
  Self.ListBox1.Items.Append('数据库连接已建立');
  Self.Timer1.Enabled := true;
end;

procedure TSDIAppForm.FileNew1Execute(Sender: TObject);
begin
  { Do nothing }
end;

procedure TSDIAppForm.FormCreate(Sender: TObject);
begin
  config := CoDOMDocument.Create;
  config.async := false;
  config.load('../config.xml');
  fields := config.selectNodes('/Config/Table/Field');
  lastRecord := 0;
end;

procedure TSDIAppForm.Timer1Timer(Sender: TObject);
var
  I:Integer;
  sql, fieldName, valueText:String;
  blobField:String;
  stream: TMemoryStream;
  f: TextFile;
begin
  AssignFile(f, 'd:\log.txt');
  blobField := '';
  if ListBox1.Items.Count - 1 > 100 then
  begin
    ListBox1.Items.Clear;
  end;
  ADOQuery1.SQL.Clear;
  Self.ADOQuery1.SQL.Text := 'select * from (select rownum rn, a.* from (select * from cltxb_hw_source) a where rownum <= ' + IntToStr(lastRecord + 10) + ') where rn > ' + IntToStr(lastRecord);
  //Self.ADOQuery1.Active := true;
  ADOQuery1.Open;
  Self.ListBox1.Items.Append('------------------------------------------------------');
  Self.ListBox1.Items.Append(FormatDateTime('yyyy.mm.dd hh:mm:ss', now()) + ': ' + Self.ADOQuery1.SQL.Text);
  Timer1.Enabled := false;
  while not ADOQuery1.Eof do
  begin
    ADOQuery2.SQL.Clear;

    sql := 'insert into cltxb_hw (';
    for I := 0 to fields.length - 2 do
    begin
      sql := sql + fields.item[I].attributes.getNamedItem('to').text + ',';
    end;
    sql := sql + fields.item[I].attributes.getNamedItem('to').text + ')';
    sql := sql + ' values (';
    for I := 0 to fields.length - 1 do
    begin
      fieldName := fields.item[I].attributes.getNamedItem('from').text;
      case DataType(fields.item[I].attributes.getNamedItem('type').text) of
      0:
      begin
        if ADOQuery1.FieldByName(fieldName).Text = '' then
        begin
          valueText := 'null,';
        end
        else
        begin
          valueText := ADOQuery1.FieldByName(fieldName).Text + ',';
        end;
      end;
      1:
      begin
        valueText := 'TO_DATE(''' + ADOQuery1.FieldByName(fieldName).Text + ''', ''YYYY/MM/DD HH24:MI:SS''),';
      end;
      2:
      begin
        valueText := ':blob,';
        blobField := fieldName;
      end;
      else
      begin
        valueText := ':' + fieldName + ',';
      end;
      end;
      sql := sql + valueText;
    end;
    sql := LeftStr(sql, length(sql) - 1);
    Sql := sql + ')';
    ADOQuery2.SQL.Add(sql);

    rewrite(f);
    writeln(f, sql);
    closefile(f);
    adoquery2.Prepared := true;

    Self.ListBox1.Items.Append(ADOQuery1.FieldByName('rn').Text);
    lastRecord := StrToInt(ADOQuery1.FieldByName('rn').Text);

   //showmessage(sql + '-' + IntToStr(adoquery2.Parameters.Count));

   for I := 0 to fields.length - 1 do
    begin
      if DataType(fields.item[I].attributes.getNamedItem('type').text) = -1 then
      begin
      //showmessage(fields.item[I].attributes.getNamedItem('to').text);
        ADOQuery2.Parameters.ParamByName(fields.item[I].attributes.getNamedItem('to').text).Value := ADOQuery1.FieldByName(fields.item[I].attributes.getNamedItem('from').text).Text;
      end;
    end;


    stream := TMemoryStream.Create;
    TBlobField(ADOQuery1.FieldByName(blobField)).SaveToStream(stream);
    ADOQuery2.Parameters.ParamByName('blob').LoadFromStream(stream, ftBlob);
    stream.Free;
    ADOQuery2.ExecSQL;

    Self.ADOQuery1.Next;
  end;
  Self.ListBox1.Selected[Self.ListBox1.Items.Count - 1] := true;
  //Timer1.Enabled := true;
end;

procedure TSDIAppForm.FormCloseQuery(Sender: TObject; var CanClose: Boolean);
begin
  if MessageBox(Handle,'确实要退出吗？','退出', MB_ICONQUESTION or MB_OKCANCEL) = IDOK then
  begin
    Self.Timer1.Enabled := false;
    Self.Timer1.Free;
    Self.ADOQuery1.Active := false;
    Self.ADOQuery1.Free;
    Self.ADOQuery2.Free;
    Self.ADOConnection1.Connected := false;
    Self.ADOConnection1.Free;
    CanClose := true;
    Self.Hide;
  end
  else
  begin
    CanClose := false;
  end;
end;

function TSDIAppForm.DataType(t: string):Integer;
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
