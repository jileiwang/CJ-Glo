CC = gcc
#For older gcc, use -O3 or -O2 instead of -Ofast
CFLAGS = -lm -pthread -Ofast -march=native -funroll-loops -Wno-unused-result
BUILDDIR := build
SRCDIR := src

all: dir glove shuffle cooccur vocab_count bi_vocab_count bi_cooccur

dir :
	mkdir -p $(BUILDDIR)
glove : $(SRCDIR)/glove.c
	$(CC) $(SRCDIR)/glove.c -o $(BUILDDIR)/glove $(CFLAGS)
shuffle : $(SRCDIR)/shuffle.c
	$(CC) $(SRCDIR)/shuffle.c -o $(BUILDDIR)/shuffle $(CFLAGS)
cooccur : $(SRCDIR)/cooccur.c
	$(CC) $(SRCDIR)/cooccur.c -o $(BUILDDIR)/cooccur $(CFLAGS)
vocab_count : $(SRCDIR)/vocab_count.c
	$(CC) $(SRCDIR)/vocab_count.c -o $(BUILDDIR)/vocab_count $(CFLAGS)
bi_vocab_count : $(SRCDIR)/bi_vocab_count.c
	$(CC) $(SRCDIR)/bi_vocab_count.c -o $(BUILDDIR)/bi_vocab_count $(CFLAGS)
bi_cooccur : $(SRCDIR)/bi_cooccur.c
	$(CC) $(SRCDIR)/bi_cooccur.c $(SRCDIR)/hash_mapping_table.c -o $(BUILDDIR)/bi_cooccur $(CFLAGS)
	#$(CC) $(SRCDIR)/bi_cooccur.c $(SRCDIR)/bisearch_mapping_table.c -o $(BUILDDIR)/bi_cooccur $(CFLAGS)

clean:
	rm -rf glove shuffle cooccur vocab_count bi_vocab_count bi_cooccur build
