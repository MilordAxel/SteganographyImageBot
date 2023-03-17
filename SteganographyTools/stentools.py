from SteganographyTools.exceptions import TextIsTooLong, TextLenghtIsBiggerSizeImage

def write_text_to_image(text, pixels):
    if len(text) > 255:
        raise TextIsTooLong("Lenght of text cannot be more than 255")
    
    # Create list of text's bits (every symbol of text must have 8 bit in binary)
    bitmask = []
    for symbol in text:
        bitmask_symbol = ["0" for i in range(8-len(bin(ord(symbol))[2:]))] + [bit for bit in bin(ord(symbol))[2:]]
        bitmask.extend(bitmask_symbol)
    
    # Create list of image's bytes from list of pixels (pixel contains 3 byte)
    pixel_bytes = []
    for pixel in pixels:
        pixel_bytes.extend(pixel)

    # Checking if the text can be in the given image
    if len(bitmask) > len(pixel_bytes):
        raise TextLenghtIsBiggerSizeImage("Count of text's bits more than count image's bytes")
    
    # Start write text's bits in image's bytes
    pixels_output = []
    for i, pxl_byte in enumerate(pixel_bytes):
        # When text's bits is over, write last pixels
        if i > len(bitmask)-1:
            pixels_output[-1].extend(pixel_bytes[i:3-len(pixels_output[-1])+i])     # filling in missing bytes in pixel
            for pixel in pixels[len(pixels_output):]: pixels_output.append(list(pixel))
            pixels_output[-1][-1] = len(text)       # Remembering of text lenght needed to reading from image
            break
        
        bin_byte = bin(pxl_byte)[2:-1] + bitmask[i]     # change last bit in image's byte
        
        # Create new pixel
        if i % 3 == 0: pixels_output.append([int(bin_byte, 2)])
        else: pixels_output[-1].append(int(bin_byte, 2))
    
    return pixels_output


def read_text_from_image(pixels):
    # Create list of image's bytes from list of pixels (pixel contains 3 byte)
    pixel_bytes = []
    for pixel in pixels:
        pixel_bytes.extend(pixel)
    
    bin_text = []
    text_len = pixel_bytes[-1]
    bits_in_text = text_len * 8
    for i, byte in enumerate(pixel_bytes[:bits_in_text]):
        # Create text bytes
        if i % 8 == 0: bin_text.append(bin(byte)[2:][-1])
        else: bin_text[-1] += bin(byte)[2:][-1]
    
    # Create text from image
    text = ""
    for bin_symbol in bin_text:
        text += chr(int(bin_symbol, 2))        
    return text


def get_all_pixels(image):
    all_pixels = []
    for y in range(image.height):
        for x in range(image.width):
            all_pixels.append(image.getpixel((x, y)))
    return all_pixels


def put_all_pixels(image, pixels):
    for y in range(image.height):
        for x in range(image.width):
            image.putpixel((x, y), tuple(pixels.pop(0)))
