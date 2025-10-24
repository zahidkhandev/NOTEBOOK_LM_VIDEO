Write-Host "Exporting codebase to markdown..." -ForegroundColor Cyan

$outputDir = "docs\context"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outputFile = "$outputDir\codebase_$timestamp.md"

New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

"# NotebookLM Video Generator - Complete Codebase" | Out-File -FilePath $outputFile
"" | Out-File -FilePath $outputFile -Append
"Generated: $(Get-Date)" | Out-File -FilePath $outputFile -Append
"" | Out-File -FilePath $outputFile -Append
"---" | Out-File -FilePath $outputFile -Append
"" | Out-File -FilePath $outputFile -Append
"## Backend Code" | Out-File -FilePath $outputFile -Append
"" | Out-File -FilePath $outputFile -Append

Get-ChildItem -Path "backend\app" -Filter "*.py" -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
    "### $($_.FullName)" | Out-File -FilePath $outputFile -Append
    "" | Out-File -FilePath $outputFile -Append
    "``````python" | Out-File -FilePath $outputFile -Append
    Get-Content $_.FullName | Out-File -FilePath $outputFile -Append
    "``````" | Out-File -FilePath $outputFile -Append
    "" | Out-File -FilePath $outputFile -Append
}

"---" | Out-File -FilePath $outputFile -Append
"## Documentation" | Out-File -FilePath $outputFile -Append
"" | Out-File -FilePath $outputFile -Append

@("README.md", "PROJECT_PLAN.md", "PROGRESS.md", "backend\requirements.txt") | ForEach-Object {
    if (Test-Path $_) {
        "### $_" | Out-File -FilePath $outputFile -Append
        "" | Out-File -FilePath $outputFile -Append
        "``````" | Out-File -FilePath $outputFile -Append
        Get-Content $_ | Out-File -FilePath $outputFile -Append
        "``````" | Out-File -FilePath $outputFile -Append
        "" | Out-File -FilePath $outputFile -Append
    }
}

Write-Host "Exported to: $outputFile" -ForegroundColor Green
