#include <windows.h>
#include <shlobj.h>
#include <stdio.h>

FILE *file;

static void __attribute__((constructor))
your_lib_init(void)
{
  TCHAR path[MAX_PATH];
  HRESULT hr = SHGetFolderPath(NULL, CSIDL_PERSONAL, NULL, SHGFP_TYPE_CURRENT, path);
  strcat(path, "\\cp210.txt");
  printf("Logging into %s\n", path);
  file = fopen(path, "w");
}

static void __attribute__((destructor))
your_lib_destroy(void)
{
  fprintf(file, "Normal finish\n");
  fclose(file);
}
