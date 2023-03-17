# SteganographyImageBot
This bot write user text in image using steganography algorithm by method *LSB (Least significant bit)*.

## Method LSB
The essence of the method LSB is to replace the least significant bit in each of the bytes of the RGB pixel with a bit of text. For example, we have the "mini-image" that contains 3 pixels (nested lists are RGB pixels):
> [ (255, 0, 255), (255, 0, 255), (255, 255, 255) ]

We need to hidden the character ***H*** in our "mini-image". Character ***H*** in ASCII-encoding equal **72**, in binary will be **01001000** (we must have *8 bits* in binary number because each a character in ASCII is byte). And now we take bit from character ***H*** and put in each "mini_image" byte:
- 255 -> "11111111" -> "11111110" -> 254
- 0 -> "00000000" -> "00000001" -> 1
- 255 -> "11111111" -> "11111110" -> 254
- 255 -> "11111111" -> "11111110" -> 254
- 0 -> "00000000" -> "00000001" -> 1
- 255 -> "11111111" -> "11111110" -> 254
- 255 -> "11111111" -> "11111110" -> 254
- 255 -> "11111111" -> "11111110" -> 254

And the output image will contains next pixels: [[254, 1, 254], [254, 1, 254], [254, 254, 255]]

Future plans:
- [ ] Optimize of create image with text (making this operation faster)
- [ ] Add of mixing text's bits
