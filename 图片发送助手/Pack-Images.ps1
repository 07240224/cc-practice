# Windows PowerShell 5.1, STA. Files stay on this computer; no network calls.
param([switch]$ChooseFiles)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$taskOutput = Join-Path $env:LOCALAPPDATA 'CodexImageSender\packages'
[IO.Directory]::CreateDirectory($taskOutput) | Out-Null
$taskArchives = [Collections.Generic.List[string]]::new()
$taskSources = [Collections.Generic.List[object]]::new()
try {
    if (-not $ChooseFiles -and [Windows.Forms.Clipboard]::ContainsImage()) {
        $taskImage = [Windows.Forms.Clipboard]::GetImage()
        try {
            $taskMemory = [IO.MemoryStream]::new()
            try {
                $taskImage.Save($taskMemory, [Drawing.Imaging.ImageFormat]::Png)
                $taskSources.Add(@{Name='clipboard.png';Bytes=$taskMemory.ToArray();Path=$null})
            } finally { $taskMemory.Dispose() }
        } finally { $taskImage.Dispose() }
    } else {
        $taskDialog = [Windows.Forms.OpenFileDialog]::new()
        try {
            $taskDialog.Title = 'Choose the original images to send as ZIP files'
            $taskDialog.Filter = 'Images|*.png;*.jpg;*.jpeg;*.webp;*.gif;*.bmp;*.tif;*.tiff|All files|*.*'
            $taskDialog.Multiselect = $true
            if ($taskDialog.ShowDialog() -ne [Windows.Forms.DialogResult]::OK) { exit 0 }
            foreach ($taskPath in $taskDialog.FileNames) {
                $taskInfo = [IO.FileInfo]::new($taskPath)
                $taskSources.Add(@{Name=$taskInfo.Name;Path=$taskInfo.FullName;Bytes=$null})
            }
        } finally { $taskDialog.Dispose() }
    }
    $taskLimit = 24MB
    $taskStamp = [DateTime]::Now.ToString('yyyyMMdd-HHmmss-fff')
    $taskArchive = $null
    $taskBytes = 0L
    $taskPart = 0
    $taskIndex = 0
    try {
        foreach ($taskSource in $taskSources) {
            $taskLength = if ($null -ne $taskSource.Bytes) { $taskSource.Bytes.LongLength } else { ([IO.FileInfo]::new($taskSource.Path)).Length }
            if ($taskLength + 4096 -gt $taskLimit) { throw 'One image exceeds 24 MiB. Use a smaller source file or a shared file link for this image.' }
            if ($null -eq $taskArchive -or $taskBytes + $taskLength + 4096 -gt $taskLimit) {
                if ($null -ne $taskArchive) { $taskArchive.Dispose(); $taskArchive=$null }
                $taskPart++
                $taskZipPath = Join-Path $taskOutput ('images-{0}-{1:D2}.zip' -f $taskStamp,$taskPart)
                $taskArchive = [IO.Compression.ZipFile]::Open($taskZipPath,[IO.Compression.ZipArchiveMode]::Create)
                $taskArchives.Add($taskZipPath)
                $taskBytes = 0L
            }
            $taskIndex++
            $taskEntryName = '{0:D3}-{1}' -f $taskIndex,[IO.Path]::GetFileName($taskSource.Name)
            if ($null -ne $taskSource.Bytes) {
                $taskEntry = $taskArchive.CreateEntry($taskEntryName,[IO.Compression.CompressionLevel]::NoCompression)
                $taskStream = $taskEntry.Open()
                try { $taskStream.Write($taskSource.Bytes,0,$taskSource.Bytes.Length) } finally { $taskStream.Dispose() }
            } else {
                [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($taskArchive,$taskSource.Path,$taskEntryName,[IO.Compression.CompressionLevel]::NoCompression) | Out-Null
            }
            $taskBytes += $taskLength + 4096
        }
    } finally { if ($null -ne $taskArchive) { $taskArchive.Dispose() } }
    $taskDrop = [Collections.Specialized.StringCollection]::new()
    foreach ($taskZipPath in $taskArchives) {
        $taskCheck = [IO.Compression.ZipFile]::OpenRead($taskZipPath)
        try { if ($taskCheck.Entries.Count -eq 0) { throw 'The generated ZIP is empty.' } } finally { $taskCheck.Dispose() }
        [void]$taskDrop.Add($taskZipPath)
    }
    [Windows.Forms.Clipboard]::SetFileDropList($taskDrop)
    Write-Host 'ZIP files created. Return to Codex and paste (Ctrl+V) to attach the ZIP files.'
    Write-Host 'If pasting files is not supported, attach the ZIP from this folder:'
    Write-Host $taskOutput
    foreach ($taskZipPath in $taskArchives) { Write-Host $taskZipPath }
    Read-Host 'Press Enter to close'
} catch {
    Write-Host ('Error: ' + $_.Exception.Message) -ForegroundColor Red
    Read-Host 'Press Enter to close'
    exit 1
}
