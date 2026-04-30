# Pilot Handbook
Quiver Dev-Kit
Heavy-Lift Multipurpose UAV (<25 kg MTOW)

<!-- Table of content -->
<!-- [toc] -->

## 1. Safety & Compliance

### 1.1 General Safety Principles
The Quiver Dev-Kit is a battery powered heavy-lift quadcopter (MTOW ~25kg). It is engineered for industrial aerial applications. It is **not** designed for the deployment of munitions/explosives, or critical life-support transport.

> [!CAUTION]  
>
> Any improper or reckless action can result in:
> 
> - Immediate fatality or severe permanent injury.
> - Electrical or metal fire hazards (Class C & D).
> - Property damage.
> - False public alert, panic or unnecessary crowds.
> - Noise pollution or disruptions.
> - Legal liability and reputational damage.

All operators must be trained and familiar with the aircraft and local aviation regulations. The Pilot in Command (PIC) must remain alert and strictly adhere to the **IMSAFE** protocol (Illness, Medication, Stress, Alcohol, Fatigue, Emotion) before operations.

### 1.2 Operational Limits
#### 1.2.1 Weather Conditions
**Wind Speed**:
Maximum sustained wind speed is 15 knots (approx. 28 km/h) and wind gusts up to 18 kts (approx. 33 km/h). Gusts exceeding this limit may compromise stability.

**Solar Activity**:
Monitor Kp Index and UV Intensity via pre-flight forecast. High UV indices can degrade composite materials over time, and high Kp (>4) can interfere with GNSS reliability.

**Precipitation**:
While the fuselage features some water-resistant seals, flight in rain, snow, or hail is prohibited for the Dev-Kit drone.

**Temperature**:
Ambient Air: Operating range is -10°C to +35°C.
Battery Temp: Do not operate if battery core temperature exceeds 56 °C. Land immediately if this threshold is reached.
      
#### 1.2.2 Visual Line of Sight (VLOS):
The Pilot in Command (PIC) must maintain effective Visual Line of Sight at all times, unaided by binoculars or FPV goggles.

Regulatory References:

- EU (EASA): Operations must comply with Open Category A3 requirements (fly far from people) unless a Specific Category authorization (SORA/PDRA) is held.
- USA (FAA): Operations must comply with 14 CFR Part 107.31 (Visual Line of Sight Aircraft Operation).

#### 1.2.3 Airspace Restrictions:
- EU: Consult national geographical zones (e.g., dipul in Germany, Geoportal in France).
- USA: Use B4UFLY or FAA DroneZone to verify airspace authorization (LAANC).

#### 1.2.4 EASA & FAA Specifics (Weight Class <25 kg):
**EU (EASA)**:

Open Category A3, C3 class drone:
You may fly without a SORA if you maintain a minimum horizontal distance of 150 m from residential, commercial, industrial, or recreational areas and ensure no uninvolved people are endangered.

Specific Category:
If your mission requires flying closer than 150 m to populated areas or over people, you must obtain an operational authorization based on a SORA (Specific Operations Risk Assessment) or PDRA.

**USA (FAA)**:

You must hold a Remote Pilot Certificate (Part 107).

The aircraft must be registered with the FAA.

The aircraft must broadcast a RemoteID signal while in flight. 

Operations over human beings are prohibited unless complying with remote ID and kinetic energy limitations, which this aircraft (25 kg) generally exceeds without a specific waiver.

**Geo-Fencing**:

The pilot must establish a local geo-fence for every flight.

Setup: Configure the FENCE_RADIUS and FENCE_ALT_MAX in the ground station software to contain the drone within the authorized flight volume.

> [!WARNING]  
> 
> Geo-fencing relies on minimum GNSS. It may not function during a navigation system error or location source failure.

**Experimental Systems Disclaimer**:

Radar & LiDAR Altimeters: These sensors are currently integrated for testing purposes only.

Do not rely on these sensors for critical flight phases. The pilot must verify altitude visually and via barometric telemetry.

These systems may be activated for controlled testing only when there is zero risk to third parties, animals, or infrastructure.

