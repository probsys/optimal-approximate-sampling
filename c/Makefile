all: mainc mainc.opt test

SRC_C = flip.c main.c macros.c readio.c sample.c

mainc: $(SRC_C)
	gcc -pg -o mainc $^

mainc.opt: $(SRC_C)
	gcc -O3 -Wno-unused-result -o mainc.opt $^

.PHONY: clean
clean:
	rm -rf *.out *.gcno *.gcnh *.gcda *.gch mainc main.opt

# Test
.PHONY: test
test: mainc.opt
	./mainc.opt 1 1000000 ky.enc ./d.enc
