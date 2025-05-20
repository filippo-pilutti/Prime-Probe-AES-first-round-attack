#!/usr/bin/env python3
import os
from PIL import Image

# A4 size at 150 DPI: 210mm x 297mm -> approximately 1240 x 1753 pixels
PAGE_WIDTH_PX = int(8.27 * 150)   # ≈1240
PAGE_HEIGHT_PX = int(11.69 * 150) # ≈1753

# Grid layout for portrait A4: 2 columns × 4 rows = 8 images per page
COLS = 2
ROWS = 4
IMAGES_PER_PAGE = COLS * ROWS
DPI = (150, 150)


def generate_heatmap_pdf(input_dir="heatmaps", output_pdf="heatmaps.pdf"):
    # load all 16 images
    imgs = []
    for i in range(16):
        path = os.path.join(input_dir, f"byte_{i}.png")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Missing heatmap image: {path}")
        img = Image.open(path).convert("RGB")
        imgs.append(img)

    # compute target cell size
    cell_w = PAGE_WIDTH_PX // COLS
    cell_h = PAGE_HEIGHT_PX // ROWS

    pages = []
    total_pages = (len(imgs) + IMAGES_PER_PAGE - 1) // IMAGES_PER_PAGE

    for p in range(total_pages):
        # create a blank A4 canvas
        page = Image.new("RGB", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), color="white")
        for idx in range(IMAGES_PER_PAGE):
            img_idx = p * IMAGES_PER_PAGE + idx
            if img_idx >= len(imgs):
                break
            img = imgs[img_idx]
            # resize to fit cell while preserving aspect ratio
            # use LANCZOS resampling (ANTIALIAS deprecated)
            img.thumbnail((cell_w, cell_h), resample=Image.LANCZOS)
            # compute paste position (centered in cell)
            row = idx // COLS
            col = idx % COLS
            x_offset = col * cell_w + (cell_w - img.width) // 2
            y_offset = row * cell_h + (cell_h - img.height) // 2
            page.paste(img, (x_offset, y_offset))
        pages.append(page)

    # save as multi-page PDF with A4 dimensions
    pages[0].save(
        output_pdf,
        save_all=True,
        append_images=pages[1:],
        dpi=DPI,
    )
    print(f"Generated {output_pdf} ({total_pages} pages) in A4 portrait format.")


if __name__ == "__main__":
    generate_heatmap_pdf()