**Instructions on how to find local regulations**:
...

### 1.3 Electrical Warning

#### 1.3.1 Arcing & Spark Risk
The electrical system is designed to be spark-free during connection via a pre-charge circuit.

> [!WARNING]  
> 
> If you observe any visible spark or audible "crack" when connecting the battery :
> - STOP immediately.
> - Disconnect and contact support.
> - Do not fly.
> 
> This indicates a failure in the pre-charge circuit or a short in the power system.

#### 1.3.2 Flight Battery Handling
**General Principles：**

> [!NOTE] 
> 
> The following principles apply to both battery and charger.

- Use only Tattu 3.5 or 4.0 14S Smart LiHV batteries.
- Use the official Tattu-supported charger compatible with 14S LiHV chemistry or SkyRC equivalent.
- Never short or ground the battery main connector even in non-operating condition.
- Minimize the unnecessary plug-and-unplug cycles to extend power connector life.
- Always check power connector cleanliness and dryness.
- Always keep a Class D fire extinguisher nearby (additional fire blanket are recommended).

**Charging:**
 
- Charge only in a designated dry, fire-resistant area (e.g., concrete floor), away from living quarters or flammable materials.
- Never charge a battery that significantly warmer than human body temperature or right after a fully-discharge flight. Allow it to cool down for 15 ~ 30 minutes before apply a charging current.

**Transport & Storage:**

- If the battery will not be used for next 14 Days, discharge it to storage voltage (3.80V per cell / approx. 50-60% capacity).
- Any battery dropped from any height > 50 cm is unsafe for flight. Internal damage is invisible and can cause unpredictable power outage or fires.
- Water vapor may condense on the battery surface when transferring from cold to hot environments. Allow it to acclimate and dry completely before connecting.

**In-Flight Emergency:**

> [!WARNING] 
> 
> To prevent escalating a failure, minimize aggressive maneuvers during any battery system emergency.
> - If battery temperature exceeds **56°C**, land immediately.
> - If voltage sags rapidly, oscillates abnormally, or stops updating, land immediately.

**Battery Fire Emergency**:

> [!CAUTION] 
> 
> In case of pungent gas, irregular popping sounds or smoke, **IMMEDIATELY:**
> - **Disconnect** the battery immediately (if safe to do so).
> - **Evacuate** the battery to an open outdoor area away from flammable materials (do not leave it in a corridor).
> - **Observe** from at least 15 meters away with a Class D fire extinguisher ready.

> [!CAUTION] 
> 
> In case of an **ACTIVE BATTERY FIRE** indoors:
> - **Evacuate** all personnel, order them to call emergency department as "Battery Fire".
> - **Cover** the battery with a fire blanket if the condition is still safe.
> - **Remove** proximate flammable objects as possible.
> - **Cut off** the main power supply.
> - **Exit** to an open area.

### 1.4 Establishing Safety Zones (Kinetic Energy)

The drone generates significant kinetic energy during flight. A free-fall impact from operational altitude carries lethal force, capable of penetrating vehicle roofs or causing fatal injury. Therefore, establishing a correct safety zone is the single most critical pre-flight step.

**Official Guidelines as Primary Source**
The Pilot in Command (PIC) must strictly adhere to the safety distances mandated by the local aviation authority. These regulations take precedence over any manufacturer recommendations:

- **EU (EASA)**: Operations fall under the Open Category A3. You must maintain a horizontal distance of at least 150 meters from residential, commercial, industrial, or recreational areas. You must never fly over uninvolved persons.

- **USA (FAA)**: Operations under Part 107 generally prohibit flight over human beings for drones of this weight class (Category 3/4) without a specific Declaration of Compliance or Waiver, due to the kinetic energy exceeding 25 ft-lbs limit.

**Operational Safety Zone Calculation (Ground Risk Buffer)**
To ensure no harm can come to any person or animal in the event of a complete power failure (ballistic fall), the pilot must establish a **Ground Risk Buffer**. This buffer extends beyond the intended flight path.

A widely accepted safety standard for rotary-wing aircraft is the 1:1 Rule:

