CC = gcc

CFLAGS = -Wall -Wextra -O3 -march=native -Ic/include `pkg-config --cflags cairo pangocairo`

LDFLAGS = `pkg-config --libs cairo pangocairo`

TARGET = libemoji_img.so

SRCS = emoji_img.c

OBJS = $(SRCS:.c=.o)

all: $(TARGET)

$(TARGET): $(OBJS)

	$(CC) -shared -o $@ $^ $(LDFLAGS)

%.o: %.c

	$(CC) $(CFLAGS) -c $< -o $@

clean:

	rm -f $(OBJS) $(TARGET)

.PHONY: all clean