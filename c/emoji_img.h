#ifndef EMOJI_IMG_H

#define EMOJI_IMG_H

#include <cairo/cairo.h>

#include <pango/pangocairo.h>

// Struct for image manipulator

typedef struct {

    cairo_surface_t *surface;

    cairo_t *cr;

} EmojiImageManipulator;

// Functions

EmojiImageManipulator* emoji_img_create(const char* image_path);

// New: Create from raw data (for Pillow/imgrs integration)
// Data should be ARGB32 (premultiplied) or RGB24 depending on usage, but Cairo usually wants ARGB32 for alpha.
// Stride should be calculated by caller (usually width * 4 for ARGB32).
EmojiImageManipulator* emoji_img_create_from_data(unsigned char* data, int width, int height, int stride);

// New: Create empty image (native Cairo surface)
EmojiImageManipulator* emoji_img_create_empty(int width, int height);

void emoji_img_add_text(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* color);

void emoji_img_save(EmojiImageManipulator* manip, const char* output_path);

void emoji_img_destroy(EmojiImageManipulator* manip);

#endif