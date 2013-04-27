object DataPoint: TDataPoint
  Left = 0
  Top = 0
  Width = 320
  Height = 240
  TabOrder = 0
  object ListBox1: TListBox
    Left = 0
    Top = 0
    Width = 320
    Height = 215
    Align = alClient
    BevelInner = bvNone
    BevelOuter = bvNone
    Color = clNone
    Font.Charset = DEFAULT_CHARSET
    Font.Color = clLime
    Font.Height = -13
    Font.Name = #23435#20307
    Font.Style = []
    ItemHeight = 13
    ParentFont = False
    TabOrder = 0
  end
  object Panel1: TPanel
    Left = 0
    Top = 215
    Width = 320
    Height = 25
    Cursor = crDrag
    Align = alBottom
    BevelOuter = bvNone
    Ctl3D = False
    ParentCtl3D = False
    TabOrder = 1
    object Label1: TLabel
      AlignWithMargins = True
      Left = 308
      Top = 6
      Width = 7
      Height = 16
      Margins.Top = 6
      Margins.Right = 5
      Align = alRight
      Font.Charset = DEFAULT_CHARSET
      Font.Color = clWindowText
      Font.Height = -13
      Font.Name = #23435#20307
      Font.Style = []
      ParentFont = False
      ExplicitHeight = 13
    end
    object Button1: TButton
      Left = 0
      Top = 6
      Width = 75
      Height = 25
      Caption = #24320#22987
      TabOrder = 0
      OnClick = Button1Click
    end
  end
  object ADOQuery1: TADOQuery
    Connection = ADOConnection1
    Parameters = <>
    Left = 8
    Top = 96
  end
  object ADOConnection1: TADOConnection
    Provider = 'MSDASQL.1'
    Left = 40
    Top = 96
  end
  object Timer1: TTimer
    Enabled = False
    OnTimer = Timer1Timer
    Left = 16
    Top = 16
  end
  object ADOQuery2: TADOQuery
    Parameters = <>
    Left = 8
    Top = 136
  end
end
