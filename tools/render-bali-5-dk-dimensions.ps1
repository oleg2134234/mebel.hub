param(
    [string]$Folded = (Join-Path $PSScriptRoot '../assets/bali-5-dk-standart/slide3_angle.jpg'),
    [string]$Unfolded = (Join-Path $PSScriptRoot '../assets/bali-5-dk-standart/slide7_unfold.jpg'),
    [string]$Output = (Join-Path $PSScriptRoot '../assets/bali-5-dk-standart/slide_dims-v2.jpg')
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$canvas = [System.Drawing.Bitmap]::new(1200,1800)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
$foldedImage = [System.Drawing.Bitmap]::FromFile((Resolve-Path $Folded))
$unfoldedImage = [System.Drawing.Bitmap]::FromFile((Resolve-Path $Unfolded))
$inkColor = [System.Drawing.Color]::FromArgb(40,45,47)
$ink = [System.Drawing.SolidBrush]::new($inkColor)
$pen = [System.Drawing.Pen]::new($inkColor,3)
$font = [System.Drawing.Font]::new('Arial',34,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
$format = [System.Drawing.StringFormat]::new()
$format.Alignment = [System.Drawing.StringAlignment]::Center
$format.LineAlignment = [System.Drawing.StringAlignment]::Center

function Draw-Panel([System.Drawing.Bitmap]$image,[int]$top) {
    $graphics.DrawImage($image,[System.Drawing.Rectangle]::new(60,$top,1080,810),0,0,1600,1200,[System.Drawing.GraphicsUnit]::Pixel)
}
function Map-Point([double]$x,[double]$y,[double]$top) {
    return @((60 + $x*0.675), ($top + $y*0.675))
}
function Draw-Dimension([string]$text,[double[]]$a,[double[]]$b,[double]$offset,[double]$panelTop) {
    $dx=$b[0]-$a[0]; $dy=$b[1]-$a[1]; $length=[Math]::Sqrt($dx*$dx+$dy*$dy)
    $x1=$a[0]-$dy/$length*$offset; $y1=$a[1]+$dx/$length*$offset
    $x2=$b[0]-$dy/$length*$offset; $y2=$b[1]+$dx/$length*$offset
    $p1=Map-Point $x1 $y1 $panelTop; $p2=Map-Point $x2 $y2 $panelTop
    if ([Math]::Abs(($x2-$x1)*$dy-($y2-$y1)*$dx) -gt 0.000001) { throw 'Line is not parallel' }
    if ([Math]::Abs(($x1-$a[0])-($x2-$b[0])) -gt 0.000001 -or [Math]::Abs(($y1-$a[1])-($y2-$b[1])) -gt 0.000001) { throw 'Offsets differ' }
    $graphics.DrawLine($pen,[single]$p1[0],[single]$p1[1],[single]$p2[0],[single]$p2[1])
    foreach($p in @($p1,$p2)){ $graphics.FillEllipse($ink,[single]($p[0]-5),[single]($p[1]-5),10,10) }
    $mx=($p1[0]+$p2[0])/2; $my=($p1[1]+$p2[1])/2
    $width=[Math]::Max(96,$graphics.MeasureString($text,$font).Width+28); $height=54
    $left=$mx-$width/2; $top=$my-$height/2
    $path=[System.Drawing.Drawing2D.GraphicsPath]::new()
    try {
        $path.AddArc([single]$left,[single]$top,$height,$height,90,180)
        $path.AddArc([single]($left+$width-$height),[single]$top,$height,$height,270,180)
        $path.CloseFigure(); $graphics.FillPath($ink,$path)
    } finally { $path.Dispose() }
    $graphics.DrawString($text,$font,[System.Drawing.Brushes]::White,[System.Drawing.RectangleF]::new($left,$top,$width,$height),$format)
    Write-Output "$text cm: parallel; equal corner offsets"
}
try {
    $graphics.Clear([System.Drawing.Color]::White)
    $graphics.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $graphics.TextRenderingHint=[System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    Draw-Panel $foldedImage 0
    Draw-Dimension '236' @(280,920) @(1410,830) 85 0
    Draw-Dimension '108' @(280,920) @(135,735) 70 0
    Draw-Panel $unfoldedImage 900
    Draw-Dimension '202' @(465,910) @(1390,800) 110 900
    Draw-Dimension '160' @(465,910) @(320,455) 85 900
    $encoder=[System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders()|Where-Object MimeType -eq 'image/jpeg'
    $parameters=[System.Drawing.Imaging.EncoderParameters]::new(1)
    try {
        $parameters.Param[0]=[System.Drawing.Imaging.EncoderParameter]::new([System.Drawing.Imaging.Encoder]::Quality,[long]95)
        $canvas.Save([System.IO.Path]::GetFullPath($Output),$encoder,$parameters)
    } finally { $parameters.Dispose() }
} finally {
    $format.Dispose();$font.Dispose();$pen.Dispose();$ink.Dispose();$graphics.Dispose();$canvas.Dispose();$foldedImage.Dispose();$unfoldedImage.Dispose()
}
