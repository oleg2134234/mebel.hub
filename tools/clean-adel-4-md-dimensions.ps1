param(
    [string]$Source = (Join-Path $PSScriptRoot '../assets/adel-4-md/slide5_dims.jpg'),
    [string]$Output = (Join-Path $PSScriptRoot '../assets/adel-4-md/slide5_dims-v2.png')
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$sourceImage = [System.Drawing.Bitmap]::FromFile((Resolve-Path $Source))
if ($sourceImage.Width -ne 2409 -or $sourceImage.Height -ne 2874) {
    $sourceImage.Dispose()
    throw 'Source dimensions changed; recheck safe empty-field rectangles.'
}
$canvas = [System.Drawing.Bitmap]::new($sourceImage.Width,$sourceImage.Height)
$graphics = [System.Drawing.Graphics]::FromImage($canvas)
try {
    # Keep both product photographs untouched. Only near-white background pixels
    # and the incorrect dimension graphic in empty space are edited.
    $graphics.DrawImageUnscaled($sourceImage,0,0)
    for ($y=0; $y -lt $canvas.Height; $y++) {
        for ($x=0; $x -lt $canvas.Width; $x++) {
            $pixel=$canvas.GetPixel($x,$y)
            if ($pixel.R -ge 235 -and $pixel.G -ge 235 -and $pixel.B -ge 235) {
                $canvas.SetPixel($x,$y,[System.Drawing.Color]::White)
            }
        }
    }

    # Remove the wrong vertical 120 callout on the right. The rectangle lies in
    # empty field outside the sofa. The existing lower line is preserved.
    $graphics.FillRectangle([System.Drawing.Brushes]::White,1960,1590,230,800)

    # Put 120 on the left-side line, as approved for this slide.
    $inkColor=[System.Drawing.Color]::FromArgb(45,50,59)
    $ink=[System.Drawing.SolidBrush]::new($inkColor)
    $pen=[System.Drawing.Pen]::new($inkColor,4)
    $font=[System.Drawing.Font]::new('Arial',46,[System.Drawing.FontStyle]::Bold,[System.Drawing.GraphicsUnit]::Pixel)
    $format=[System.Drawing.StringFormat]::new()
    $format.Alignment=[System.Drawing.StringAlignment]::Center
    $format.LineAlignment=[System.Drawing.StringAlignment]::Center
    try {
        $x1=85; $y1=2070; $x2=370; $y2=2510
        $graphics.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
        $graphics.DrawLine($pen,$x1,$y1,$x2,$y2)
        $graphics.FillEllipse($ink,$x1-10,$y1-10,20,20)
        $graphics.FillEllipse($ink,$x2-10,$y2-10,20,20)
        $labelX=($x1+$x2)/2; $labelY=($y1+$y2)/2
        $capsule=[System.Drawing.Drawing2D.GraphicsPath]::new()
        try {
            $capsule.AddArc($labelX-82,$labelY-38,76,76,90,180)
            $capsule.AddArc($labelX+6,$labelY-38,76,76,270,180)
            $capsule.CloseFigure()
            $graphics.FillPath($ink,$capsule)
        } finally { $capsule.Dispose() }
        $graphics.DrawString('120',$font,[System.Drawing.Brushes]::White,[System.Drawing.RectangleF]::new($labelX-82,$labelY-38,164,76),$format)

        # Put 197 on the original lower line parallel to the sofa front.
        $labelX=1460; $labelY=2560
        $capsule=[System.Drawing.Drawing2D.GraphicsPath]::new()
        try {
            $capsule.AddArc($labelX-100,$labelY-46,92,92,90,180)
            $capsule.AddArc($labelX+8,$labelY-46,92,92,270,180)
            $capsule.CloseFigure()
            $graphics.FillPath($ink,$capsule)
        } finally { $capsule.Dispose() }
        $graphics.DrawString('197',$font,[System.Drawing.Brushes]::White,[System.Drawing.RectangleF]::new($labelX-100,$labelY-46,200,92),$format)
    } finally {
        $format.Dispose(); $font.Dispose(); $pen.Dispose(); $ink.Dispose()
    }
    $canvas.Save([System.IO.Path]::GetFullPath($Output),[System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $graphics.Dispose(); $canvas.Dispose(); $sourceImage.Dispose()
}
