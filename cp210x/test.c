#include <windows.h>
#include <stdio.h>
#include "SiUSBXp.h"

int main(int argc, char* argv[]) {
  DWORD ndev;
  int err = SI_GetNumDevices(&ndev);
  printf("You've got %d devices connected\n", ndev);
  return 0;
}
