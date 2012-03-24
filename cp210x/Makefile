CC=i586-mingw32msvc-gcc
CXX=i586-mingw32msvc-g++
LD=i586-mingw32msvc-ld
DLLTOOL=i586-mingw32msvc-dlltool

all: SiUSBXp.dll test.exe libSiUSBXp.a

#CXXFLAGS=-DSI_USB_XP_EXPORTS
#-Wl,--output-def,my.def
# It is important to keep ordinals in def file
SiUSBXp.dll: proxy.o hexdump.o SiUSBXp.def
	$(CXX) -shared  -Wl,--enable-stdcall-fixup -o $@ $^ -L. -lSiUSBXp

# | libSiUSBXp.a # use this prereq only for direct linking tests
test.exe: test.o x86/SiUSBXp.lib
	$(CXX) -o $@ $^ 
# -L. -lsiusbxp # to link against renamed original
# x86/SiUSBXp.lib # to link against original name (proxy in fact)

libSiUSBXp.a: SiUSBXp_orig.def
	$(DLLTOOL) -d $^ -l $@ --kill-at
