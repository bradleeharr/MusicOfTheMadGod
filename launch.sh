Write-Host "========== Starting =========="


# VB Cable is a Required Dependency
$vbCableFound = Get-CimInstance -ClassName Win32_SoundDevice | Where-Object { $_.Name -like "*VB-Audio*" }
if (-not $vbCableFound) {
    Write-Host "========== Installing VB Cable =========="
    $vbCableUrl = "https://download.vb-audio.com/Download_CABLE/VBCABLE_Driver_Pack45.zip"
    $vbCableDownloadedZip = "vbCableDriverPack45.zip"
    $vbCableExtractedFolder = "vbCableDriverPack45"

    Invoke-WebRequest $vbCableUrl -o $vbCableDownloadedZip
    if (!(Test-Path -PathType container $vbCableExtractedFolder)) {
        mkdir $vbCableExtractedFolder
    }
    Expand-Archive $vbCableDownloadedZip $vbCableExtractedFolder -Force
    Start-Process "$vbCableExtractedFolder\VBCABLE_Setup_x64.exe" -Wait
    Remove-Item $vbCableDownloadedZip
    # Remove-Item $vbCableExtractedFolder
    Write-Host "========== Please Restart your PC, then rerun =========="
    Exit 0
} else {
    Write-Host "VB Cable Found."
}


# Do nothing until RotMG Exalt exe is Open
$rotmgActive = 0
Write-Host "Please Start RotMG Exalt" -NoNewLine
while (-not $rotmgActive) {
    $exaltProcessInfo = Get-Process -Name "RotMG Exalt" -ErrorAction SilentlyContinue
    $exaltFileInfo = Get-Process -Name "RotMG Exalt" -FileVersionInfo -ErrorAction SilentlyContinue
    if ($exaltFileInfo -and $exaltProcessInfo) {
        $rotmgActive = 1
        Write-Host "========= Found RotMG Exalt Loaded =========="
        Write-Host $exaltProcessInfo
        Write-Host $exaltFileInfo
    } 
    Start-Sleep -Milliseconds 200 
    Write-Host "." -NoNewline
}
Write-Host "`n"


# TODO: Currently does not work. Set Manually.
Write-Host "========== Setting RotMG Output Audio =========="
Write-Host "Manually Set the Audio, then Press Enter to Continue"
Write-Host ""
# Start-Process -FilePath "powershell.exe" -Verb runAs -ArgumentList "-File $PSScriptRoot\src\SetAudio.ps1" -Wait
# REQUIRES ADMIN
# Install-Module -Name AudioDeviceCmdlets -Force
# Get-AudioDevice -List -Playback
# Get-AudioDevice -List -Recording


Write-Host "========== Launching RotMG Audio Filter App =========="

$venvDir = Join-Path -Path $PSScriptRoot -ChildPath ".venv"
$venvPythonExe = Join-Path -Path $PSScriptRoot -ChildPath ".venv\Scripts\python.exe"
$venvActivateScript = Join-Path -Path $venvDir -ChildPath "Scripts\Activate.ps1"
$venvRequirementsTxt = Join-Path -Path $PSScriptRoot -ChildPath "requirements.txt"
if ((-not (Test-Path $venvPythonExe)) -or (-not (Test-Path $venvActivateScript))) {
    Write-Host "Virtual environment not found. Creating new venv in $venvDir..."
    python -m venv $venvDir
    & $venvPythonExe -m pip install -r $venvRequirementsTxt
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create venv!"
        Exit 1
    }
} else {
    Write-Host "Found venv for python at $venvDir"
} 

# Venv now exists. Activate the venv and launch the script
. $venvActivateScript # Dot-Sourced to activate in current context
Write-Host "Venv activated, now running filter."
$filterScript = Join-Path -Path $PSScriptRoot -ChildPath "src\filter.py"

Write-Host "========== Running Filter =========="
python $filterScript 

