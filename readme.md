# Whatsapp stickers hosting

## Convert png to webp

Use the Image Magick software to do it

https://github.com/ImageMagick/ImageMagick

### Commands

#### Generate all images png to webp

magick mogrify -format webp *.png

#### Transform gif to pngs

magick 1.gif -coalesce xx_%05d.png

#### Make a webp to loop

magick 4.webp -loop 0 4-final.webp -quality

#### Transform png to animated gif/webp

magick convert -resize 512x512 -dispose Previous  x0.png x1.png -loop 0 anim1.gif

### Dudas y Referencias

- https://askubuntu.com/questions/648244/how-do-i-create-an-animated-gif-from-still-images-preferably-with-the-command-l
- https://stackoverflow.com/questions/51830740/imagemagick-gif-and-overlaying-png-image
- https://github.com/ImageMagick/ImageMagick/issues/6479
- https://stackoverflow.com/questions/49591274/cli-command-to-convert-webp-images-to-jpg