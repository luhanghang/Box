unit  FTPClient;
 
interface  
 
uses  
           Windows,  Messages,  Variants,SysUtils,  Classes,  Wininet,  Dialogs;  
 
type  
           TFTPClient  =  class(TObject)

           private
                       FInetHandle:  HInternet;  //  句柄  
                       FFtpHandle:  HInternet;  //  句柄  
 
                       FHost:  string;  //  主机IP地址  
                       FUserName:  string;  //  用户名  
                       FPassword:  string;  //  密码  
                       FPort:  integer;  //  端口  
 
                       FCurrentDir:  string;  //  当前目录  
 
           public  
                       constructor  Create;virtual;  
                       destructor  Destroy;override;  
 
                       function  Connect:  boolean;  
                       function  Disconnect:  boolean;  
 
                       function  UploadFile(RemoteFile:  PChar;  NewFile:  PChar):  boolean;  
                       function  DownloadFile(RemoteFile:  PChar;  NewFile:  PChar):  boolean;  
 
                       function  CreateDirectory(Directory:  PChar):  boolean;  
 
                       function  LayerNumber(dir:  string):  integer;  
                       function  MakeDirectory(dir:  string):  boolean;  
                       function  FTPMakeDirectory(dir:  string):  boolean;  
                       function  IndexOfLayer(index:  integer;  dir:  string):  string;  
                       function  GetFileName(FileName:  string):  string;  
                       function  GetDirectory(dir:  string):  string;  
 
                       property  InetHandle:  HInternet  read  FInetHandle  write  FInetHandle;  
                       property  FtpHandle:  HInternet  read  FFtpHandle  write  FFtpHandle;  
                       property  Host:  string  read  FHost  write  FHost;  
                       property  UserName:  string  read  FUserName  write  FUserName;  
                       property  Password:  string  read  FPassword  write  FPassword;  
                       property  Port:  integer  read  FPort  write  FPort;  
 
                       property  CurrentDir:  string  read  FCurrentDir  write  FCurrentDir;  
 
end;  
 
 
implementation  
 
//-------------------------------------------------------------------------  
//  构造函数  
constructor  TFTPClient.Create;
begin  
           inherited  Create;  
 
end;  
 
//-------------------------------------------------------------------------  
//  析构函数  
destructor  TFTPClient.Destroy;
begin  
 
           inherited  Destroy;  
end;  
 
//-------------------------------------------------------------------------  
//  链接服务器  
function  TFTPClient.Connect:  boolean;
begin  
           try  
                       Result  :=  false;  
                       //  创建句柄  
                       FInetHandle  :=  InternetOpen(PChar('KOLFTP'),  0,  nil,  nil,  0);  
                       FtpHandle  :=  InternetConnect(FInetHandle,  PChar(Host),  FPort,  PChar(FUserName),  
                                                                       PChar(FPassword),  INTERNET_SERVICE_FTP,  0,  255);  
                       if  Assigned(FtpHandle)  then  
                       begin  
                                   Result  :=  true;  
                       end;  
 
           except  
                       Result  :=  false;  
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  断开链接  
function  TFTPClient.Disconnect:  boolean;
begin  
           try  
                       InternetCloseHandle(FFtpHandle);  
                       InternetCloseHandle(FInetHandle);  
                       FtpHandle:=nil;  
                       inetHandle:=nil;  
 
                       Result  :=  true;  
           except  
                       Result  :=  false;  
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  上传文件  
function  TFTPClient.UploadFile(RemoteFile:  PChar;  NewFile:  PChar):  boolean;
begin  
           try  
                       Result  :=  true;  
                       FTPMakeDirectory(NewFile);  
                       if  not  FtpPutFile(FFtpHandle,  RemoteFile,  NewFile,  
                                                           FTP_TRANSFER_TYPE_BINARY,  255)  then  
                       begin  
                                   Result  :=  false;  
                       end;  
           except  
                       Result  :=  false;  
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  下载文件  
function  TFTPClient.DownloadFile(RemoteFile:  PChar;  NewFile:  PChar):  boolean;
begin  
           try  
                       Result  :=  true;
                       MakeDirectory(NewFile);
                       if  not  FtpGetFile(FFtpHandle,  RemoteFile,  NewFile,
                                                                                   True,  FILE_ATTRIBUTE_NORMAL,  FTP_TRANSFER_TYPE_BINARY  OR  INTERNET_FLAG_RELOAD,  255)  then
                       begin
                                   Result  :=  false;
                       end;
           except
                on E:Exception do
                begin
                       Result  :=  false;
                       showMessage(e.Message);
                end;
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  创建目录  
function  TFTPClient.CreateDirectory(Directory:  PChar):  boolean;
begin  
           try  
                       Result  :=  true;  
                       if  FtpCreateDirectory(FFtpHandle,  Directory)=false  then  
                       begin  
                                   Result  :=  false;  
                       end;  
           except  
                       Result  :=  false;  
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  目录数  
function  TFTPClient.LayerNumber(dir:  string):  integer;
var  
           i:  integer;  
           flag:  string;  
