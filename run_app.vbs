Set objShell = CreateObject("WScript.Shell")

strCommand = "streamlit run main.py"
objShell.Run strCommand, 1, True

' Clean up the objects
Set objShell = Nothing
