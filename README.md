# USBXpress version

This is an intermediate branch for Windows users that allows to use
original drivers as is. This makes it possible to use both original
software for the watch and this code without the need to reinstall
driver.

Note that you must place your original `SiUSBXp.dll` into e.g. `<path to this repo copy>\src\core\x86\` . `SiUSBXp.dll` version must match that of a driver. That is if you install latest driver from Silicon Labs (4.0 as of now), you'd have to use `SiUSBXp.dll` from the same kit. If you are using 64 bit Python, place a copy of 64 bit version of `SiUSBXp.dll` (from silab.com) to `<path to this repo copy>\src\core\x64\`.
