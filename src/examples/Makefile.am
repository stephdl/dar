localedir = @localedir@

if BUILD_MODE32
  MYLIB=dar32
  AM_CPPFLAGS=-DLIBDAR_MODE=32 -I../libdar -DDAR_LOCALEDIR=\"$(localedir)\" $(GPGME_CFLAGS)
else
if BUILD_MODE64
    MYLIB=dar64
    AM_CPPFLAGS=-DLIBDAR_MODE=64 -I../libdar -DDAR_LOCALEDIR=\"$(localedir)\" $(GPGME_CFLAGS)
else
    MYLIB=dar
    AM_CPPFLAGS=-I../libdar -DDAR_LOCALEDIR=\"$(localedir)\" $(GPGME_CFLAGS)
endif
endif

noinst_PROGRAMS = factoriel prime formula
dist_noinst_DATA = README
LDADD = -L../libdar -l$(MYLIB) $(GPGME_LIBS)
AM_LDFLAGS = @LTLIBINTL@

factoriel_SOURCES = factoriel.cpp
factoriel_LDADD =  ../dar_suite/shell_interaction.o ../dar_suite/dar_suite.o ../dar_suite/line_tools.o $(LDADD)
factoriel_DEPENDENCIES = ../libdar/lib$(MYLIB).la ../dar_suite/shell_interaction.cpp ../dar_suite/dar_suite.cpp

prime_SOURCES = prime.cpp
prime_LDADD = ../dar_suite/shell_interaction.o ../dar_suite/dar_suite.o ../dar_suite/line_tools.o  $(LDADD)
prime_DEPENDENCIES = ../libdar/lib$(MYLIB).la ../dar_suite/shell_interaction.cpp ../dar_suite/dar_suite.cpp

formula_SOURCES = formula.cpp
formula_LDADD = ../dar_suite/shell_interaction.o ../dar_suite/dar_suite.o ../dar_suite/crit_action_cmd_line.o ../dar_suite/line_tools.o  $(LDADD)
formula_DEPENDENCIES = ../libdar/lib$(MYLIB).la ../dar_suite/line_tools.cpp ../dar_suite/shell_interaction.cpp ../dar_suite/crit_action_cmd_line.cpp ../dar_suite/dar_suite.cpp