begin  
           Result  :=  0;  
 
           for  i:=1  to  Length(dir)  do  
           begin  
                       flag  :=  Copy(dir,i,1);  
                       if  (flag='\')  or  (flag='/')  then  
                       begin  
                                   Result  :=  Result  +  1;  
                       end;  
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  创建目录  
function  TFTPClient.FTPMakeDirectory(dir:  string):  boolean;
var  
           count,  i:  integer;  
           SubPath:  string;  
begin  
           Result  :=  true;  
           count  :=  LayerNumber(dir);  
 
           for  i:=1  to  count  do  
           begin  
                       SubPath  :=  IndexOfLayer(i,  dir);  
                       if  CreateDirectory(PChar(CurrentDir+SubPath))=false  then  
                       begin  
                                   Result  :=  false;  
                       end;  
           end;
end;

//-------------------------------------------------------------------------
//  创建目录
function  TFTPClient.MakeDirectory(dir:  string):  boolean;
var
           count,  i:  integer;
           SubPath:  string;
           str:  string;
begin
           Result  :=  true;
           count  :=  LayerNumber(dir);
           str  :=  GetDirectory(dir);

           for  i:=2  to  count  do
           begin
                       SubPath  :=  IndexOfLayer(i,  str);
                       if  not  DirectoryExists(SubPath)  then
                       begin
                                   if  not  CreateDir(SubPath)  then
                                   begin
                                               Result  :=  false;
                                   end;
                       end;
           end;
end;

//-------------------------------------------------------------------------
//  获取index层的目录
function  TFTPClient.IndexOfLayer(index:  integer;  dir:  string):  string;
var
           count,  i:  integer;  
           ch:  string;  
begin  
           Result  :=  '';  
           count  :=  0;  
           for  i:=1  to  Length(dir)  do  
           begin  
                       ch  :=  Copy(dir,  i,  1);  
                       if  (ch='\')  or  (ch='/')  then  
                       begin  
                                   count  :=  count+1;  
                       end;  
                       if  count=index  then  
                       begin  
                                   break;  
                       end;  
                       Result  :=  Result  +  ch;  
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  获取文件名
function  TFTPClient.GetFileName(FileName:  string):  string;
begin  
           Result  :=  '';  
           while  (Copy(FileName,  Length(FileName),  1)<>'\')  and  (Length(FileName)>0)  do  
           begin  
                       Result  :=  Copy(FileName,  Length(FileName),  1)+Result;  
                       Delete(FileName,  Length(FileName),  1);  
           end;  
end;  
 
//-------------------------------------------------------------------------  
//  获取目录  
function  TFTPClient.GetDirectory(dir:  string):  string;
begin  
           Result  :=  dir;  
           while  (Copy(Result,  Length(Result),  1)<>'/')  and  (Length(Result)>0)  do  
           begin  
                       Delete(Result,  Length(Result),  1);  
           end;  
 
{            if  Copy(Result,  Length),  1)='\'  then  
           begin  
                       Delete(Result,  1,  1);  
           end;}  
end;  
 
//-------------------------------------------------------------------------  
end.
