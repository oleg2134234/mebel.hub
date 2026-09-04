param(
    [string]$Source = (Join-Path $PSScriptRoot '../assets/adel-4-dk/slide_dims.jpg'),
    [string]$Output = (Join-Path $PSScriptRoot '../assets/adel-4-dk/slide_dims-v2.png')
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$sourceImage = [System.Drawing.Bitmap]::FromFile((Resolve-Path $Source))
if ($sourceImage.Width -ne 1200 -or $sourceImage.Height -ne 1423) {
    $sourceImage.Dispose()
    throw 'Source dimensions changed; recheck safe empty-field rectangles.'
}
$canvas = [System.Drawing.Bitmap]::new($sourceImage.Width,$sourceImage.Height)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
try {
    # Preserve the source pixels exactly, then edit only empty background and
    # dimension graphics. Neither sofa is touched.
    $graphics.DrawImageUnscaled($sourceImage,0,0)
    $graphics.FillRectangle([System.Drawing.Brushes]::White,425,638,385,61)
    $graphics.FillRectangle([System.Drawing.Brushes]::White,145,1294,910,95)
    # The JPEG background is nominally white but contains near-white compression
    # noise. The green sofa and graphite graphics are well below this threshold.
    for ($y=0; $y -lt $canvas.Height; $y++) {
        for ($x=0; $x -lt $canvas.Width; $x++) {
            $pixel=$canvas.GetPixel($x,$y)
            if ($pixel.R -ge 235 -and $pixel.G -ge 235 -and $pixel.B -ge 235) {
                $canvas.SetPixel($x,$y,[System.Drawing.Color]::White)
            }
        }
    }
    # The source wrongly presents 152 as a vertical height on the right. Remove
    # that graphic from empty background and redraw depth at the lower-left,
    # parallel to the side projection of the unfolded sofa.
    $graphics.FillRectangle([System.Drawing.Brushes]::White,990,740,115,300)
    $inkColor=[System.Drawing.Color]::FromArgb(40,45,47)
    $ink=[System.Drawing.SolidBrush]::new($inkColor)
    $pen=[System.Drawing.Pen]::new($inkColor,2)
    $font=[System.Drawing.Font]::new('Arial',24,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
    $format=[System.Drawing.StringFormat]::new()
    $format.Alignment=[System.Drawing.StringAlignment]::Center
    $format.LineAlignment=[System.Drawing.StringAlignment]::Center
    try {
        $x1=105; $y1=1010; $x2=260; $y2=1148
        $graphics.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $graphics.DrawLine($pen,$x1,$y1,$x2,$y2)
        $graphics.FillEllipse($ink,$x1-5,$y1-5,10,10)
        $graphics.FillEllipse($ink,$x2-5,$y2-5,10,10)
        $labelX=($x1+$x2)/2; $labelY=($y1+$y2)/2
        $capsule=[System.Drawing.Drawing2D.GraphicsPath]::new()
        try {
            $capsule.AddArc($labelX-53,$labelY-24,48,48,90,180)
            $capsule.AddArc($labelX+5,$labelY-24,48,48,270,180)
            $capsule.CloseFigure()
            $graphics.FillPath($ink,$capsule)
        } finally { $capsule.Dispose() }
        $graphics.DrawString('152',$font,[System.Drawing.Brushes]::White,[System.Drawing.RectangleF]::new($labelX-53,$labelY-24,106,48),$format)
    } finally {
        $format.Dispose(); $font.Dispose(); $pen.Dispose(); $ink.Dispose()
    }
    $canvas.Save([System.IO.Path]::GetFullPath($Output),[System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $graphics.Dispose(); $canvas.Dispose(); $sourceImage.Dispose()
}
