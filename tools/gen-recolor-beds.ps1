$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$key = (Get-Content 'kie_api_key.txt' -Raw).Trim()
$H = @{ Authorization = "Bearer $key" }
$out = 'C:\Temp\claude\C--Users-papa-Downloads-Claude\5ab331ec-020f-46dd-9112-949fdd2f4c5a\scratchpad\kie-recolor'
New-Item -ItemType Directory -Force -Path $out | Out-Null

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

$common = "Do NOT change the room, walls, curtains, other furniture, lighting, camera angle, or the bed's shape/silhouette/proportions/construction. Do NOT redraw or restyle the bed. Everything else pixel-for-pixel identical. Output a clean photo with no visible edit artifacts."

$jobs = @(
    @{ name = "soty-1";   src = "https://oleg2134234.github.io/mebel.hub/assets/soty-1/slide1_hero.jpg";
       prompt = "Take this exact real product photo of an upholstered bed with a honeycomb-stitched fabric headboard in a bedroom interior, and return it with two edits: (1) recolor the bed's velour fabric (headboard and base, including the matching nightstand) from dark green to a neutral warm-grey velour like the rest of this product's studio photos, keeping the same fabric texture, stitching pattern, and folds; (2) completely remove all text, the model name headline, and the rounded badge icons overlaid on the image - restore that area to the plain interior scene as if they were never there. $common" },
    @{ name = "rica-1";   src = "https://oleg2134234.github.io/mebel.hub/assets/rica-1/slide1_hero.jpg";
       prompt = "Take this exact real product photo of an upholstered bed with a geometric-stitched fabric headboard in a bedroom interior, and return it with two edits: (1) recolor the bed's velour fabric (headboard and base) from dusty pink/mauve to a neutral warm-grey velour like the rest of this product's studio photos, keeping the same fabric texture, stitching pattern, and folds; (2) completely remove all text, the model name headline, and the rounded badge icons overlaid on the image - restore that area to the plain interior scene as if they were never there. $common" },
    @{ name = "eklips-3"; src = "https://oleg2134234.github.io/mebel.hub/assets/eklips-3/slide1_hero.jpg";
       prompt = "Take this exact real product photo of an upholstered bed with a chevron-stitched fabric headboard in a bedroom interior, and return it with two edits: (1) recolor the bed's velour fabric (headboard and base) from dusty pink/mauve to a neutral warm-grey velour like the rest of this product's studio photos, keeping the same fabric texture, stitching pattern, and folds; (2) completely remove all text, the model name headline, and the rounded badge icons overlaid on the image - restore that area to the plain interior scene as if they were never there. $common" }
)

$taskIds = @{}
foreach ($j in $jobs) {
    Write-Host ("=== {0} ===" -f $j.name)
    $taskIds[$j.name] = New-KieTask $j.prompt $j.src
}

foreach ($name in $taskIds.Keys) {
    $url = Wait-KieTask $taskIds[$name]
    Write-Host ("{0} result: {1}" -f $name, $url)
    Invoke-WebRequest -Uri $url -OutFile "$out\$name.png"
}
Write-Host "Done. Files in $out"
