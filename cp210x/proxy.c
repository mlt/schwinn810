#include <windows.h>
#include <stdio.h>
#include "hexdump.h"

/* make sure we use proper attributes */
#undef SI_USB_XP_EXPORTS
#include "SiUSBXp.h"

#undef SI_USB_XP_API
#define SI_USB_XP_API __declspec(dllexport)

SI_USB_XP_API
SI_STATUS WINAPI proxySI_GetNumDevices(
	LPDWORD lpdwNumDevices
	)
{
  SI_STATUS err = SI_GetNumDevices(lpdwNumDevices);
  printf("%X = GetNumDevices(NumDevices=>%X\n", err, *lpdwNumDevices);
  return err;
}

SI_USB_XP_API
SI_STATUS WINAPI proxySI_GetProductString(
	DWORD dwDeviceNum,
	LPVOID lpvDeviceString,
	DWORD dwFlags
	)
{
  SI_STATUS err = SI_GetProductString(dwDeviceNum, lpvDeviceString, dwFlags);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS WINAPI proxySI_Open(
	DWORD dwDevice,
	HANDLE* cyHandle
	) 
{
  SI_STATUS err = SI_Open(dwDevice, cyHandle);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS WINAPI proxySI_Close(
	HANDLE cyHandle
	)
{
  SI_STATUS err = SI_Close(cyHandle);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS WINAPI proxySI_Read(
	HANDLE cyHandle,
	LPVOID lpBuffer,
	DWORD dwBytesToRead,
	LPDWORD lpdwBytesReturned,
	OVERLAPPED* o
	)
{
  SI_STATUS err = SI_Read(cyHandle, lpBuffer, dwBytesToRead, lpdwBytesReturned, o);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_Write(
	HANDLE cyHandle,
	LPVOID lpBuffer,
	DWORD dwBytesToWrite,
	LPDWORD lpdwBytesWritten,
	OVERLAPPED* o
	)
{
  SI_STATUS err = SI_Write(cyHandle, lpBuffer, dwBytesToWrite, lpdwBytesWritten, o);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_DeviceIOControl(
	HANDLE cyHandle,
	DWORD dwIoControlCode,
	LPVOID lpInBuffer,
	DWORD dwBytesToRead,
	LPVOID lpOutBuffer,
	DWORD dwBytesToWrite,
	LPDWORD lpdwBytesSucceeded
	)
{
  SI_STATUS err = SI_DeviceIOControl(cyHandle, dwIoControlCode, lpInBuffer, dwBytesToRead, lpOutBuffer, dwBytesToWrite, lpdwBytesSucceeded);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_FlushBuffers(
	HANDLE cyHandle, 
	BYTE FlushTransmit,
	BYTE FlushReceive
	)
{
  SI_STATUS err = SI_FlushBuffers(cyHandle, FlushTransmit, FlushReceive);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_SetTimeouts(
	DWORD dwReadTimeout,
	DWORD dwWriteTimeout
	)
{
  SI_STATUS err = SI_SetTimeouts(dwReadTimeout, dwWriteTimeout);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetTimeouts(
	LPDWORD lpdwReadTimeout,
	LPDWORD lpdwWriteTimeout
	)
{
  SI_STATUS err = SI_GetTimeouts(lpdwReadTimeout, lpdwWriteTimeout);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_CheckRXQueue(
	HANDLE cyHandle,
	LPDWORD lpdwNumBytesInQueue,
	LPDWORD lpdwQueueStatus
	)
{
  SI_STATUS err = SI_CheckRXQueue(cyHandle, lpdwNumBytesInQueue, lpdwQueueStatus);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS	WINAPI proxySI_SetBaudRate(
	HANDLE cyHandle,
	DWORD dwBaudRate
	)
{
  SI_STATUS err = SI_SetBaudRate(cyHandle, dwBaudRate);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS	WINAPI proxySI_SetBaudDivisor(
	HANDLE cyHandle,
	WORD wBaudDivisor
	)
{
  SI_STATUS err = SI_SetBaudDivisor(cyHandle, wBaudDivisor);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS	WINAPI proxySI_SetLineControl(
	HANDLE cyHandle, 
	WORD wLineControl
	)
{
  SI_STATUS err = SI_SetLineControl(cyHandle, wLineControl);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS	WINAPI proxySI_SetFlowControl(
	HANDLE cyHandle, 
	BYTE bCTS_MaskCode, 
	BYTE bRTS_MaskCode, 
	BYTE bDTR_MaskCode, 
	BYTE bDSR_MaskCode, 
	BYTE bDCD_MaskCode, 
	BOOL bFlowXonXoff
	)
{
  SI_STATUS err = SI_SetFlowControl(cyHandle, bCTS_MaskCode, bRTS_MaskCode, bDTR_MaskCode, bDSR_MaskCode, bDCD_MaskCode, bFlowXonXoff);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS WINAPI proxySI_GetModemStatus(
	HANDLE cyHandle, 
	PBYTE ModemStatus
	)
{
  SI_STATUS err = SI_GetModemStatus(cyHandle, ModemStatus);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS WINAPI proxySI_SetBreak(
	HANDLE cyHandle, 
	WORD wBreakState
	)
{
  SI_STATUS err = SI_SetBreak(cyHandle, wBreakState);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_ReadLatch(
	HANDLE cyHandle,
	LPBYTE	lpbLatch
	)
{
  SI_STATUS err = SI_ReadLatch(cyHandle, lpbLatch);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_WriteLatch(
	HANDLE cyHandle,
	BYTE	bMask,
	BYTE	bLatch
	)
{
  SI_STATUS err = SI_WriteLatch(cyHandle, bMask, bLatch);
  printf("\n");
  return err;
}

SI_USB_XP_API 
SI_STATUS WINAPI proxySI_GetPartNumber(
	HANDLE cyHandle,
	LPBYTE	lpbPartNum
	)
{
  SI_STATUS err = SI_GetPartNumber(cyHandle, lpbPartNum);
  printf("\n");
  return err;
}

SI_USB_XP_API
SI_STATUS WINAPI proxySI_GetDeviceProductString(	
	HANDLE	cyHandle,
	LPVOID	lpProduct,
	LPBYTE	lpbLength,
	BOOL	bConvertToASCII
	)
{
  SI_STATUS err = SI_GetDeviceProductString(cyHandle, lpProduct, lpbLength, bConvertToASCII);
  printf("%X = SI_GetDeviceProductString(cyHandle=%X, &Product, &Length=%X, bConvertToASCII=%d)\n", err, cyHandle, lpbLength, bConvertToASCII);
  printf("lpProduct:\n");
  hexdump(lpProduct, *lpbLength);
  return err;
}

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
SI_STATUS WINAPI proxySI_GetDriverVersion(
	DWORD* HighVersion,
	DWORD* LowVersion
	)
{
  SI_STATUS err = SI_GetDriverVersion(HighVersion, LowVersion);
  printf("%X = SI_GetDriverVersion(&HighVersion, &LowVersion)\n", err);
  printf("HighVersion = %lX, LowVersion = %lX\n", *HighVersion, *LowVersion);
  return err;
}



/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetDLLVersion( */
/*   DWORD* HighVersion, */
/*   DWORD* LowVersion */
/*   ) */

/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetNumDevices() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetProductString() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_Close() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_Read() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_Write() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_DeviceIOControl() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_FlushBuffers() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_SetTimeouts() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetTimeouts() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_CheckRXQueue() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_SetBaudRate() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_SetBaudDivisor() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_SetLineControl() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_SetFlowControl() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetModemStatus() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_SetBreak() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_ReadLatch() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_WriteLatch() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetPartNumber() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetDeviceProductString() { return SI_SUCCESS; } */
/* SI_USB_XP_API  */
/* SI_STATUS WINAPI proxySI_GetDriverVersion() { return SI_SUCCESS; } */

