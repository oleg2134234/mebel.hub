param(
    [string]$Source = (Join-Path $PSScriptRoot '../assets/brand/logo.jpg'),
    [string]$Output = (Join-Path $PSScriptRoot '../assets/brand/logo-transparent-v2.png')
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

$sourceImage = [System.Drawing.Bitmap]::FromFile((Resolve-Path $Source))
$outputImage = [System.Drawing.Bitmap]::new(
    $sourceImage.Width,
    $sourceImage.Height,
    [System.Drawing.Imaging.PixelFormat]::Format32bppArgb
)
try {
    for ($y=0; $y -lt $sourceImage.Height; $y++) {
        for ($x=0; $x -lt $sourceImage.Width; $x++) {
            $pixel=$sourceImage.GetPixel($x,$y)
            # The source is a black mark on white. Convert its luminance to
            # opacity so JPEG antialiasing becomes a clean transparent edge.
            $luma=[int][Math]::Round(0.2126*$pixel.R + 0.7152*$pixel.G + 0.0722*$pixel.B)
            $alpha=[Math]::Max(0,[Math]::Min(255,255-$luma))
            $outputImage.SetPixel($x,$y,[System.Drawing.Color]::FromArgb($alpha,0,0,0))
        }
    }
    $outputImage.Save([System.IO.Path]::GetFullPath($Output),[System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $outputImage.Dispose()
    $sourceImage.Dispose()
}
