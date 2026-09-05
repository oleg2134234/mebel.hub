$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Reusable template: regenerate ONE dims panel (folded or unfolded) from an existing
# real gallery photo when its measurement callout lines are crooked / not parallel to
# the object's edges. See CLAUDE.md "Как делать слайд Размеры" for the full process.
# Example run: Финка 3 ДК unfolded panel, 05.09.2026 (see docs/catalog/CHANGELOG.md).

$key = (Get-Content 'kie_api_key.txt' -Raw).Trim()
$H = @{ Authorization = "Bearer $key" }
$out = 'C:\Temp\claude\C--Users-papa-Downloads-Claude\5ab331ec-020f-46dd-9112-949fdd2f4c5a\scratchpad\kie-dims-fix'
New-Item -ItemType Directory -Force -Path $out | Out-Null

# --- EDIT THESE for each new fix ---
$sourceUrl = "https://oleg2134234.github.io/mebel.hub/assets/finka-3-dk/slide4_unfold.jpg"
$lengthNum = 197   # long edge, front-bottom
$widthNum  = 140   # short edge, near-left, going back into depth
$fabricDesc = "blue tufted velour fabric"
# ------------------------------------

$prompt = "Take this exact real product photo of a sofa-bed fully unfolded flat into a long bed, three-quarter angle view (near-left corner closest to camera, far-right corner furthest away), and return it UNCHANGED except for added measurement lines. Reproduce the object pixel-for-pixel: same $fabricDesc and texture, same exact shape and proportions and every detail, same lighting. Do NOT simplify it into a plain box, do NOT redraw it, do NOT change its silhouette, do NOT change the background scene. Background: plain seamless white studio backdrop, no floor, no wall, no room. ADD only two measurement callouts, both STRICTLY PARALLEL to the object edge they measure and fully outside the object silhouette, never crossing or touching the bed: a thin dark charcoal straight line with a small round dot at each end, and a dark charcoal rounded-pill label containing ONLY a white bold number (no letters, no words, no brackets, no units). One line runs along the near-left short edge of the bed (the width/depth edge going from the front-left corner back towards the far side), parallel to that edge, offset a small constant distance outward to the left, with the number $widthNum. One line runs along the front-bottom long edge of the bed (the length edge), parallel to that edge, offset a small constant distance below it, with the number $lengthNum. Both lines span the full length of the edge they measure, from corner to corner, each endpoint offset from its corresponding corner by the same small perpendicular distance. Do not tilt, skew or diagonally cut across the frame with either line. No other lines, numbers or text."

$body = @{
    model = "nano-banana-pro"
    input = @{
        prompt        = $prompt
        image_input   = @($sourceUrl)
        aspect_ratio  = "4:3"
        resolution    = "2K"
        output_format = "png"
    }
} | ConvertTo-Json -Depth 8
$r = Invoke-RestMethod -Method Post -Uri "https://api.kie.ai/api/v1/jobs/createTask" -Headers $H -ContentType "application/json" -Body $body
Write-Host ("createTask -> code={0} taskId={1}" -f $r.code, $r.data.taskId)
$id = $r.data.taskId
if (-not $id) { throw ("no taskId: " + ($r | ConvertTo-Json -Depth 6)) }

for ($i = 0; $i -lt 90; $i++) {
    Start-Sleep -Seconds 5
    $rr = Invoke-RestMethod -Method Get -Uri "https://api.kie.ai/api/v1/jobs/recordInfo?taskId=$id" -Headers $H
    $st = $rr.data.state
    Write-Host ("  state={0} progress={1}" -f $st, $rr.data.progress)
    if ($st -eq 'success') {
        $url = ($rr.data.resultJson | ConvertFrom-Json).resultUrls[0]
        Write-Host "result: $url"
        Invoke-WebRequest -Uri $url -OutFile "$out\panel.png"
        Write-Host "saved to $out\panel.png"
        exit 0
    }
    if ($st -eq 'fail') { throw ("task fail: {0} {1}" -f $rr.data.failCode, $rr.data.failMsg) }
}
throw "timeout"
