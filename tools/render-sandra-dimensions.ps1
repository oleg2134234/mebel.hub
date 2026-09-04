param(
    [string]$Source = (Join-Path $PSScriptRoot '../assets/sandra-2-dk/dims_base.png'),
    [string]$Output = (Join-Path $PSScriptRoot '../assets/sandra-2-dk/slide_dims.jpg')
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

# Coordinates are measured on the 1088 x 1445 base image, not guessed per render.
# A/B are the endpoints of each measured edge. Both endpoints receive the SAME
# perpendicular translation, guaranteeing parallelism and equal corner offsets.
$dimensions = @(
    @{ Text = '246'; A = @(215,350); B = @(798,535); Offset = 70 },
    @{ Text = '106,5'; A = @(827,555); B = @(906,386); Offset = 65 },
    @{ Text = '214'; A = @(171,957); B = @(739,1090); Offset = 210 },
    @{ Text = '150'; A = @(784,1225); B = @(876,1080); Offset = 60 }
)
$sourceImage = [System.Drawing.Bitmap]::FromFile((Resolve-Path $Source))
if ($sourceImage.Width -ne 1088 -or $sourceImage.Height -ne 1445) {
    $sourceImage.Dispose()
    throw 'Base image dimensions changed; recheck all measured corners.'
}
# The isolated dark-gray sofas have no near-white surfaces. Normalize the
# generator's near-white background noise to opaque #FFFFFF before drawing.
for ($pixelY = 0; $pixelY -lt $sourceImage.Height; $pixelY++) {
    for ($pixelX = 0; $pixelX -lt $sourceImage.Width; $pixelX++) {
        $pixel = $sourceImage.GetPixel($pixelX,$pixelY)
        if ($pixel.R -ge 240 -and $pixel.G -ge 240 -and $pixel.B -ge 240) {
            $sourceImage.SetPixel($pixelX,$pixelY,[System.Drawing.Color]::White)
        }
    }
}
$canvas = [System.Drawing.Bitmap]::new(1200,1594)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$ink = [System.Drawing.SolidBrush]::new([System.Drawing.Color]::FromArgb(40,45,47))
$pen = [System.Drawing.Pen]::new($ink,2)
$font = [System.Drawing.Font]::new('Arial',32,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
$format = [System.Drawing.StringFormat]::new()
$format.Alignment = [System.Drawing.StringAlignment]::Center
$format.LineAlignment = [System.Drawing.StringAlignment]::Center
try {
    $graphics.Clear([System.Drawing.Color]::White)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $graphics.ScaleTransform((1200.0/1088),(1594.0/1445))
    $graphics.DrawImage($sourceImage,0,0,1088,1445)
    foreach ($dimension in $dimensions) {
        $ax,$ay = $dimension.A
        $bx,$by = $dimension.B
        $dx = $bx - $ax; $dy = $by - $ay
        $length = [Math]::Sqrt($dx*$dx + $dy*$dy)
        $ox = -$dy / $length * $dimension.Offset
        $oy = $dx / $length * $dimension.Offset
        $x1 = $ax + $ox; $y1 = $ay + $oy
        $x2 = $bx + $ox; $y2 = $by + $oy
        if ([Math]::Abs(($x2-$x1)*$dy - ($y2-$y1)*$dx) -gt 0.000001) {
            throw 'Dimension line is not parallel.'
        }
        if ([Math]::Abs(($x1-$ax)-($x2-$bx)) -gt 0.000001 -or
            [Math]::Abs(($y1-$ay)-($y2-$by)) -gt 0.000001) {
            throw 'Corner offsets differ.'
        }
        $graphics.DrawLine($pen,[single]$x1,[single]$y1,[single]$x2,[single]$y2)
        $graphics.FillEllipse($ink,[single]($x1-4.5),[single]($y1-4.5),9,9)
        $graphics.FillEllipse($ink,[single]($x2-4.5),[single]($y2-4.5),9,9)
        $midX = ($x1+$x2)/2; $midY = ($y1+$y2)/2
        $width = [Math]::Max(94,$graphics.MeasureString($dimension.Text,$font).Width + 26)
        $left = $midX-$width/2; $top = $midY-25
        if ($left -lt 0 -or $left+$width -gt 1088 -or $top -lt 0 -or $top+50 -gt 1445) {
            throw 'Dimension label clips the canvas.'
        }
        $capsule = [System.Drawing.Drawing2D.GraphicsPath]::new()
        try {
            $capsule.AddArc([single]$left,[single]$top,50,50,90,180)
            $capsule.AddArc([single]($left+$width-50),[single]$top,50,50,270,180)
            $capsule.CloseFigure()
            $graphics.FillPath($ink,$capsule)
        } finally { $capsule.Dispose() }
        $labelBox = [System.Drawing.RectangleF]::new($left,$top,$width,50)
        $graphics.DrawString($dimension.Text,$font,[System.Drawing.Brushes]::White,$labelBox,$format)
        Write-Output ('{0} cm: parallel, equal perpendicular corner offsets ({1}px)' -f $dimension.Text,$dimension.Offset)
    }
    $encoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
    $parameters = [System.Drawing.Imaging.EncoderParameters]::new(1)
    try {
        $parameters.Param[0] = [System.Drawing.Imaging.EncoderParameter]::new([System.Drawing.Imaging.Encoder]::Quality,[long]95)
        $canvas.Save([System.IO.Path]::GetFullPath($Output),$encoder,$parameters)
    } finally { $parameters.Dispose() }
} finally {
    $format.Dispose(); $font.Dispose(); $pen.Dispose(); $ink.Dispose()
    $graphics.Dispose(); $canvas.Dispose(); $sourceImage.Dispose()
}
