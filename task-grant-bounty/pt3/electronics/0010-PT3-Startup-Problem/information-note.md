# PT3 startup issue

# Status

`Valid`

`Revision History: V1`

`Replacement Log: None`

`Reference: PT3 Battery PCB Information Note`

# Project Description

## Overview

An issue was observed during the startup of the PT3 electronics when the SIYI telemetry unit and camera were connected to the power system. The flight controller (FC) would repeatedly reset during the power-up sequence. LEDs connected to the FC briefly turned off, indicating that the FC was rebooting in a loop. Consequently, it was not possible to establish a link to the FC via the SIYI telemetry unit.

# Methodology

Troubleshooting focused on the Battery PCB’s pre-charge circuitry. Measurements showed significant voltage drops on the power rails when the SIYI telemetry unit, camera, and the Hobbywing motors (which occasionally beep during startup) were powered through the pre-charge resistor network. The original design used three parallel resistors R15, R16, and R17 to form a 50 Ω pre-charge path. Under the added load, the voltage drop caused the Main PCB’s DC-DC converters to enter an undervoltage condition, resetting both the FC and telemetry module. By analyzing current consumption and voltage droop, it was determined that lowering the total pre-charge resistance would provide sufficient current during startup.

## Layout Description

The pre-charge resistor network on the Battery PCB (components R15, R16, R17) forms part of the soft-start path between the battery and main power bus. Originally, these three resistors were selected such that the equivalent resistance was 50 Ω. To increase current during startup, each resistor was replaced with a lower-value 50 Ω device (down from 150 Ω each), resulting in a total pre-charge resistance of 16.6 Ω (50 Ω/3 in parallel). No other layout changes were required.

## Circuit Operation

With the original 50 Ω pre-charge resistor, the inrush current available to power the overall system was limited. When the SIYI telemetry unit and camera drew their initial surge current, the voltage at the DC-DC inputs dropped below their operating threshold. This caused the regulators to reset, momentarily interrupting power to the FC. After replacing R15-R17 with lower-value resistors, the pre-charge circuit allowed more current flow during startup, reducing the voltage drop. The DC-DC converters remained within their input range, and the FC and telemetry unit booted normally without resets.

# Remarks

This change only affects the pre-charge resistor values; all other components remain as specified in the original Battery PCB design.