> [!NOTE] 
> 
> Minimum Safety Buffer = Flight Altitude (AGL)

- **Example**: If flying at 50 meters (164 ft) altitude, you must ensure a clear zone of at least 50 meters horizontally from your flight path where no uninvolved persons are present.

- **Why?** If the drone loses power while moving at speed, momentum will carry it forward as it falls. The 1:1 rule provides a simplified safety margin to contain this ballistic trajectory.

**Implementation Steps**:

1. **Identify the Operational Volume**: Define the exact area where the drone will fly.

2. **Add the Buffer**: Extend this area by a distance equal to your maximum planned altitude (the 1:1 rule).

3. **Verify the Ground**: Ensure this entire extended zone is clear of non-participants, animals, and critical infrastructure.

4. **Geo-Fence**: Program the flight controller's Geo-Fence to prevent the drone from exiting the Operational Volume, ensuring that even if it hits the "virtual wall" and falls, it remains within the Ground Risk Buffer.

## 2. System Setup
### 2.1 Unbox and assemble
> [!TIP] 
> 
> Due to the large size of the aircraft, a two-person lift or assistance is recommended for assembly.

> [!WARNING] 
> 
> Be aware of pinch and cut.
> 
> Unlocked folding motor arms will rotate while horizontal force or unwise handling technique being applied.

**1. Preparation:**
- Reserve enough working space for transport case, devices and the aircraft assembly.

**2. Extraction:** 
- Lift the aircraft by the central aluminum airframe with symmetrical handling. 
- Never lift by the avionics lid, plastic or 3D-printed parts.

**3. Landing gear assembly:**
- Steadily holding the aircraft.
- Fully insert the detached landing gear tube into the quick-release joint. 
- Rest the aircraft on flat surface.
- Fully tighten the quick-release screw.
- Confirm the installation by applying a light pull on the landing gear component.

**4. Extend motor arms**
- Check the contact section of arm folder for any obstacles.
- Unfold and fully align one motor
- Rotate and fully engage the lock handle.
- Visually verify the locking mechanism is engaged and immobile.
- Repeat steps above for all remaining motor arms.

**5. Antenna assembly:**
- Unfold and extend both antenna to upright.
- Check and tighten antenna connector.
- Rotate and adjust the antennas to a heading where they do not face each other.

**6. Gimbal camera assembly:**
- Check the integrity of cables, connectors and rubber damper balls.
- Remove any camera protection or locking mechanism before power up.
- Check for dust and debris at lens and gimbal motor gaps and apply proper cleaning.

### 2.2 Installing battery
> [!NOTE] 
> 
> Acknowledge the "Flight Battery Handling" chapter before handling the battery.

> [!WARNING] 
> 
> During the following steps:
> - Do not power on the battery.
> - Do not press the battery power button right after the installation.

1. Align the battery to the 3D-printed guide rails with the connector side up. 
2. Insert the battery by sliding it into the aluminum chassis.
3. Secure the mechanical latch and check the lock position.
4. Confirm the battery is locked in place by applying a light pull on the lift handle.

### 2.3 Battery power button 

**For Tattu 3.5 series:**
- There is always voltage present at the battery terminals. The 3.5 Tattu smart batteries do not offer the function to control the battery power output.
- The power button can be used to display the charging state or to awake the internal CAN bus communication of the battery.

**For Tattu 4.0 series:**
- The power button can be used to control the battery power up state. The output needs to be activated before the push button on the drone can power up the drone.

### 2.4 Drone push button
The drone push button is used to initiate the pre-charge of the power system and to power up all low voltage systems, such as:
- Flight controller computer
- Telemetry
- Gimbal camera
- Payload power supply
- ...

After the flight controller boots, the Quiver SSR auto-engage Lua script shall automatically activate Relay 1 and close the high-voltage SSR / main power MOSFETs. This removes the normal need for the pilot to manually toggle Relay 1 before flight.

> [!WARNING]
>
> The auto-engage Lua script must be installed and enabled on the aircraft before operation. If Relay 1 / SSR does not activate automatically after boot, do not assume the aircraft is ready for flight. Troubleshoot the script or relay state before arming.

