import io
from PIL import Image


def compress_image(img_data, max_px_size, quality, webp_conversion):
    image = Image.open(io.BytesIO(img_data))
    w = float(image.size[0])
    h = float(image.size[1])
    if w < h:
        if w > max_px_size:
            new_w = max_px_size
            scale = max_px_size / w
            new_h = h * scale
        else:
            new_h = h
            new_w = w
    else:
        if h > max_px_size:
            new_h = max_px_size
            scale = max_px_size / h
            new_w = w * scale
        else:
            new_h = h
            new_w = w

    re_image = image.resize((int(new_w), int(new_h)), Image.Resampling.LANCZOS)
    buf = io.BytesIO()

    if webp_conversion is True:
        re_image.save(buf, format='webp', quality=quality)
    else:
        re_image.save(buf, format=image.format, quality=quality)

    return buf.getvalue()
