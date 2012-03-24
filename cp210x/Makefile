CC=i586-mingw32msvc-gcc
CXX=i586-mingw32msvc-g++
LD=i586-mingw32msvc-ld
DLLTOOL=i586-mingw32msvc-dlltool
#DLLTOOL=dlltool


all: SiUSBXp.dll test.exe libSiUSBXp.a

CFLAGS=-D_WIN32_IE=0x0500

#-Wl,--output-def,my.def
# It is important to keep ordinals in def file
SiUSBXp.dll: proxy.o hexdump.o log.o SiUSBXp.def | libSiUSBXp.a
	$(CXX) -shared  -Wl,--enable-stdcall-fixup -o $@ $^ -L. -lSiUSBXp

# | libSiUSBXp.a # use this prereq only for direct linking tests
test.exe: test.o x86/SiUSBXp.lib
	$(CXX) -o $@ $^ 
# -L. -lsiusbxp # to link against renamed original
# x86/SiUSBXp.lib # to link against original name (proxy in fact)

libSiUSBXp.a: SiUSBXp_orig.def
	$(DLLTOOL) -d $^ -l $@ --kill-at
