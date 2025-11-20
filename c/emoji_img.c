#include "emoji_img.h"

#include <stdlib.h>

#include <string.h>

// Helper to parse color

void parse_color(const char* color_str, double* r, double* g, double* b) {

    if (strcmp(color_str, "red") == 0) { *r=1; *g=0; *b=0; }

    else if (strcmp(color_str, "black") == 0) { *r=0; *g=0; *b=0; }

    else { *r=0; *g=0; *b=0; } // default black

}

EmojiImageManipulator* emoji_img_create(const char* image_path) {
    // Load image using Cairo (simplified, assume PNG)
    cairo_surface_t *image_surface = cairo_image_surface_create_from_png(image_path);
    cairo_t *cr = cairo_create(image_surface);

    EmojiImageManipulator* manip = malloc(sizeof(EmojiImageManipulator));
    manip->surface = image_surface;
    manip->cr = cr;
    return manip;
}

EmojiImageManipulator* emoji_img_create_from_data(unsigned char* data, int width, int height, int stride) {
    // Create surface from raw data
    // CAIRO_FORMAT_ARGB32 is the standard for Pillow 'RGBA' (after some swizzling if needed) or 'ARGB'.
    // Note: Cairo expects pre-multiplied alpha. Pillow uses straight alpha.
    // The python wrapper will handle the conversion if needed.
    cairo_surface_t *image_surface = cairo_image_surface_create_for_data(
        data,
        CAIRO_FORMAT_ARGB32,
        width,
        height,
        stride
    );
    
    cairo_t *cr = cairo_create(image_surface);

    EmojiImageManipulator* manip = malloc(sizeof(EmojiImageManipulator));
    manip->surface = image_surface;
    manip->cr = cr;
    return manip;
}

EmojiImageManipulator* emoji_img_create_empty(int width, int height) {
    cairo_surface_t *image_surface = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, width, height);
    cairo_t *cr = cairo_create(image_surface);

    EmojiImageManipulator* manip = malloc(sizeof(EmojiImageManipulator));
    manip->surface = image_surface;
    manip->cr = cr;
    return manip;
}

void emoji_img_add_text(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* color) {

    double r, g, b;

    parse_color(color, &r, &g, &b);

    cairo_set_source_rgb(manip->cr, r, g, b);

    PangoLayout *layout = pango_cairo_create_layout(manip->cr);

    pango_layout_set_text(layout, text, -1);

    PangoFontDescription *desc = pango_font_description_from_string(font_family);

    pango_font_description_set_size(desc, font_size * PANGO_SCALE);

    pango_layout_set_font_description(layout, desc);

    cairo_move_to(manip->cr, x, y);

    pango_cairo_show_layout(manip->cr, layout);

    g_object_unref(layout);

    pango_font_description_free(desc);

}

// Removed emoji_img_add_textbox as requested


void emoji_img_save(EmojiImageManipulator* manip, const char* output_path) {

    cairo_surface_write_to_png(manip->surface, output_path);

}

void emoji_img_destroy(EmojiImageManipulator* manip) {

    cairo_destroy(manip->cr);

    cairo_surface_destroy(manip->surface);

    free(manip);

}