> [!CAUTION]
>
> If Relay 1 / SSR is intentionally or accidentally deactivated while the aircraft is powered, keep the avionics PCB temperature under observation. The pre-charge resistor is not intended to carry sustained aircraft load, and overheating risk increases with higher power consumption from equipment such as companion computers or powered attachments.

### 2.5 1st time setup
Each Quiver Dev-Kit aircraft is shipped with a validated firmware image, pre-loaded baseline parameters, and completed sensor calibrations performed by the manufacturer prior to shipment.

The purpose of the first-time setup is verification, not configuration.

The pilot shall not modify firmware, parameters, or calibrations during initial setup unless explicitly instructed by the Quiver team. The pilot’s responsibility is to confirm that the aircraft state matches the documented baseline before first flight.

#### 2.5.1 Firmware and Configuration Baseline (Verification Only)

Before the first flight, the pilot must verify that:

- The flight controller firmware version matches the version declared in the delivery documentation.
- The official Quiver baseline parameter set is present and unchanged.
- Frame configuration, motor order, and motor rotation direction match the documented airframe layout.
- Battery monitor type, voltage scaling, and current sensing values match the baseline.
- All failsafe behaviors are enabled and match the baseline configuration.

No parameters shall be altered at this stage.  
Any discrepancy between the expected baseline and the aircraft state must be reported to the Quiver team before flight.

#### 2.5.2 Mandatory Calibrations (Verification)

The following calibrations are completed by the manufacturer prior to shipment and shall only be verified by the pilot:

- Accelerometer calibration
- Compass calibration (including interference check)
- RC input calibration
- Level / horizon verification

If RTK positioning is used, verify correct GPS role assignment and correction data flow.

Re-calibration shall only be performed if:
- Hardware has been replaced or repositioned, or
- Explicitly requested by the Quiver team.

#### 2.5.3 Safety, Arming, and Logging Verification

Before flight, verify that:

- All arming checks are enabled.
- Geo-fencing is enabled and configured for the current test site.
- RTL altitude is appropriate for the operating environment.
- Battery failsafe thresholds are correct.
- The kill switch is mapped and verified with motors disabled or propellers removed.
- Onboard logging is enabled and an SD card is installed.

Flight without logging is not permitted.

#### 2.5.4 First-Flight Authorization

The aircraft is considered authorized for first flight only when:

- All verification steps above are completed,
- No unexplained warnings or errors are present,
- Logging is confirmed active,
- No unauthorized configuration changes exist.

### 2.6 Parameter walk through
This section introduces flight-critical parameters that the pilot must understand, not modify.

#### 2.6.1 Parameter Modification Policy

The Quiver Dev-Kit is delivered with a locked, flight-validated configuration.

- Flight-critical parameters shall not be modified by default.
- Parameter changes may be permitted only after:
  - Accumulating sufficient flight hours on the platform,
  - Demonstrated pilot experience,
  - Explicit approval from the Quiver team.

Any request to modify flight-critical parameters must be submitted and approved before changes are applied.

Unauthorized parameter changes may invalidate:
- Manufacturer support,
- Flight test data,
- Continued participation in the Dev-Kit program.

#### 2.6.2 Parameters the Pilot Must Understand

> [!TIP]
>
> The official baseline parameter file can be downloaded from:  
> https://github.com/Arrow-air/project-quiver/tree/vector/firmware-docs-clean/docs/firmware/parameters

**Geo-Fence**
- `FENCE_ENABLE`
- `FENCE_RADIUS`
- `FENCE_ALT_MAX`

Pilots must understand the configured response when the fence is breached (Brake / RTL / Land).

**Battery Failsafes**
- Battery monitor configuration (`BATT_*`)
- Low and critical battery thresholds and actions (`FS_BATT_*`)

**RC and GCS Failsafes**
- RC signal loss behavior
- Telemetry/GCS loss behavior

**Return-to-Launch**
- RTL altitude
- RTL speed (if configured)
- Home position requirements

