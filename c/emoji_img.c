#include "emoji_img.h"

#include <stdlib.h>

#include <string.h>

// Helper to parse color (enhanced with more colors)
void parse_color(const char* color_str, double* r, double* g, double* b) {
    if (strcmp(color_str, "red") == 0) { *r=1; *g=0; *b=0; }
    else if (strcmp(color_str, "black") == 0) { *r=0; *g=0; *b=0; }
    else if (strcmp(color_str, "white") == 0) { *r=1; *g=1; *b=1; }
    else if (strcmp(color_str, "blue") == 0) { *r=0; *g=0; *b=1; }
    else if (strcmp(color_str, "green") == 0) { *r=0; *g=0.5; *b=0; }
    else if (strcmp(color_str, "yellow") == 0) { *r=1; *g=1; *b=0; }
    else if (strcmp(color_str, "orange") == 0) { *r=1; *g=0.65; *b=0; }
    else if (strcmp(color_str, "purple") == 0) { *r=0.5; *g=0; *b=0.5; }
    else if (strcmp(color_str, "pink") == 0) { *r=1; *g=0.75; *b=0.8; }
    else if (strcmp(color_str, "gray") == 0) { *r=0.5; *g=0.5; *b=0.5; }
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

// Text with outline
void emoji_img_add_text_outlined(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* fill_color, const char* outline_color, double outline_width) {
    double fr, fg, fb, or, og, ob;
    parse_color(fill_color, &fr, &fg, &fb);
    parse_color(outline_color, &or, &og, &ob);

    PangoLayout *layout = pango_cairo_create_layout(manip->cr);
    pango_layout_set_text(layout, text, -1);
    
    PangoFontDescription *desc = pango_font_description_from_string(font_family);
    pango_font_description_set_size(desc, font_size * PANGO_SCALE);
    pango_layout_set_font_description(layout, desc);

    cairo_move_to(manip->cr, x, y);
    
    // Draw outline
    cairo_set_source_rgb(manip->cr, or, og, ob);
    cairo_set_line_width(manip->cr, outline_width);
    pango_cairo_layout_path(manip->cr, layout);
    cairo_stroke_preserve(manip->cr);
    
    // Fill text
    cairo_set_source_rgb(manip->cr, fr, fg, fb);
    cairo_fill(manip->cr);

    g_object_unref(layout);
    pango_font_description_free(desc);
}

// Text with gradient
void emoji_img_add_text_gradient(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* color1, const char* color2, int vertical) {
    double r1, g1, b1, r2, g2, b2;
    parse_color(color1, &r1, &g1, &b1);
    parse_color(color2, &r2, &g2, &b2);

    PangoLayout *layout = pango_cairo_create_layout(manip->cr);
    pango_layout_set_text(layout, text, -1);
    
    PangoFontDescription *desc = pango_font_description_from_string(font_family);
    pango_font_description_set_size(desc, font_size * PANGO_SCALE);
    pango_layout_set_font_description(layout, desc);

    // Get text extents for gradient
    PangoRectangle ink_rect, logical_rect;
    pango_layout_get_extents(layout, &ink_rect, &logical_rect);
    double width = logical_rect.width / (double)PANGO_SCALE;
    double height = logical_rect.height / (double)PANGO_SCALE;

    // Create gradient pattern
    cairo_pattern_t *pattern;
    if (vertical) {
        pattern = cairo_pattern_create_linear(0, y, 0, y + height);
    } else {
        pattern = cairo_pattern_create_linear(x, 0, x + width, 0);
    }
    cairo_pattern_add_color_stop_rgb(pattern, 0, r1, g1, b1);
    cairo_pattern_add_color_stop_rgb(pattern, 1, r2, g2, b2);

    cairo_move_to(manip->cr, x, y);
    cairo_set_source(manip->cr, pattern);
    pango_cairo_show_layout(manip->cr, layout);

    cairo_pattern_destroy(pattern);
    g_object_unref(layout);
    pango_font_description_free(desc);
}

// Text with shadow
void emoji_img_add_text_shadow(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* color, double shadow_x, double shadow_y, const char* shadow_color, double shadow_opacity) {
    double r, g, b, sr, sg, sb;
    parse_color(color, &r, &g, &b);
    parse_color(shadow_color, &sr, &sg, &sb);

    PangoLayout *layout = pango_cairo_create_layout(manip->cr);
    pango_layout_set_text(layout, text, -1);
    
    PangoFontDescription *desc = pango_font_description_from_string(font_family);
    pango_font_description_set_size(desc, font_size * PANGO_SCALE);
    pango_layout_set_font_description(layout, desc);

    // Draw shadow
    cairo_move_to(manip->cr, x + shadow_x, y + shadow_y);
    cairo_set_source_rgba(manip->cr, sr, sg, sb, shadow_opacity);
    pango_cairo_show_layout(manip->cr, layout);

    // Draw main text
    cairo_move_to(manip->cr, x, y);
    cairo_set_source_rgb(manip->cr, r, g, b);
    pango_cairo_show_layout(manip->cr, layout);

    g_object_unref(layout);
    pango_font_description_free(desc);
}

// TextBox with background and border
void emoji_img_add_textbox(EmojiImageManipulator* manip, const char* text, double x, double y, const char* font_family, double font_size, const char* text_color, const char* bg_color, double padding, const char* border_color, double border_width) {
    double tr, tg, tb, br, bg, bb, bdr, bdg, bdb;
    parse_color(text_color, &tr, &tg, &tb);
    parse_color(bg_color, &br, &bg, &bb);
    parse_color(border_color, &bdr, &bdg, &bdb);

    PangoLayout *layout = pango_cairo_create_layout(manip->cr);
    pango_layout_set_text(layout, text, -1);
    
    PangoFontDescription *desc = pango_font_description_from_string(font_family);
    pango_font_description_set_size(desc, font_size * PANGO_SCALE);
    pango_layout_set_font_description(layout, desc);

    // Get text extents
    PangoRectangle ink_rect, logical_rect;
    pango_layout_get_extents(layout, &ink_rect, &logical_rect);
    double width = logical_rect.width / (double)PANGO_SCALE;
    double height = logical_rect.height / (double)PANGO_SCALE;

    // Draw background
    cairo_set_source_rgb(manip->cr, br, bg, bb);
    cairo_rectangle(manip->cr, x - padding, y - padding, width + 2*padding, height + 2*padding);
    cairo_fill(manip->cr);

    // Draw border
    if (border_width > 0) {
        cairo_set_source_rgb(manip->cr, bdr, bdg, bdb);
        cairo_set_line_width(manip->cr, border_width);
        cairo_rectangle(manip->cr, x - padding, y - padding, width + 2*padding, height + 2*padding);
        cairo_stroke(manip->cr);
    }

    // Draw text
    cairo_move_to(manip->cr, x, y);
    cairo_set_source_rgb(manip->cr, tr, tg, tb);
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