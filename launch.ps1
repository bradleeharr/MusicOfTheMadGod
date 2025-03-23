




# VB Cable is a Required Dependency
$vbCableFound = 1
if (-not $vbCableFound) {
    Write-Host "========== Installing VB Cable ========== "
    $vbCableUrl = "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack45.zip"
    $vbCableDownloadedZip = "vbCableDriverPack45.zip"
    $vbCableExtractedFolder = "vbCableDriverPack45"

    Invoke-WebRequest $vbCableUrl -o $vbCableDownloadedZip
    if (!(Test-Path -PathType container $vbCableExtractedFolder)) {
        mkdir $vbCableExtractedFolder
    }
    Expand-Archive $vbCableDownloadedZip $vbCableExtractedFolder -Force
    Start-Process "$vbCableExtractedFolder\VBCABLE_Setup_x64.exe"
    Write-Host "========== Please Restart your PC, then rerun ========== "
    Return
}




# Do nothing until RotMG Exalt exe is Open
$rotmgActive = 0
while (-not $rotmgActive) {
    $exaltProcessInfo = Get-Process -Name "RotMG Exalt" -ErrorAction SilentlyContinue
    $exaltFileInfo = Get-Process -Name "RotMG Exalt" -FileVersionInfo -ErrorAction SilentlyContinue
    if ($exaltFileInfo -and $exaltProcessInfo) {
        $rotmgActive = 1
        Write-Host "========= Found RotMG Exalt Loaded ========== "
        Write-Host $exaltProcessInfo
        Write-Host $exaltFileInfo
    } 
    Start-Sleep -Milliseconds 200 
}



Write-Host "========== Grabbing Audio ========== " 


