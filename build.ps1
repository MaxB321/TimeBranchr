$APP_NAME = "TimeBranchr"
$MAIN_SCRIPT = "main.py"
$ICON = ""

# .qss and .ui files
$dataArgs = @()

Get-ChildItem -Recurse -Include "*.qss" | ForEach-Object {
    $rel = $_.DirectoryName | Resolve-Path -Relative
    $dataArgs += "--add-data `"$($_.FullName);$rel`""
}

Get-ChildItem -Recurse -Include "*.ui" | ForEach-Object {
    $rel = $_.DirectoryName | Resolve-Path -Relative
    $dataArgs += "--add-data `"$($_.FullName);$rel`""
}

$iconArg = if ($ICON -ne "") { "--icon `"$ICON`"" } else { "" }

$cmd = "pyinstaller " +
    "--onefile " +
    "--windowed " +
    "--name `"$APP_NAME`" " +
    "--collect-all PySide6 " +
    ($dataArgs -join " ") + " " +
    $iconArg + " " +
    "`"$MAIN_SCRIPT`""

Invoke-Expression $cmd