**Logging**
- Log bitmask
- Storage availability

#### 2.6.3 Approved Parameter Changes

When parameter modification is explicitly authorized:

- Only the approved parameters may be changed.
- All changes must be recorded in the flight tracking platform maintenance log, including:
  - Date
  - Parameter name(s)
  - Old and new values
  - Reason for change
  - Affected flight(s)


### 2.7 RC setup
The RC system is the pilot’s primary safety interface. All Dev-Kit aircraft shall conform to the following requirements.

#### 2.7.1 Required RC Functions

The following pilot-accessible controls are mandatory:

- Arm / Disarm
- Flight Mode selector (3-position)  
  *(Typical: LOITER / AUTO / STABILIZE)*
- Return-to-Launch (RTL)
- Kill Switch (guarded or deliberately positioned)

Optional but recommended:
- Mission pause / skip
- Payload or camera controls

#### 2.7.2 RC Calibration and Verification

- Perform RC calibration in the ground control station.
- No trims or sub-trims shall be applied.
- Verify correct channel directions.
- Verify each switch produces the intended function and mode.

#### 2.7.3 RC Failsafe Behavior

The pilot must understand:
- The aircraft response to RC signal loss,
- The recovery behavior when RC signal is restored.

#### 2.7.4 Pre-Flight RC Verification

Before arming, confirm:
- Flight mode switch positions,
- Arm/disarm switch orientation,
- Kill switch location and protection against accidental activation.

### 2.8 GCS setup

Mission Planner is the primary supported ground control station for Quiver Dev-Kit operations.

#### 2.8.1 Pilot Station Setup

- Laptop connected to stable power,
- Telemetry radio securely connected,
- Optional external monitor for camera or payload feed (recommended).

If telemetry connection fails, power-cycle the radio and retry.

#### 2.8.2 Mission Planner Connection

1. Launch Mission Planner.
2. Select the correct COM port (or Auto).
3. Set the baud rate to 57600 (default for SiK telemetry radios).
4. Connect and verify:
   - Live telemetry updates,
   - No critical system messages,
   - Stable estimator (EKF) status.

#### 2.8.3 RTK / Correction Data (If Used)

If RTK positioning is employed:
- Verify base station configuration,
- Confirm RTCM correction messages are received,
- Inject corrections via Mission Planner as configured.

#### 2.8.4 Camera / SIYI Setup 

- Verify camera power and data connections,
- Confirm video feed before arming,
- Verify camera control response.

#### 2.8.5 Mission Planner Servo/Relay Page

The Mission Planner **Servo/Relay** page is used to verify and manually control relay outputs during setup, troubleshooting, and payload operations.

Before flight, set the relay labels in Mission Planner so the operator can identify each function quickly:

| Relay | Label | Function | Normal use |
| - | - | - | - |
| 1 | `SSR` | Controls the high-voltage SSR / main power MOSFETs. | Automatically activates after boot via the Quiver SSR auto-engage Lua script. If deactivated for any reason while powered, monitor PCB temperature. |
| 2 | `Bypass` | Legacy bypass output for a separate fused low-current MOSFET path (typically 2–5 A). | Not used on current Dev-Kit operation. Leave off unless specifically instructed by the Quiver team. |
| 3 | `Add HV` | Enables the additional high-voltage connector output. | Enable only when an attachment requires the additional HV connector. |
| 4 | `P1 Sig` | GPIO signal from the flight controller to the bottom payload adapter. | Used for payload logic or switching when configured for the attachment. |
| 5 | `P1 12V` | Enables the separate 12 V supply for the bottom payload port. | Enable only when the bottom payload requires this supply, such as a motorized attachment. |
| 6 | `12V Pay` | Enables the general 12 V payload supply to the attachment interfaces. | Enable only when an attachment requires general 12 V payload power. This is separate from `P1 12V`. |

Relays 7 and above are not part of the standard Quiver Dev-Kit pilot workflow unless a specific aircraft or attachment configuration documents them.

