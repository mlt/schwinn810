# About #

There are cheap sport watches out there, however the software is limited to MS Windows and is quite ugly.

## Idea ##

All looks like [USBXpress Development Tools][http://www.silabs.com/products/mcu/Pages/USBXpress.aspx) from Silicon Labs was used to communicate via USB-UART bridge cp210x.

It seems feasible to write a proxy and transcribe all communication between the software on Windows host and device behind USB-UART bridge.

## Goal ##

At this point one should not expect an exact copy of software for other OSes. The first goal is to code proxy and transcribe communication making it possible for others to develop software independently.