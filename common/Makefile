# 
#  Argus Software
#  Copyright (c) 2000-2012 QoSient, LLC
#  All rights reserved.
# 
#  QOSIENT, LLC DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS 
#  SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY 
#  AND FITNESS, IN NO EVENT SHALL QOSIENT, LLC BE LIABLE FOR ANY
#  SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER 
#  IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
#  ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
#  THIS SOFTWARE.
#
# Top level hierarchy

prefix = /usr/local
exec_prefix = ${prefix}
datarootdir = ${prefix}/share

# Pathname of directory to install the include files
INCLDEST = ${prefix}/include
# Pathname of directory to install the library
LIBDEST =  ${exec_prefix}/lib
# Pathname of directory to install the man page
MANDEST = ${datarootdir}/man

# VPATH
srcdir = .


#
# You shouldn't need to edit anything below.
#

CC = gcc
CCOPT = -O3
INCLS = -I$(srcdir) -I/usr/include -I$(srcdir)/../include  -I$(srcdir)/../argus
DEFS = -DHAVE_CONFIG_H

# Standard CFLAGS
CFLAGS = $(CCOPT) $(INCLS) $(DEFS)
LDFLAGS = 

INSTALL = /usr/bin/install -c
RANLIB = ranlib

#
# Flex and bison allow you to specify the prefixes of the global symbols
# used by the generated parser.  This allows programs to use lex/yacc
# and link against libpcap.  If you don't have flex or bison, get them.
#
LEX = flex -Pargus_
YACC = bison -y -p argus_

# Explicitly define compilation rule since SunOS 4's make doesn't like gcc.
# Also, gcc does not remove the .o before forking 'as', which can be a
# problem if you don't own the file but can write to the directory.
.c.o:
	@rm -f $@
	$(CC) $(CFLAGS) -c $<

# We would like to say "OBJ = $(SRC:.c=.o)" but Ultrix's make cannot
# hack the extra indirection


VSRC =  version.c
LSRC =  scanner.l
YSRC =  grammar.y
GENSRC = $(LSRC:.l=.c) $(YSRC:.y=.c)
GENHDR = tokdefs.h

TAGHDR = bpf/net/bpf.h

TAGFILES = $(SRC) $(HDR) $(TAGHDR)

LIBS = ../lib/argus_common.a 

OBJ =	$(COMMONOBJ) $(PARSEOBJ)
CLEANFILES = $(LIBS) $(OBJ) $(GENSRC) $(GENHDR) $(VSRC) lex.yy.c 

COMMONSRC = argus_util.c argus_code.c argus_filter.c $(GENSRC) $(VSRC)
COMMONOBJ = argus_util.o argus_code.o argus_filter.o grammar.o scanner.o version.o

SRC = $(COMMONSRC)

all: $(LIBS)

../lib/argus_common.a: $(COMMONOBJ)
	rm -f $@; ar qc $@ $(COMMONOBJ)
	-$(RANLIB) $@

scanner.c: scanner.l 
	@rm -f $@
	$(LEX) -t $< > $$$$.$@; mv $$$$.$@ $@
 
scanner.o: scanner.c tokdefs.h
tokdefs.h: grammar.c
grammar.c: grammar.y
	@rm -f grammar.c tokdefs.h
	$(YACC) -d $<
	mv y.tab.c grammar.c
	mv y.tab.h tokdefs.h
 
grammar.o: grammar.c
	$(CC) $(CFLAGS) -Dyylval=argus_lval -c grammar.c

version.o: version.c
version.c: $(srcdir)/../VERSION
	@rm -f $@
	sed -e 's/.*/char version[] = "&";/' $(srcdir)/../VERSION > $@

install: all force

uninstall: clean
clean:
	rm -f $(CLEANFILES)

distclean:
	rm -f $(CLEANFILES) Makefile config.cache config.log config.status \
	    gnuc.h os-proto.h bpf_filter.c net

tags: $(TAGFILES)
	ctags -wtd $(TAGFILES)

tar:	force
	@cwd=`pwd` ; dir=`basename $$cwd` ; name=libpcap-`cat VERSION` ; \
	    list="" ; tar="tar chFFf" ; \
	    for i in `cat FILES` ; do list="$$list $$name/$$i" ; done; \
	    echo \
	    "rm -f ../$$name; ln -s $$dir ../$$name" ; \
	     rm -f ../$$name; ln -s $$dir ../$$name ; \
	    echo \
	    "(cd .. ; $$tar - [lots of files]) | compress > /tmp/$$name.tar.Z" ; \
	     (cd .. ; $$tar - $$list) | compress > /tmp/$$name.tar.Z ; \
	    echo \
	    "rm -f ../$$name" ; \
	     rm -f ../$$name

force:	/tmp
depend:	$(GENSRC) $(VSRC) force
	../bin/mkdep -c $(CC) $(DEFS) $(INCLS) $(SRC)
