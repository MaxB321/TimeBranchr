$APP_NAME = "TimeBranchr"
$MAIN_SCRIPT = "src\main.py"
$ICON = ""

# .qss and .ui files
$dataArgs = @()

Get-ChildItem -Recurse -Include "*.qss" | ForEach-Object {
    $rel = $_.DirectoryName | Resolve-Path -Relative
    $dest = $rel -replace '^\.\\src\\', ''
    $dataArgs += "--add-data `"$($_.FullName);$dest`""
}

Get-ChildItem -Recurse -Include "*.ui" | ForEach-Object {
    $rel = $_.DirectoryName | Resolve-Path -Relative
    $dest = $rel -replace '^\.\\src\\', ''
    $dataArgs += "--add-data `"$($_.FullName);$dest`""
}

# Exclude modules
$excludeArgs = @(
    "--exclude-module src.api",
    "--exclude-module src.api.*",
    "--exclude-module src.database.categories_table",
    "--exclude-module src.database.logs_table",
    "--exclude-module src.database.user_table"
)

$iconArg = if ($ICON -ne "") { "--icon `"$ICON`"" } else { "" }

$cmd = "pyinstaller " +
    "--onedir " +
    "--windowed " +
    "--name `"$APP_NAME`" " +
    "--collect-all PySide6 " +
    ($dataArgs -join " ") + " " +
    ($excludeArgs -join " ") + " " +
    $iconArg + " " +
    "`"$MAIN_SCRIPT`""

Invoke-Expression $cmd