> [!NOTE]
>
> Relay labels are an operator-facing safety aid. The labels do not change wiring or firmware behavior; they only make the Mission Planner relay controls easier to identify.


## 3. Power Up Procedure

This sequence defines the only approved process from battery installation to takeoff.

### 3.1 Aircraft Preparation (No Power)

1. Place aircraft on level ground within the established safety zone.
2. Verify motor arms are fully locked.
3. Inspect avionics bay:
   - No loose wiring,
   - SD card installed for logging.
4. Confirm the flight area is clear of uninvolved persons.

### 3.2 Battery Installation

5. **Install Battery:** Insert and latch mechanically.
6.  **Battery Wake:** Press the Battery Button (if Tattu 4.0) to enable output.

### 3.3 Avionics Power-Up

7.  **Drone Init:** Press the **Drone Push Button**.
    * *Expectation:* Air unit fan spins up, LEDs illuminate.
    * *Wait:* Allow 30-60 seconds for Flight Controller boot and GPS lock.
8. **GCS Link:** Verify connection on GCS. Check for "Ready to Fly" status (GPS: 3D Fix).
9. Verify:
   - No critical pre-arm errors,
   - Stable EKF status,
   - GPS fix with HDOP ≤ 1.6 and ≥ 14 satellites (check GCS Status tab).
10. **Verify SSR auto-engage:** In the GCS Servo/Relay page, confirm Relay 1 (`SSR`) has automatically activated and closed the high-voltage SSR after boot.
    * *Expectation:* Relay 1 / `SSR` is active without manual pilot input.
    * *Fault:* If Relay 1 / `SSR` is not active, do not arm. Verify the Quiver SSR auto-engage Lua script is installed and running, then troubleshoot the relay state.

### 3.4 Motor Power and Arming

11. Keep main motor power disabled during configuration.
12. Load mission or RTK data if applicable.
> [!NOTE]
>
> Steps 11–13 require the mission to be loaded before enabling motor power. This ensures:
> - Waypoints and geo-fence are verified while the aircraft is safe on the ground,
> - Any upload errors or configuration issues are caught before the motors are live,
> - The pilot can abort without risk if the mission is incorrect.
13. Enable main motor power.
14. Select LOITER mode.
15. Arm via RC.
    * *Expectation:* Motors spin at idle.
    * *Fault:* If a motor fails to spin, disarm immediately.
16. Observe motors for abnormal behavior.
17. Take off slowly and climb to a safe hover altitude.
18. Verify stability before proceeding with mission modes.

### 3.5 Abort Criteria

Abort immediately if:
- Electrical arcing occurs,
- Critical errors persist,
- Estimator instability is observed,
- Motor power enables unexpectedly,
- Any unsafe or unexplained behavior is detected.


## 4. Emergency Procedures
### 4.1 Kill switch

> [!WARNING] 
> 
> The kill switch was design to deliberately freeze and crash the aircraft. It should only be used when the aircraft is about to collide or cause serious damage. 
> 
> Use "Kill Switch" feature only after assessing the expected loss.
> Only use while the aircraft poses an immediate threat to life, or lost of every available control.

- When users toggle the dedicated "Kill" switch on the RC.
    - The SSR will open immediately and cutting all power to the motors. 
    - The aircraft will enter a ballistic free fall.

### 4.2 Flight Mode Changes (Failures)

#### 4.2.1 Low Battery (≤ 20%)
* **System Action:** Triggers **RTL (Return to Land)**.
* **Pilot Action:** Monitor the return path. Do not override unless the landing path is obstructed or unsafe.
    * *Warning:* RTL relies on GPS. Be ready to take manual control if navigation fails.

#### 4.2.2 Sensor Failure (GPS Glitch/Compass Variance)
- Indication: Drone "toilets" (swirls) or drifts uncontrollably.
- Action: Switch to AltHold (Altitude Hold) immediately. This disables GPS positioning. You must manually counter wind drift to land safely.
- High Vibration/Motor Loss: Land immediately.

#### 4.2.3 Single Motor Failure (Signs of incoming failure)

#### 4.2.3 Single Motor Failure

