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

// Advanced text functions
void emoji_img_add_text_outlined(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* fill_color, const char* outline_color, double outline_width);

void emoji_img_add_text_gradient(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* color1, const char* color2, int vertical);

void emoji_img_add_text_shadow(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* color, double shadow_x, double shadow_y, const char* shadow_color, double shadow_opacity);

void emoji_img_add_textbox(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* text_color, const char* bg_color, double padding, const char* border_color, double border_width);

void emoji_img_save(EmojiImageManipulator* manip, const char* output_path);

void emoji_img_destroy(EmojiImageManipulator* manip);

#endif