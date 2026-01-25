---
title: Pilot Handbook
tags: [dev-kit]

---

---
title: Pilot Handbook
tags: dev-kit
---

# Pilot Handbook
Quiver Dev-Kit
Heavy-Lift Multipurpose UAV (<25 kg MTOW)

Table of content
[toc]

## 1. Safety & Compliance

### 1.1 General Safety Principles
The Quiver Dev-Kit is a mid-voltage electrical battery powered heavy-lift quadcopter drone (MTOW ~25kg). It is designed for industrial enterprises aerial applications instead of general entertainment, adult and teenager fun purpose, incendiary and explosive handling or critical medical life-supporting.

:::danger
**DANGEROUS:**
Any improper or reckless action can result in :
 
 - Immediate fatality
 - Severe permanent injury or disability
 - Chemical fire hazard
 - Property damage
 - False public alert, panic or unnecessary crowds
 - Noise pollution or disturbing
 - Reputational damage to business
 - Possible legal issues
:::

All operators must be trained and familiar with their devices and local aviation regulations, meanwhile remain clear awareness and not affected by drugs, alcohol or emotional fluctuations during all operation.

### 1.2 Operational Limits
#### 1.2.1 Weather Conditions
**Wind Speed**:
Maximum sustained wind speed is XX.X knots (approx. XX km/h). Gusts exceeding this limit may compromise stability.

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

Open Category C3 and A3:
You may fly without a SORA if you maintain a minimum horizontal distance of 150 m from residential, commercial, industrial, or recreational areas and ensure no uninvolved people are endangered.

Specific Category:
If your mission requires flying closer than 150 m to populated areas or over people, you must obtain an operational authorization based on a SORA (Specific Operations Risk Assessment) or PDRA.

**USA (FAA)**:

You must hold a Remote Pilot Certificate (Part 107).

The aircraft must be registered with the FAA.

Operations over human beings are prohibited unless complying with remote ID and kinetic energy limitations, which this aircraft (25 kg) generally exceeds without a specific waiver.

**Geo-Fencing**:

The pilot must establish a local geo-fence for every flight.

Setup: Configure the FENCE_RADIUS and FENCE_ALT_MAX in the ground station software to contain the drone within the authorized flight volume.

:::warning
**WARNING:**
Due to software limitation, geo-fencing may not function during a navigation system or location source failure.
:::

**Experimental Systems Disclaimer**:

Radar & LiDAR Altimeters: These sensors are currently integrated for testing purposes only.

Do not rely on these sensors for critical flight phases. The pilot must verify altitude visually and via barometric telemetry.

These systems may be activated for controlled testing only when there is zero risk to third parties, animals, or infrastructure.

**Instructions on how to find local regulations**:
...

### 1.3 Electrical Warning

#### 1.3.1 Arcing & Spark Risk
The electrical system is designed to be spark-free during connection via a pre-charge circuit.

:::warning

**WARNING:** 
If you observe any visible spark or audible "crack" when connecting the battery :
- STOP immediately.
- Disconnect and contact support.
- Do not fly.

This indicates a failure in the pre-charge circuit or a short in the power system.
:::

#### 1.3.2 Flight Battery Handling
**General Principles：**
:::info
The general principles are applied to both battery and charger side.
:::
- Use only Tattu 3.5 or 4.0 14S Smart LiHV batteries.
- Use only the official Tattu-supported charger compatible with 14S LiHV chemistry.
- Never short or ground the battery main connector even in non-operating condition.
- Minimize the unnecessary plug-and-unplug cycles to extend power connector life.
- Always check power connector cleanliness and dryness.
- Always keep a Class D fire extinguisher nearby (additional fire blanket are recommended).

**Charging:**
 
- Charge only in a designated dry, fire-resistant area (e.g., concrete floor), away from living quarters or flammable materials.
- Never charge a battery that significantly warmer than human body temperature or right after a fully-discharge flight. Allow it to cool down for 15 ~ 30 minutes before apply a charging current.

**Transport & Storage:**

