param(
    [string]$OutputDirectory = (Join-Path $PSScriptRoot '..\outputs\native-smoke'),
    [string]$SecurityModulePath = '',
    [switch]$ShowWindow
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$outputPath = [IO.Path]::GetFullPath($OutputDirectory)
[IO.Directory]::CreateDirectory($outputPath) | Out-Null
$hwp = $null
$moduleKey = $null
$moduleName = $null
$moduleHash = $null
try {
    if ($SecurityModulePath) {
        $dllPath = (Resolve-Path -LiteralPath $SecurityModulePath).Path
        $moduleHash = (Get-FileHash -LiteralPath $dllPath -Algorithm SHA256).Hash
        $moduleName = 'HwpSmoke_' + [Guid]::NewGuid().ToString('N')
        $moduleKey = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey('Software\HNC\HwpAutomation\Modules')
        $moduleKey.SetValue($moduleName, $dllPath, [Microsoft.Win32.RegistryValueKind]::String)
    }
    Write-Output 'Creating a new Hancom COM object...'
    $hwp = New-Object -ComObject HWPFrame.HwpObject
    Write-Output 'COM object created.'
    if ($moduleName) {
        $moduleRegistered = $hwp.RegisterModule('FilePathCheckDLL', $moduleName)
        Write-Output "Official security module registration: $moduleRegistered"
        if (-not $moduleRegistered) { throw 'Official security module registration failed; stopping before file access' }
    }
    $hwp.XHwpWindows.Item(0).Visible = [bool]$ShowWindow
    $installedFonts = New-Object System.Drawing.Text.InstalledFontCollection
    $fontNames = @($installedFonts.Families | ForEach-Object { $_.Name })
    $font = if ($fontNames -contains '휴먼명조') { '휴먼명조' } elseif ($fontNames -contains '함초롬바탕') { '함초롬바탕' } else { throw 'No verified sample font available' }
    $char = $hwp.HParameterSet.HCharShape
    $hwp.HAction.GetDefault('CharShape', $char.HSet) | Out-Null
    $char.FaceNameHangul = $font
    $char.FaceNameLatin = $font
    $char.Height = 1400
    if (-not $hwp.HAction.Execute('CharShape', $char.HSet)) { throw 'CharShape failed' }
    $para = $hwp.HParameterSet.HParaShape
    $hwp.HAction.GetDefault('ParagraphShape', $para.HSet) | Out-Null
    $para.LineSpacingType = 0
    $para.LineSpacing = 145
    if (-not $hwp.HAction.Execute('ParagraphShape', $para.HSet)) { throw 'ParagraphShape failed' }
    $paragraphs = @(
        @{ Text = 'hwp 스킬 문서 제작 테스트'; Size = 20; Bold = $true },
        @{ Text = ''; Size = 14; Bold = $false },
        @{ Text = '1. 테스트 목적'; Size = 14; Bold = $true },
        @{ Text = '이 문서는 독립적인 hwp 스킬의 실제 한글 저장 기능을 확인하기 위한 공개 샘플입니다.'; Size = 14; Bold = $false },
        @{ Text = ''; Size = 7; Bold = $false },
        @{ Text = '2. 확인 항목'; Size = 14; Bold = $true },
        @{ Text = '한글 텍스트 입력, HWPX 저장, HWP 저장, 최종 파일 재열기와 PDF 출력을 확인합니다.'; Size = 14; Bold = $false },
        @{ Text = ''; Size = 7; Bold = $false },
        @{ Text = '3. 기대 결과'; Size = 14; Bold = $true },
        @{ Text = '두 형식의 본문 내용이 같고 한글에서 정상적으로 열려야 합니다.'; Size = 14; Bold = $false },
        @{ Text = ''; Size = 7; Bold = $false },
        @{ Text = '4. 안내'; Size = 14; Bold = $true },
        @{ Text = '테스트 문서에는 사용자 문서와 개인정보가 없습니다.'; Size = 14; Bold = $false }
    )
    for ($index = 0; $index -lt $paragraphs.Count; $index++) {
        $item = $paragraphs[$index]
        $hwp.HAction.GetDefault('CharShape', $char.HSet) | Out-Null
        $char.Height = $item.Size * 100
        $char.Bold = $item.Bold
        if (-not $hwp.HAction.Execute('CharShape', $char.HSet)) { throw 'Paragraph character formatting failed' }
        if ($item.Text) {
            $insert = $hwp.HParameterSet.HInsertText
            $hwp.HAction.GetDefault('InsertText', $insert.HSet) | Out-Null
            $insert.Text = $item.Text
            if (-not $hwp.HAction.Execute('InsertText', $insert.HSet)) { throw 'InsertText failed' }
        }
        if ($index -lt ($paragraphs.Count - 1)) {
            if (-not $hwp.HAction.Run('BreakPara')) { throw 'BreakPara failed' }
        }
    }
    $report = [ordered]@{ font = $font; security_module_sha256 = $moduleHash; purpose = 'Native serialization smoke test, not a report typography template'; formats = @() }
    foreach ($format in @('HWPX', 'HWP')) {
        Write-Output "Saving and reopening $format..."
        $documentPath = Join-Path $outputPath ('sample.' + $format.ToLower())
        if (Test-Path -LiteralPath $documentPath) { throw "Refusing to overwrite $documentPath" }
        if (-not $hwp.SaveAs($documentPath, $format, '')) { throw "SaveAs failed: $format" }
        if (-not $hwp.Open($documentPath, $format, '')) { throw "Reopen failed: $format" }
        $readback = $hwp.GetTextFile('TEXT', '')
        foreach ($item in $paragraphs) {
            if ($item.Text -and (($readback -replace '\s+', '') -notlike ('*' + ($item.Text -replace '\s+', '') + '*'))) {
                throw "Readback failed: $format"
            }
        }
        $pdfPath = Join-Path $outputPath ('sample-' + $format.ToLower() + '.pdf')
        if (Test-Path -LiteralPath $pdfPath) { throw "Refusing to overwrite $pdfPath" }
        $pdfSaved = $hwp.SaveAs($pdfPath, 'PDF', '')
        Write-Output "Completed $format, PDF saved: $pdfSaved"
        $report.formats += [ordered]@{ format = $format; saved = $true; reopened = $true; text_verified = $true; pages = $hwp.PageCount; pdf_saved = [bool]$pdfSaved }
    }
    $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outputPath 'report.json') -Encoding UTF8
    $report | ConvertTo-Json -Depth 5
} finally {
    if ($moduleKey -and $moduleName) {
        $moduleKey.DeleteValue($moduleName, $false)
        $moduleKey.Close()
    }
    if ($null -ne $hwp) { $hwp.Quit() | Out-Null }
}
