#include "emoji_img.h"

#include <stdio.h>

int main() {

    EmojiImageManipulator* manip = emoji_img_create("../input.png");

    emoji_img_add_text(manip, "Hello 😀", 50, 50, "Sans", 30, "red");

    emoji_img_save(manip, "../output_c.png");

    emoji_img_destroy(manip);

    printf("C version done\n");

    return 0;

}