>[!CAUTION]
>
>For motor failure cases on a quadcopter aircraft, there is **NO** known method for in-flight recovery. The aircraft will crash.

**Indications of Motor Failure:**
- GCS warning messages: "Motor X output saturated", "Thrust loss", "Motor X RPM low"
- Sudden uncommanded roll, pitch, or yaw
- Audible change in motor sound (grinding, stuttering, silence from one motor)
- Visible smoke, sparks, or stopped propeller
- Aircraft rapidly losing altitude despite full throttle input
- "Toilet bowl" effect (uncontrolled spiraling)

**Pilot Actions:**
- In case of thrust, motor or yaw warning message, 
- Or the aircraft experiences unexpected roll, yaw, U-turn or insufficient yaw force during the flight:
    - Abort auto mission and switch to ground-controlled flight mode.
    - Land immediately with minimum maneuver and flight distance.
    - Avoid any property and creatures under the flight path.
    - If the aircraft is uncontrollable and heading toward people or property, activate the kill switch.
- Retrieve the aircraft and disconnect main power.
- The aircraft shall not takeoff before detailed inspection and testing.

#### 4.2.4 Fly-Away or Lost Control
#### 4.2.4 Fly-Away or Lost Control

> [!WARNING]
>
> A fly-away occurs when the aircraft stops responding to pilot commands and drifts or flies away from the operational zone. Time is critical — act quickly.

**Step 1: Attempt to Regain Control**

- If there is no activity or refreshing in ground control and telemetry: 
    - Try disconnect and reconnect the telemetry to regain control.
- Check the status or any flight mode misoperation on handheld RC transmitter.
    - Fix the operation by switch to any hover or unguided flight modes.
    - Shutdown and restart the RC transmitter and try switch the flight mode again.

**Step 2: If Control Cannot Be Regained**

- If the aircraft remain uncontrolled while stays in visual line of sight and geofence,
    - Maintain observation and remove any property below the aircraft.
    - The aircraft will automatically land itself when reaching low battery level.
- If the uncontrolled aircraft flies heading:
    - **To you**: **RUN AWAY** from the flight path.
    - To persons, creatures or properties: Activate the kill switch.
    - To hard target, ground, hill or vegetation: Let the aircraft to crash or hard landing.
    - To mid and high altitude airspace: Activate the kill switch.

**Step 3: If Aircraft Leaves Operational Zone**

- Note the last known position, altitude, heading, and battery level from GCS.
- Contact the Quiver team immediately (see §4.4).
- Do NOT chase the aircraft by vehicle — maintain situational awareness at the launch site.
- Prepare for search and rescue operations (see §4.3).

### 4.3 Aircraft search and rescue in wilderness 

> [!NOTE] 
> 
> If the aircraft lost connection mid-air and its exact location may variant, consider bring the ground station to the search area, to help regain the connection to the aircraft.

> [!WARNING] 
> 
> Do not enter hazardous terrain alone or without proper preparation. Maintain communication with a base station.

1. Record last telemetry frame from the ground station (Shall include attitude and coordinate).
2. Report aircraft lost to the business team and assemble search team and supply team.
3. Confirm offline available weather and entry path information of the search area.
4. Be prepare for the possibility that the aircraft may unable to evacuate immediately.
5. Consider bring any necessary items below for the search operation :

|Items|Purpose|
|-|-|
|Water|First and general wildness requirement|
|Food supply|For long time or heavy duty search operation|
|Communication device|For navigation and status feedback|
|Flash light|Visibility for extreme and night condition|
|Protection clothing|Isolate the environmental hazard|
|Large knife / Machete|Cutting plants and bushes for path|
|Bear spray or noise makers|Wild animals avoidance|

### 4.4 Contact the development team for help

>[!TIP]
>
> Prepare flight log, screenshot, photo or any material in advance could help resolve issues quicker.

If any Quiver aircraft unit encounters difficult problem or requires urgent / emergency assistance, please contact the Quiver development team for help.