- If the battery will not be used for next 3 Days, discharge it to the storage voltage or ≥ 55 % capacity or 3.80V per cell.
- Any battery dropped from any height > 50 cm is unsafe for flight. Internal damage is invisible and can cause unpredictable power outage or fires.
- Water vapor may condense on battery surface while transferring from cold to hot environment. Do clean up or let it dry before any connecting operation.

**In-Flight:**

:::warning
**WARNING:**
To prevent the failure from escalating, always handle with gentle maneuver during in-flight battery system emergency.
:::

- If battery temperature reports > 56 °C during flight, land immediately.
- If voltage meter decrease or oscillate with abnormal speed, or stop changing, land immediately.

**Battery Fire Emergency**:
:::warning
**In case of pungent gas, irregular popping sounds or smoke, immediately :**

- Disconnect the battery without confirm.
- Bring battery and run to an open area with no flammable materials (not to the indoor corridor).
- Bring Class D fire extinguisher and observe from at least 15 meters away.
:::

:::danger
**In case of a flaming battery pack indoor :**

- Ask other personnel to evacuate and let them call for fire department.
- Cover the battery with fire blanket as possible.
- Cut-off indoor power supply.
- Remove proximity object from the battery as possible.
- Evacuate to open area.
:::

### 1.4 Establishing safety zone due to heavy kinetic energy

The drone enerates significant kinetic energy during flight. A free-fall impact from operational altitude carries lethal force, capable of penetrating vehicle roofs or causing fatal injury. Therefore, establishing a correct safety zone is the single most critical pre-flight step.

**Official Guidelines as Primary Source**
The Pilot in Command (PIC) must strictly adhere to the safety distances mandated by the local aviation authority. These regulations take precedence over any manufacturer recommendations:

- **EU (EASA)**: Operations fall under the Open Category A3. You must maintain a horizontal distance of at least 150 meters from residential, commercial, industrial, or recreational areas. You must never fly over uninvolved persons.

- **USA (FAA)**: Operations under Part 107 generally prohibit flight over human beings for drones of this weight class (Category 3/4) without a specific Declaration of Compliance or Waiver, due to the kinetic energy exceeding 25 ft-lbs limit.

**Operational Safety Zone Calculation (Ground Risk Buffer)**
To ensure no harm can come to any person or animal in the event of a complete power failure (ballistic fall), the pilot must establish a **Ground Risk Buffer**. This buffer extends beyond the intended flight path.

A widely accepted safety standard for rotary-wing aircraft is the 1:1 Rule:

:::info
Minimum Safety Buffer = Flight Altitude (AGL)
:::

- **Example**: If flying at 50 meters (164 ft) altitude, you must ensure a clear zone of at least 50 meters horizontally from your flight path where no uninvolved persons are present.

- **Why?** If the drone loses power while moving at speed, momentum will carry it forward as it falls. The 1:1 rule provides a simplified safety margin to contain this ballistic trajectory.

**Implementation Steps**:

1. **Identify the Operational Volume**: Define the exact area where the drone will fly.

2. **Add the Buffer**: Extend this area by a distance equal to your maximum planned altitude (the 1:1 rule).

3. **Verify the Ground**: Ensure this entire extended zone is clear of non-participants, animals, and critical infrastructure.

4. **Geo-Fence**: Program the flight controller's Geo-Fence to prevent the drone from exiting the Operational Volume, ensuring that even if it hits the "virtual wall" and falls, it remains within the Ground Risk Buffer.

## 2. System Setup
### 2.1 Unbox and assemble
:::success
Ask for a help or handyman for assembling is recommended due to the large size of the aircraft.
:::
:::warning
**WARNING: Be aware of pinch and cut**
The unlocked folding motor arms will rotate while being applied with horizontal force or bad handling technics.
:::
**1. Preparation:**
- Reserve enough space for the transport case, devices and the aircraft assembly.

**2. Extraction:** 
- Lift the aircraft by the central aluminum chassis with symmetrical handling. 
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

> [color=lightgreen][name=KBM] need further progress for this chapter

