Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "E:\start.bat" & Chr(34), 0
Set WshShell = Nothing
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "E:\target.bat" & Chr(34), 0
Set WshShell = Nothing