- Join the Discord server: [Arrow](https://discord.com/invite/arrow)
- Visit the DAO forum: [Arrow DAO](https://dao.arrowair.com)

**... (NEED MORE CONTACT - KBM)**


## 5. Checklist
### 5.1 Pre-Flight Checklist
Before each new flight mission you should go through the pre-flight checklist:

**1. Airframe Inspection**

- [ ] Visual check (no deformation, cracks, loose fasteners, damage) 

- [ ] Structural mounting points (battery, payload) secure

Take photos of the airframe, details where necessary.

**2. Propulsion / Power System**

- [ ] Propeller(s) securely fastened, free of damage
      
- [ ] Battery charge adequate. Minimum voltage: 56.0V (4.0V/cell for 14S LiHV)

**3. Avionics / Electronics**

- [ ] Check all accessible physical connections

- [ ] Battery power control working normally

- [ ] Relay 1 / `SSR` automatically activates after boot via the Quiver SSR auto-engage Lua script

- [ ] Mission Planner Servo/Relay labels are set for relays 1–6 (`SSR`, `Bypass`, `Add HV`, `P1 Sig`, `P1 12V`, `12V Pay`)

- [ ] All pre-flight checks OK on the ground station

- [ ] RC remote & telemetry connections stable

- [ ] Joystick input working normally

- [ ] Geo-fence enabled and configured for current site:
  - [ ] `FENCE_ENABLE` = 1
  - [ ] `FENCE_RADIUS` set appropriately for operational area
  - [ ] `FENCE_ALT_MAX` set appropriately for site altitude limits

**4. Pilot Notes**

- [ ] Flight plan reviewed and acknowledged.

- [ ] IM SAFE (Not Flying Under Influence or Risky Decision).
 
Note anything that is missing on the aircraft or anything that doesn't feel right.

### 5.2 After flight check list

- [ ] Logs: (Optional) Save flight logs for maintenance records.
    1. Transfer and save the flight logs file with the GCS.
    2. Upload to flight tracking platform is very welcome.

- [ ] Power Down:
    1. Disable main power breaker with the GCS or remote button.
    2. Disable the push button.
    3. Power down the battery.
    4. Remove the battery from the drone.

- [ ] Inspection: 
    1. Check motor temperatures (shall not be scorching or being huge difference).
    2. Inspect propeller tips and leading edges.
    3. Inspect chassis.
    4. Inspect aircraft total shape for potential deformation from different angle.


- [ ] Storage: Store battery in fire-safe container or location

## 6. Flight tracking platform

### 6.1 Platform Overview

Quiver operates an in-house flight tracking and analysis platform:

https://project-flight-tracking.vercel.app/

The platform is used to:
- Track accumulated flight hours,
- Correlate flights with firmware and configuration state,
- Support anomaly and incident investigation,
- Maintain maintenance traceability.

Use of the platform is encouraged for all Dev-Kit operations.

### 6.2 Aircraft Registration

Each Dev-Kit aircraft is pre-registered on the platform by the manufacturer prior to shipment.

When uploading logs, the pilot shall select the existing registered aircraft corresponding to the physical airframe. Duplicate aircraft entries are not permitted.

### 6.3 Flight Log Upload

After each flight:

1. Retrieve the onboard flight log.
2. Upload the log to the platform.
3. Select the correct registered aircraft.
4. Enter the required flight metadata.

Flights conducted without logs or metadata may be excluded from test analysis.

### 6.4 Required Flight Metadata

Each flight entry shall include:
- Date
- Location or anonymized region
- Weather conditions
- Mission type
- Pilot notes describing abnormal behavior, system warnings, and pilot interventions.

### 6.5 Maintenance and Modification Log

Any modification made after delivery shall be recorded in the platform maintenance log, including:
- Hardware changes
- Wiring or structural modifications
- Sensor replacement or repositioning
- Firmware updates
- Approved parameter changes

Each entry shall include date, description, reason, and affected flights.

### 6.6 Problem Reporting

For anomalies, near-misses, or incidents, upload:
- Relevant flight log(s)
- Firmware version
- Parameter set identifier
- Weather conditions
- Description of expected vs observed behavior
- Severity assessment