### 2.2 Installing battery
:::info
Acknowledge the "Flight Battery Handling" chapter before handling the battery.
:::
:::warning
**WARNING: During the following steps**
- Do not power on the battery.
- Do not press the battery power button right after the installation.
:::
1. Align the battery to the 3D-printed guide rails with the connector side up. 
2. Insert the battery by sliding it into the aluminum chassis.
3. Secure the mechanical latch and check the lock position.
4. Confirm the battery is locked in place by applying a light pull on the lift handle.

### 2.3 Battery power button 
> [color=lightgreen][name=KBM] need more confirm

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

The drone is not ready to fly yet. The main power MOSFET needs to be activated via a relay button in the ground control station.

### 2.5 1st time setup
- Mandatory steps before first flight
- Firmware/parameter version verification
- Sensor calibration checks and requirements

### 2.6 Parameter walk through
- Point to the official arrow parameter list in the wiki or Gitub
- Explain only the most important parameters like failsafes, geo-fence
- The official arrow parameter list could include links to Ardupilot wiki for explanation
- No parameters should be changed. Only if the pilot is experienced and wants to change the flight characteristics (A minimum hours of flight time could be enforced for a parameter change request. These changes should be stored in a changelog if any)

### 2.7 RC setup
- Determine which remote we will make official 
- Connection from remote to drone (with or without additional PC)
- Overall joystick function and channel mappings
- Button Assignment

### 2.8 GCS setup
- installing QGC or Mission Planner
- Setting up SIYI unit
- Camera setup guide 
- Telemetry link expectations
- Map/airspace configuration
## 3. Power Up Procedure
### 3.1 Walk through from battery installation to arming drone
- Exact sequence (numbered)
- What to wait for between steps
- Expected LEDs / tones
- What indicates a fault
- Reasons arming will be blocked
- When to abort power-up
## 4. Flight Emergency Procedures
### 4.1 Kill switch
:::danger
**DANGROUS:**
The kill swtich was design to deliberately crash the aircraft, it should only be used when the aircraft is about to collide or cause serious damage. 

Use this feature only after assessing the expected loss.
:::

- When toggle the dedicated "Kill" switch on the RC.
    - The SSR will open immediately and cutting all power to the motors. 
    - The aircraft will enter a ballistic free fall.

:::danger
Only use if the aircraft poses an immediate threat to life and all other control methods have failed.
:::

### 4.2 Flight mode change due to failures (low battery, sensor failure, etc.)
#### 4.2.1 Low Battery (≤ 20 %)
- The aircraft system will trigger RTL mode.
    - The aircraft will return to the home point in a direct flight. 
- Do not override unless: 
    - The landing path is obstructed.
    - Any other unsafe factor in the direct flight route back home.

:::warning
**WARNING:**
RTL mode may not working during navigation or location source failure.
:::
#### 4.2.2 Sensor Failure (GPS Glitch/Compass Variance):
- Indication: Drone "toilets" (swirls) or drifts uncontrollably.
- Action: Switch to AltHold (Altitude Hold) immediately. This disables GPS positioning. You must manually counter wind drift to land safely.
- High Vibration/Motor Loss: Land immediately.

### 4.3 Aircraft search and rescue in wilderness 
> [color=lightgreen][name=KBM]

(capture or record last telemetry frame)
(report aircraft lost to the business team and assemble a search team)
(confirm weather forecast of search area)
(prepare for the located aircraft may not be able to evacuate immediately)
(always bring water and supplies)

## 5. Check List
### 5.1 Before flight check list
Before each new flight mission you should go through the pre-flight checklist:
**1. Airframe Inspection**

- [ ] Visual check (no deformation, cracks, loose fasteners, damage) 

- [ ] Structural mounting points (battery, payload) secure

Take photos of the airframe, details where necessary.

**2. Propulsion / Power System**

- [ ] Propeller(s) securely fastened, free of damage

- [ ] Battery charge adequate. Battery Voltage:

**3. Avionics / Electronics**

- [ ] Check all accessible physical connections

- [ ] Battery power control working normally

- [ ] All pre-flight checks OK on the ground station

- [ ] RC remote & telemetry connections stable

- [ ] Joystick input working normally

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

- Sign up and enter aircraft and pilot information

- How to upload and tag flights. 
- Naming convention 
- How to anonymize the location data via the platform
- What to include in pilot's notes
- How to report a problem