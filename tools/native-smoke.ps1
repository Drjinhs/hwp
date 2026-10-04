param([string]$OutputDirectory = (Join-Path $PSScriptRoot '..\outputs\native-smoke'))
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$outputPath = [IO.Path]::GetFullPath($OutputDirectory)
[IO.Directory]::CreateDirectory($outputPath) | Out-Null
$hwp = $null
try {
    Write-Output 'Creating a new Hancom COM object...'
    $hwp = New-Object -ComObject HWPFrame.HwpObject
    Write-Output 'COM object created.'
    $hwp.XHwpWindows.Item(0).Visible = $false
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
    $content = @"
hwp 스킬 문서 제작 테스트

1. 테스트 목적
이 문서는 독립적인 hwp 스킬의 실제 한글 저장 기능을 확인하기 위한 공개 샘플입니다.
2. 확인 항목
한글 텍스트 입력, HWPX 저장, HWP 저장, 최종 파일 재열기와 PDF 출력을 확인합니다.
3. 기대 결과
두 형식의 본문 내용이 같고 한글에서 정상적으로 열려야 합니다.
4. 안내
이 자료는 테스트용이며 사용자 문서나 개인정보를 포함하지 않습니다.
"@
    $insert = $hwp.HParameterSet.HInsertText
    $hwp.HAction.GetDefault('InsertText', $insert.HSet) | Out-Null
    $insert.Text = $content
    if (-not $hwp.HAction.Execute('InsertText', $insert.HSet)) { throw 'InsertText failed' }
    $report = [ordered]@{ font = $font; purpose = 'Native serialization smoke test, not a report typography template'; formats = @() }
    foreach ($format in @('HWPX', 'HWP')) {
        Write-Output "Saving and reopening $format..."
        $documentPath = Join-Path $outputPath ('sample.' + $format.ToLower())
        if (Test-Path -LiteralPath $documentPath) { throw "Refusing to overwrite $documentPath" }
        if (-not $hwp.SaveAs($documentPath, $format, '')) { throw "SaveAs failed: $format" }
        if (-not $hwp.Open($documentPath, $format, '')) { throw "Reopen failed: $format" }
        $readback = $hwp.GetTextFile('TEXT', '')
        if ($readback -notmatch '독립적인 hwp 스킬' -or $readback -notmatch '개인정보를 포함하지 않습니다') { throw "Readback failed: $format" }
        $pdfPath = Join-Path $outputPath ('sample-' + $format.ToLower() + '.pdf')
        if (Test-Path -LiteralPath $pdfPath) { throw "Refusing to overwrite $pdfPath" }
        $pdfSaved = $hwp.SaveAs($pdfPath, 'PDF', '')
        Write-Output "Completed $format, PDF saved: $pdfSaved"
        $report.formats += [ordered]@{ format = $format; saved = $true; reopened = $true; text_verified = $true; pages = $hwp.PageCount; pdf_saved = [bool]$pdfSaved }
    }
    $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outputPath 'report.json') -Encoding UTF8
    $report | ConvertTo-Json -Depth 5
} finally {
    if ($null -ne $hwp) { $hwp.Quit() | Out-Null }
}
