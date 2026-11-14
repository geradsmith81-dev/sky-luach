# Creates "Sky Luach.lnk" on the Desktop and in the Start menu.
$here = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$ws = New-Object -ComObject WScript.Shell
$targets = @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))
$old = @()   # earlier shortcut names to remove (none yet)
foreach ($dir in $targets) {
    foreach ($o in $old) { $p = Join-Path $dir $o; if (Test-Path $p) { Remove-Item $p } }
    $s = $ws.CreateShortcut((Join-Path $dir 'Sky Luach.lnk'))
    $s.TargetPath = $env:ComSpec
    $s.Arguments = '/c "' + (Join-Path $here 'Start app.bat') + '"'
    $s.WorkingDirectory = $here
    $s.IconLocation = (Join-Path $here 'assets\luach_icon.ico')
    $s.WindowStyle = 7
    $s.Save()
}
