#include <windows.h>
#include <stdio.h>
#include "hexdump.h"

/* make sure we use proper attributes */
#undef SI_USB_XP_EXPORTS
#include "SiUSBXp.h"

#undef SI_USB_XP_API
#define SI_USB_XP_API __declspec(dllexport)

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetDLLVersion(
  DWORD* HighVersion,
  DWORD* LowVersion
  )
{
  SI_STATUS err = SI_GetDLLVersion(HighVersion, LowVersion);
  printf("%X = SI_GetDLLVersion(&HighVersion, &LowVersion)\n", err);
  printf("HighVersion = %lX, LowVersion = %lX\n", *HighVersion, *LowVersion);
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetNumDevices() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetProductString() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_Close() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_Read() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_Write() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_DeviceIOControl() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_FlushBuffers() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_SetTimeouts() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetTimeouts() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_CheckRXQueue() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_SetBaudRate() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_SetBaudDivisor() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_SetLineControl() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_SetFlowControl() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetModemStatus() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_SetBreak() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_ReadLatch() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_WriteLatch() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetPartNumber() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetDeviceProductString() { return SI_SUCCESS; }
SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetDriverVersion() { return SI_SUCCESS; }

