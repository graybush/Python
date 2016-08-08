Set WshShell = CreateObject("WScript.Shell")
Return = WshShell.Run(chr(34) & "C:\Users\Owner\Documents\GitHub\Python\IP_address_lookup\currentIP.bat" & Chr(34), 0)
If Return <> 0 Then
  WScript.Echo "Description: " & Return.Description
End If
Set WshShell = Nothing