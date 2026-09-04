param(
  [string]$OutputDir = "audit-output/contact-sheets"
)

Add-Type -AssemblyName System.Drawing
$root = Split-Path -Parent $PSScriptRoot
$html = Get-Content -Raw -LiteralPath (Join-Path $root "index.html")
$productsJson = [regex]::Match($html, 'const PRODUCTS = (\[.*?\]);\r?\n', 'Singleline').Groups[1].Value
$galleriesJson = [regex]::Match($html, 'const GALLERIES = (\{.*?\});\r?\n', 'Singleline').Groups[1].Value
$products = $productsJson | ConvertFrom-Json
$galleries = $galleriesJson | ConvertFrom-Json -AsHashtable
$out = Join-Path $root $OutputDir
New-Item -ItemType Directory -Force -Path $out | Out-Null

$font = [System.Drawing.Font]::new("Arial", 12)
$titleFont = [System.Drawing.Font]::new("Arial", 18, [System.Drawing.FontStyle]::Bold)
$brush = [System.Drawing.Brushes]::Black
$muted = [System.Drawing.Brushes]::DimGray
$columns = 4
$cellW = 300
$cellH = 250

foreach ($p in ($products | Where-Object category -eq "sofa")) {
  $gallery = $galleries[[string]$p.id]
  if (-not $gallery) { continue }
  $slides = @($gallery.slides)
  $rows = [Math]::Ceiling($slides.Count / $columns)
  $canvas = [System.Drawing.Bitmap]::new($columns * $cellW, 55 + $rows * $cellH)
  $graphics = [System.Drawing.Graphics]::FromImage($canvas)
  $graphics.Clear([System.Drawing.Color]::White)
  $graphics.DrawString("$($p.id) · $($p.title) · $($slides.Count) слайдов", $titleFont, $brush, 12, 12)

  for ($i = 0; $i -lt $slides.Count; $i++) {
    $slide = $slides[$i]
    $x = ($i % $columns) * $cellW
    $y = 55 + [Math]::Floor($i / $columns) * $cellH
    $src = [string]$slide.src
    if ($p.id -eq 5 -and $src -eq "assets/ostin-3-dk/slide_hero_interior.jpg") { $src = "assets/ostin-3-dk/slide_hero_interior-v2.png" }
    if ($p.id -eq 5 -and $src -eq "assets/ostin-3-dk/slide_hero_real.jpg") { $src = "assets/ostin-3-dk/slide_hero_real-v2.png" }
    $mediaPath = Join-Path $root $src
    $graphics.DrawRectangle([System.Drawing.Pens]::LightGray, $x + 5, $y + 5, $cellW - 10, 205)
    if ((Test-Path -LiteralPath $mediaPath) -and $slide.type -ne "video") {
      try {
        $image = [System.Drawing.Image]::FromFile($mediaPath)
        $scale = [Math]::Min(($cellW - 12) / $image.Width, 198 / $image.Height)
        $w = [int]($image.Width * $scale)
        $h = [int]($image.Height * $scale)
        $graphics.DrawImage($image, $x + [int](($cellW - $w) / 2), $y + 8 + [int]((198 - $h) / 2), $w, $h)
        $image.Dispose()
      } catch {
        $graphics.DrawString("Ошибка изображения", $font, [System.Drawing.Brushes]::DarkRed, $x + 12, $y + 90)
      }
    } else {
      $graphics.FillRectangle([System.Drawing.Brushes]::Black, $x + 8, $y + 8, $cellW - 16, 198)
      $graphics.DrawString("ВИДЕО", $titleFont, [System.Drawing.Brushes]::White, $x + 105, $y + 90)
    }
    $graphics.DrawString("[$($i + 1)] $($slide.name)", $font, $brush, $x + 8, $y + 214)
    $graphics.DrawString((Split-Path -Leaf $src), $font, $muted, $x + 8, $y + 232)
  }

  $safeName = ([string]$p.title -replace '[\\/:*?"<>|]', '_')
  $dest = Join-Path $out ("{0:D3}-{1}.jpg" -f [int]$p.id, $safeName)
  $canvas.Save($dest, [System.Drawing.Imaging.ImageFormat]::Jpeg)
  $graphics.Dispose()
  $canvas.Dispose()
}

$font.Dispose()
$titleFont.Dispose()
Get-ChildItem -LiteralPath $out -Filter *.jpg | Sort-Object Name | Select-Object FullName, Length
