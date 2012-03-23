Imports System
Imports System.Collections.Generic
Imports System.Text
Imports System.Runtime.InteropServices

Module SIUSBXP
    ' Return codes
    Public Const SI_SUCCESS As Byte = &H00
    Public Const SI_DEVICE_NOT_FOUND As Byte = &HFF
    Public Const SI_INVALID_HANDLE As Byte = &H01
    Public Const SI_READ_ERROR As Byte = &H02
    Public Const SI_RX_QUEUE_NOT_READY As Byte = &H03
    Public Const SI_WRITE_ERROR As Byte = &H04
    Public Const SI_RESET_ERROR As Byte = &H05
    Public Const SI_INVALID_PARAMETER As Byte = &H06
    Public Const SI_INVALID_REQUEST_LENGTH As Byte = &H07
    Public Const SI_DEVICE_IO_FAILED As Byte = &H08
    Public Const SI_INVALID_BAUDRATE As Byte = &H09
    Public Const SI_FUNCTION_NOT_SUPPORTED As Byte = &H0a
    Public Const SI_GLOBAL_DATA_ERROR As Byte = &H0b
    Public Const SI_SYSTEM_ERROR_CODE As Byte = &H0c
    Public Const SI_READ_TIMED_OUT As Byte = &H0d
    Public Const SI_WRITE_TIMED_OUT As Byte = &H0e
    Public Const SI_IO_PENDING As Byte = &H0f

    ' GetProductString() function flags
    Public Const SI_RETURN_SERIAL_NUMBER As Byte = &H00
    Public Const SI_RETURN_DESCRIPTION As Byte = &H01
    Public Const SI_RETURN_LINK_NAME As Byte = &H02
    Public Const SI_RETURN_VID As Byte = &H03
    Public Const SI_RETURN_PID As Byte = &H04

    ' RX Queue status flags
    Public Const SI_RX_NO_OVERRUN As Byte = &H00
    Public Const SI_RX_EMPTY As Byte = &H00
    Public Const SI_RX_OVERRUN As Byte = &H01
    Public Const SI_RX_READY As Byte = &H02

    ' Buffer size limits
    Public Const SI_MAX_DEVICE_STRLEN As Integer = 256
    Public Const SI_MAX_READ_SIZE As Integer = 4096 * 16
    Public Const SI_MAX_WRITE_SIZE As Integer = 4096

    ' Type definitions

    ' Input and Output pin Characteristics
    Public Const SI_HELD_INACTIVE As Byte = &H00
    Public Const SI_HELD_ACTIVE As Byte = &H01
    Public Const SI_FIRMWARE_CONTROLLED As Byte = &H02
    Public Const SI_RECEIVE_FLOW_CONTROL As Byte = &H02
    Public Const SI_TRANSMIT_ACTIVE_SIGNAL As Byte = &H03
    Public Const SI_STATUS_INPUT As Byte = &H00
    Public Const SI_HANDSHAKE_LINE As Byte = &H01

    ' Mask and Latch value bit definitions
    Public Const SI_GPIO_0 As Byte = &H01
    Public Const SI_GPIO_1 As Byte = &H02
    Public Const SI_GPIO_2 As Byte = &H04
    Public Const SI_GPIO_3 As Byte = &H08

    ' GetDeviceVersion() return codes
    Public Const SI_CP2101_VERSION As Byte = &H01
    Public Const SI_CP2102_VERSION As Byte = &H02
    Public Const SI_CP2103_VERSION As Byte = &H03
    Public Const SI_CP2104_VERSION As Byte = &H04

    Public Declare Function SI_GetNumDevices Lib "SiUSBXp.dll" (
    ByRef lpdwNumDevices As UInteger
    ) As Integer

    Public Declare Function SI_GetProductString Lib "SiUSBXp.dll" (
    dwDeviceNum As UInteger,
    lpvDeviceString As StringBuilder,
    dwFlags As UInteger
    ) As Integer

    Public Declare Function SI_Open Lib "SiUSBXp.dll" (
    dwDevice As UInteger,
    ByRef cyHandle As IntPtr
    ) As Integer

    Public Declare Function SI_Close Lib "SiUSBXp.dll" (
    cyHandle As IntPtr
    ) As Integer

    Public Declare Function SI_Read Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    lpBuffer() As Byte,
    dwBytesToRead As UInteger,
    ByRef lpdwBytesReturned As UInteger,
    o As IntPtr
    ) As Integer

    Public Declare Function SI_Write Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    lpBuffer() As Byte,
    dwBytesToWrite As UInteger,
    ByRef lpdwBytesWritten As UInteger,
    o As IntPtr
    ) As Integer

    Public Declare Function SI_DeviceIOControl Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    dwIoControlCode As UInteger,
    lpInBuffer() As Byte,
    dwBytesToRead As UInteger,
    lpOutBuffer() As Byte,
    dwBytesToWrite As UInteger,
    ByRef lpdwBytesSucceeded As UInteger
    ) As Integer

    Public Declare Function SI_FlushBuffers Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    FlushTransmit As Byte,
    FlushReceive As Byte
    ) As Integer

    Public Declare Function SI_SetTimeouts Lib "SiUSBXp.dll" (
    dwReadTimeout As UInteger,
    dwWriteTimeout As UInteger
    ) As Integer

    Public Declare Function SI_GetTimeouts Lib "SiUSBXp.dll" (
    ByRef lpdwReadTimeout As UInteger,
    ByRef lpdwWriteTimeout As UInteger
    ) As Integer

    Public Declare Function SI_CheckRXQueue Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    ByRef lpdwNumBytesInQueue As UInteger,
    ByRef lpdwQueueStatus As UInteger
    ) As Integer

    Public Declare Function SI_SetBaudRate Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    dwBaudRate As UInteger
    ) As Integer

    Public Declare Function SI_SetBaudDivisor Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    wBaudDivisor As UShort
    ) As Integer

    Public Declare Function SI_SetLineControl Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    wLineControl As UShort
    ) As Integer

    Public Declare Function SI_SetFlowControl Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    bCTS_MaskCode As Byte,
    bRTS_MaskCode As Byte,
    bDTR_MaskCode As Byte,
    bDSR_MaskCode As Byte,
    bDCD_MaskCode As Byte,
    bFlowXonXoff As Boolean
    ) As Integer

    Public Declare Function SI_GetModemStatus Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    ByRef ModemStatus As Byte
    ) As Integer

    Public Declare Function SI_SetBreak Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    wBreakState As UShort
    ) As Integer

    Public Declare Function SI_ReadLatch Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    ByRef lpbLatch As Byte
    ) As Integer

    Public Declare Function SI_WriteLatch Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    bMask As Byte,
    bLatch As Byte
    ) As Integer

    Public Declare Function SI_GetPartNumber Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    ByRef lpbPartNum As Byte
    ) As Integer

    Public Declare Function SI_GetDeviceProductString Lib "SiUSBXp.dll" (
    cyHandle As IntPtr,
    lpProduct() As Byte,
    ByRef lpbLength As Byte,
    bConvertToASCII As Boolean
    ) As Integer

    Public Declare Function SI_GetDLLVersion Lib "SiUSBXp.dll" (
    ByRef HighVersion As UInteger,
    ByRef LowVersion As UInteger
    ) As Integer

    Public Declare Function SI_GetDriverVersion Lib "SiUSBXp.dll" (
    ByRef HighVersion As UInteger,
    ByRef LowVersion As UInteger
    ) As Integer
End Module
