object Form1: TForm1
  Left = 0
  Top = 0
  Caption = 'Find Box'
  ClientHeight = 352
  ClientWidth = 265
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object Memo1: TMemo
    Left = 8
    Top = 8
    Width = 249
    Height = 305
    ReadOnly = True
    TabOrder = 0
  end
  object Button1: TButton
    Left = 96
    Top = 319
    Width = 75
    Height = 25
    Caption = #26597#25214
    TabOrder = 1
    OnClick = Button1Click
  end
  object IdUDPClient1: TIdUDPClient
    BroadcastEnabled = True
    Host = '224.0.0.0'
    Port = 8812
    Left = 80
    Top = 96
  end
  object IdUDPServer1: TIdUDPServer
    Active = True
    BroadcastEnabled = True
    Bindings = <
      item
        IP = '0.0.0.0'
        Port = 8712
      end>
    DefaultPort = 8712
    OnUDPRead = IdUDPServer1UDPRead
    ThreadedEvent = True
    Left = 120
    Top = 176
  end
end
