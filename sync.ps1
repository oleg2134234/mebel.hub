#!/usr/bin/env pwsh
# Синхронизация репозитория между двумя компьютерами.
#   .\sync.ps1 start            — подтянуть изменения перед работой
#   .\sync.ps1 end "что сделал" — сделать бэкап, закоммитить и отправить
param(
    [Parameter(Position = 0)]
    [ValidateSet('start', 'end')]
    [string]$Action,

    [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
    [string[]]$MessageParts
)

$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

function Say($t) { Write-Host $t -ForegroundColor Cyan }
function Ok($t)  { Write-Host $t -ForegroundColor Green }
function Die($t) { Write-Host $t -ForegroundColor Red; exit 1 }

if (-not $Action) {
    Write-Host "Использование:"
    Write-Host '  .\sync.ps1 start                — подтянуть изменения перед работой'
    Write-Host '  .\sync.ps1 end "что сделал"     — бэкап + коммит + отправка'
    exit 0
}

if ($Action -eq 'start') {
    Say "-> git pull --rebase --autostash"
    git pull --rebase --autostash
    if ($LASTEXITCODE -ne 0) { Die "pull не прошёл. Разреши конфликт, затем: git rebase --continue" }
    Ok "Готово. Репозиторий актуален — можно работать."
    exit 0
}

# --- end ---
$msg = ($MessageParts -join ' ').Trim()
if (-not $msg) { $msg = "update " + (Get-Date -Format 'yyyy-MM-dd HH:mm') }

# 1. Резервная копия исходников перед отправкой — быстрый офлайн-откат.
#    Медиа (модели, соцсети) в бэкап не кладём: они тяжёлые и меняются редко,
#    их откат — через git. См. CLAUDE.md → «Откат обновлений».
$backupDir = Join-Path $PSScriptRoot 'backups'
New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
$zip = Join-Path $backupDir ("source_" + (Get-Date -Format 'yyyy-MM-dd_HHmm') + ".zip")
$include = @(
    'index.html', 'CLAUDE.md', '.gitattributes', '.gitignore',
    'sync.ps1', 'sync.sh', 'tools', 'assets\fonts', 'assets\brand'
) | ForEach-Object { Join-Path $PSScriptRoot $_ } | Where-Object { Test-Path $_ }
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path $include -DestinationPath $zip -CompressionLevel Optimal
Say ("-> бэкап: backups/" + [IO.Path]::GetFileName($zip))
# держим только 15 последних
Get-ChildItem $backupDir -Filter 'source_*.zip' |
    Sort-Object LastWriteTime -Descending | Select-Object -Skip 15 |
    Remove-Item -Force -ErrorAction SilentlyContinue

# 2. Коммит (если есть что коммитить).
git add -A
if (git diff --cached --name-only) {
    Say "-> commit: $msg"
    git commit -m $msg
    if ($LASTEXITCODE -ne 0) { Die "commit не прошёл." }
}
else {
    Write-Host "Новых изменений нет — проверю неотправленные коммиты." -ForegroundColor Yellow
}

# 3. Подтянуть чужое и отправить.
Say "-> git pull --rebase --autostash"
git pull --rebase --autostash
if ($LASTEXITCODE -ne 0) { Die "pull перед push не прошёл. Разреши конфликт, затем снова: .\sync.ps1 end" }

Say "-> git push"
git push
if ($LASTEXITCODE -ne 0) { Die "push не прошёл." }
Ok "Отправлено. На другой машине в начале работы: .\sync.ps1 start"
