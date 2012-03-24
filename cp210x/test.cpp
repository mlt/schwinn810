#include <windows.h>
#include <iostream>
#include "SiUSBXp.h"

using namespace std;

int main(int argc, char* argv[]) {
  DWORD hv,lv;
  int err = SI_GetDLLVersion(&hv, &lv);
  cout << "Hello" << err << endl;
  cout << "high=" << hv << " low=" << lv << endl;
  return 0;
}
