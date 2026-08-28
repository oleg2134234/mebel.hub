$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$key = (Get-Content 'C:\Users\papa\.claude\kie_api_key.txt' -Raw).Trim()
$H = @{ Authorization = "Bearer $key" }
$out = 'C:\Temp\claude\C--Users-papa-Downloads-Claude\ec44cbaa-996d-4058-8839-ac007d9339a1\scratchpad'

$P_FOLDED = "Take this exact real product photo of a compact chair-bed in its folded chair state, three-quarter front view, and return it UNCHANGED except for added measurement lines. Reproduce the object pixel-for-pixel: same beige woven velour fabric colour and mottled texture, same exact shape and proportions and every detail (thick softly-rounded rolled armrests with a horizontal seam, low tufted backrest, small black plastic feet), same lighting. Do NOT simplify it into a plain box, do NOT redraw it, do NOT change its silhouette, do NOT change the background scene. Background: plain seamless very-light-grey studio backdrop, no floor, no wall, no room. ADD only two measurement callouts on the empty background: a thin dark charcoal straight line with a small round dot at each end, and a dark charcoal rounded-pill label containing ONLY a white bold number (no letters, no words, no brackets, no units). One line along the front bottom edge of the object with the number 93. One shorter line along the side bottom edge going back into depth with the number 105. Straight lines, each spanning the full length of its edge, parallel to the object edges, offset outward clear of the object, never overlapping it. No other lines or text."

$P_UNFOLD = "Take this exact real product photo of the chair-bed fully unfolded flat into a long narrow single bed (backrest folded down level with the seat, pull-out metal frame visible underneath) and return it UNCHANGED except for added measurement lines. Reproduce the object pixel-for-pixel: same beige woven velour fabric colour and mottled texture, same exact shape and proportions and every detail, same lighting. Do NOT simplify it into a plain box, do NOT redraw it, do NOT change its silhouette, do NOT change the background scene. Background: plain seamless very-light-grey studio backdrop, no floor, no wall, no room. ADD only two measurement callouts on the empty background: a thin dark charcoal straight line with a small round dot at each end, and a dark charcoal rounded-pill label containing ONLY a white bold number (no letters, no words, no brackets, no units). One line along the front bottom edge below the object with the number 197. One shorter line at the bottom-left corner going back into depth with the number 70. Straight lines, each spanning the full length of its edge, parallel to the object edges, offset outward clear of the object, never overlapping it. No other lines or text."

function New-KieTask($prompt, $img) {
    $body = @{
        model = "nano-banana-pro"
        input = @{
            prompt        = $prompt
            image_input   = @($img)
            aspect_ratio  = "4:3"
            resolution    = "2K"
            output_format = "png"
        }
    } | ConvertTo-Json -Depth 8
    $r = Invoke-RestMethod -Method Post -Uri "https://api.kie.ai/api/v1/jobs/createTask" -Headers $H -ContentType "application/json" -Body $body
    Write-Host ("createTask -> code={0} taskId={1}" -f $r.code, $r.data.taskId)
    if (-not $r.data.taskId) { throw ("no taskId: " + ($r | ConvertTo-Json -Depth 6)) }
    $r.data.taskId
}

function Wait-KieTask($id) {
    for ($i = 0; $i -lt 90; $i++) {
        Start-Sleep -Seconds 5
        $r = Invoke-RestMethod -Method Get -Uri "https://api.kie.ai/api/v1/jobs/recordInfo?taskId=$id" -Headers $H
        $st = $r.data.state
        Write-Host ("  {0}  state={1} progress={2}" -f $id, $st, $r.data.progress)
        if ($st -eq 'success') { return ($r.data.resultJson | ConvertFrom-Json).resultUrls[0] }
        if ($st -eq 'fail')    { throw ("task fail: {0} {1}" -f $r.data.failCode, $r.data.failMsg) }
    }
    throw "timeout waiting for $id"
}

$base = "https://oleg2134234.github.io/mebel.hub/assets/adel-4-kreslo-krovat"

Write-Host "=== FOLDED ==="
$t1 = New-KieTask $P_FOLDED "$base/real4_angle.jpg"
Write-Host "=== UNFOLDED ==="
$t2 = New-KieTask $P_UNFOLD "$base/real5_unfold.jpg"

$u1 = Wait-KieTask $t1
Write-Host "folded result: $u1"
$u2 = Wait-KieTask $t2
Write-Host "unfold result: $u2"

Invoke-WebRequest -Uri $u1 -OutFile "$out\gen_folded.png"
Invoke-WebRequest -Uri $u2 -OutFile "$out\gen_unfold.png"
Write-Host ("saved: {0} KB / {1} KB" -f [math]::Round((Get-Item "$out\gen_folded.png").Length/1KB), [math]::Round((Get-Item "$out\gen_unfold.png").Length/1KB))
