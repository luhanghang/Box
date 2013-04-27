object SDIAppForm: TSDIAppForm
  Left = 197
  Top = 111
  Caption = 'SDI Application'
  ClientHeight = 429
  ClientWidth = 357
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -13
  Font.Name = 'System'
  Font.Style = []
  OldCreateOrder = False
  OnCloseQuery = FormCloseQuery
  OnCreate = FormCreate
  PixelsPerInch = 96
  TextHeight = 16
  object Button1: TButton
    Left = 0
    Top = 0
    Width = 357
    Height = 25
    Align = alTop
    Caption = #24320#22987
    TabOrder = 0
    OnClick = Button1Click
  end
  object ListBox1: TListBox
    Left = 0
    Top = 25
    Width = 357
    Height = 404
    Align = alClient
    ItemHeight = 16
    TabOrder = 1
  end
  object Timer1: TTimer
    Enabled = False
    Interval = 3000
    OnTimer = Timer1Timer
    Left = 504
  end
  object ADOConnection1: TADOConnection
    ConnectionString = 
      'Provider=MSDASQL.1;Password=hwits;Persist Security Info=True;Use' +
      'r ID=hwits;Data Source=test'
    Provider = 'MSDASQL.1'
    Left = 8
    Top = 32
  end
  object ADOQuery1: TADOQuery
    Connection = ADOConnection1
    Parameters = <>
    Left = 8
    Top = 96
  end
  object ADOQuery2: TADOQuery
    Connection = ADOConnection1
    Parameters = <>
    Left = 8
    Top = 64
  end
end
