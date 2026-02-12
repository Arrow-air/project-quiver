# Quiver Maintenance Guide

Quiver Dev-Kit
Heavy-Lift Multipurpose UAV (<25 kg MTOW)

Table of content
[toc]

## 1. General Maintenance Principles

Maintenance operations are essential to discover potential issues within aircraft subsystems, reduce failure rates, and ensure the aircraft operates at peak performance. Regular maintenance is also critical for ensuring the aircraft can adapt to extreme mission environments. 

If a technician lacks the necessary tools or confidence to perform a specific maintenance operation, starting with a detailed visual observation is a valid best practice. Always share findings with the team or professional maintenance personnel before attempting repairs.

## 2. Subsystems Maintenance Checklist

Each subsystem affects the necessary functions, performance, and safety of the aircraft. 
Maintenance personnel should pay attention to the specific components listed below:

### 2.1. Motor Arm Assembly

| Component | Inspection Check | Potential Risk |
| :--- | :--- | :--- |
| **Propellers** | Check for cracks, fractures, or surface burrs. | Harmful vibration; cracks may spread leading to a crash. |
| **Propeller Clamp** | Ensure screws are tight and secure. | Vibration; risk of propeller falling off. |
| **Integrated Motor** | Check rotor case for cuts, notches, or deformation. | Coil damage, overheating, or fire risk due to stator collision. |
| **Motor Mount** | Verify arm mounting slot screws are tight. | Motor unit tilting causing unstable flight performance. |
| **Arm Connectors** | Check folding joint screws for play / looseness. | Harmful vibration and reduced flight stability. |
| **Arm Tube** | Inspect Carbon Fiber for cracks, fractures, or burrs. | Tube breakage during high-stress maneuvers. |

### 2.2. Cockpit Structure Assembly

| Component | Inspection Check | Potential Risk |
| :--- | :--- | :--- |
| **Structural Fasteners** | Check general airframe screws for tightness. | General structural integrity loss. |
| **Main Enclosure** | Verify screw tightness and overall case integrity. | Structural failure or component exposure. |
| **Top Lid** | Check hinge movement and latch security. | Lid opening in flight. |
|**Attachment Interface**|Check for wearing, contamination and pogo pin spring tension.|Unstable attachment equipment connection and controlling.|
| **Battery Interface** | Inspect latch slot for cracks or deformation. | Battery falling off; difficult insertion causing insecure locking. |
| **Battery Bay** | Check slide rails for dust, grease, or cracks. | Battery shifting in flight; difficult insertion or power loss. |
| **Battery Connector Cut-Out** | Check for deformation around the connector opening. | Poor electrical connection; invisible overheating signs. |

### 2.3. Electrical Components

| Component | Inspection Check | Potential Risk |
| :--- | :--- | :--- |
|**PCB Connectors**|Inspect for loosen and contaminated connectors.|Short circuit or unstable connection lead to system failure.|
| **External Sensors** | Check mounts for cracks or loose screws. | Sensor tilting causing Flight Control errors or camera malfunction. |
| **Sensor Cabling** | Ensure cables are tight and not blocking sensors. | Obstruction of critical sensors. |
| **Battery Power Connector** | Inspect for dust, debris, or pitting on pins. | Reduced lifespan, short circuits, or total power loss. |
| **Battery Latch** | Check for broken latches or lost spring tension. | Battery shifting during maneuvers leading to power loss. |
|**Battery Pack Voltage**|Verify cell balance and total voltage.| Permanent damage to the battery. |

## 3. Tools Requirement

There is generally no strict requirement on tool brands for maintenance operations, but using tools with correct specifications and high quality helps extend the life of flight equipment. 

:::warning
**WARNING :**
Always acknowledge the user manual before using your tools.
:::

### 3.1. Always-prepared Items

The Quiver Dev-kit is a complex system that may encounter various configurations in the field. The following tools are recommended to be carried at all times during flight operations:

| Item | Requirement | Purpose |
| :--- | :--- | :--- |
| **Pliers** | Narrow / Thin | Modifying cables, connectors, and nuts in tight locations. |
| **Backup Propellers** | Full set (CW & CCW) | On-site repair for potential propeller damage. |
| **Hex Wrench Set** | L-Shape, Metric, Ball-end | Accessing fasteners in both open and narrow locations. |
| **Zip Ties** | ≈ 20 cm, medium flexibility | Wiring and cable harness management. |
| **Brush** | Non-conductive fiber | Safely cleaning electronic components. |
| **Rag / Paper Towels** | Lint-free | Cleaning grease or water drops. |
| **Personal Device** | PC / Tablet, USB-C cable | Ground diagnostics and configuration software. |

:::info
**REMINDER:**
For fastener tools such as hex wrench, confirm with the "Structural Assembly Guide" document or other user manual from equipment suppliers for the correct size and parameters.
:::

### 3.2. Additional Items

In addition to the field kit, the following things are **recommended** for the maintenance base to perform deeper level of cleaning, maintenance, and diagnostics.

#### 3.2.1. Devices

|Item|Requirement|Purpose|
|-|-|-|
|**More brushes**|Non-conductive fiber, Different sizes|Cleaning narrow locations.|
|**Compressed air device**| Pressure limitation|High efficiency dusting.|
|**Multimeter**|Digital display|Voltage and continuity inspection.|
|**DC power supply**| Adjustable Voltage | Powering up individual subsystems for analysis.|
#### 3.2.2. Fasteners & Consumable

|Item|Requirement|Purpose|
|-|-|-|
|**Screws**|-|(According to "Structural Assembly Guide" and equipment documents)|
|**Electrical tape**|-|Protecting exposed electrical connections.|
|**Velcro band**|-|Temporarily equipment and cable fixing.|
|**Adhesives**|Non-corrosive, Acid-free|Fixing any potential enclosure fracture.|

## 4. Regular Maintenance

This chapter provides a workflow for regular in-base maintenance. This procedure helps discover and record potential malfunctions and can be performed by personnel with basic training.

:::warning
**WARNING :**
For safety, the flight battery must be **removed** before starting the maintenance procedure.
:::

:::danger
**DANGER :**
Carbon fiber splinters can cause penetrating injuries. If you suspect a crack in carbon parts, use protective gloves or a cloth when handling.
:::

1. **Assembly & Extension:**
    - Check necessary frictions of landing gear insertion.
    - Check for loose screws on arm folding mechanisms.
    - Ensure proper operating clearance of the arm folding mechanism.
    - Check friction and security of telemetry antennas.
2. **Cockpit Structure Visual Inspection:**
    - Check for deformation, cracks or deep scratches.
    - Tap on different surfaces to discover any loosen fasteners.
    - Check the connections of hinges and latches.
3. **Propulsion System:**
    - Extend propellers to the straightened position.
    - Check for loose fasteners on the thrust unit (motor).
    - Visual inspect for any propeller fractures or cracks.
    - Gently run a finger along propeller edges to detect burrs or chips.
4. **Internal Inspection:**
    - Open the cockpit lid gently.
    - Check lid hinge and latch fastening integrity.
    - Check mating quality between lid and main enclosure.
    - Inspect PCBs and Flight Controller for cleanliness.
    - Gently touch cables to check tension and connection security.
5. **Logging:**
    - Add a record to the maintenance log (Time, Issue Location, Status, Tools Used).
    - Photo or imagery are recommended.
    - Note them to a record. 
    - Report significant findings to professional engineering personnel.

### 4.1. Before & After flight

**Before Flight (Pre-Mission)**
* Perform visual inspection of aircraft shape and texture.
* Verify arm locking mechanisms are secure.
* Ensure payload interface is in good condition.

**After Flight (Post-Mission)**
* Perform visual inspection for new scratches or stress marks.
* Wipe down optical sensors (LiDAR/Radar).

### 4.2. Environment conditions 

For flight missions in harsh environment, extra maintenance steps are required.

1. Full power shutdown and remove the battery.
2. Wipe the remaining drops as clean as possible.
3. Check and clean gimbal camera and cockpit.
4. Follow the table below :

| Condition | Additional Measures |
| :--- | :--- |
| **Rain / Snow** | Leave the aircraft in a non-condensing, air-conditioned area to dry completely. |
| **Dust** | Perform compressed air dust removal on PCBs, motors, and attachment interfaces. |
| **Chemicals** | Perform decontamination on handling surfaces before transporting the aircraft. |

:::warning
**WARNING :**
If you discover water drops in the cockpit, that indicates the current flight condition exceeds the waterproof design level. Pause operations and wait for stable weather.
:::

### 4.3 Hour cycles maintenance

Operational stressors and environmental factors inevitably degrade aircraft components over time, increasing mechanical load and reducing safety margins. As a quadcopter platform, the Quiver Dev-Kit’s durability is primarily challenged by thrust-induced vibrations, acceleration forces, and environmental exposure.

The following checks should be performed at specific intervals:

| Flight Hours | Maintenance Items |
| :--- | :--- |
| **8 Hours** | Soft cleaning of cockpit inner space. |
| | Soft cleaning of battery connector and slide rails. |
| **24 Hours** | Rigidness check of PCB connectors and fasteners. |
| | Dusting of PCB and connectors. |
| | Check fasteners on thrust units and propellers. |
| | Calibrate Flight Controller IMU / Inertia sensors. |
| **50 Hours** | Check fasteners for external devices (e.g., Attachment Interface). |
| | Detect airframe structural deformation using a scale/straight edge. |
| | Partial disassembly for detailed inspection and cleaning. |
| | Inspect shock absorption and rubber components. |
| | Test battery connector contact resistance. |

:::warning
**WARNING :**
Excessive cleaning or plugging/unplugging of electrical connectors may decrease their cycle life. Clean only when necessary.
:::

## 5. Troubleshooting & Unscheduled Maintenance

Always be prepared for unexpected cases to minimize downtime and damage.

### 5.1. Abnormal behavior

Given the variability of flight missions and environmental conditions, the aircraft may occasionally exhibit irregular behavior. These anomalies can range from temporary glitches resolvable on-site to substantial issues indicating long-standing malfunctions. Correctly identifying the severity of these behaviors is critical for maintaining aviation safety and operational efficiency.

Here are some examples : 

| Behavior | Potential Cause | Solution | Result |
| :--- | :--- | :--- | :--- |
| **Heavy friction in joints** | Environmental particles (dust/sand). | Clean and lubricate (if applicable). | Friction returns to normal. |
| **Difficult battery insertion** | Connector or casing deformation. | Inspect battery and bay. | Repair or replace battery/rails. |
| **Top lid won't close** | 3D part deformation or cable pinch. | Inspect with flashlight while closing. | Reroute cable or adjust hinge. |
| **Excessive Vibration** | Unbalanced prop or loose arm. | Check props and arm bolts. | Flight becomes smooth. |
|...|...|...|...|

**Specific Component Diagnostics:**

* **Loose or Cracked Parts:**
    * **Visual Deformation:** If metal parts are bent, decommission immediately. If 3D printed parts show stress whitening or layer separation, replace.
    * **Surface Feel:** If a surface feels rough or "glitchy" (delamination), inspect closer.
    * **Friction Loss:** If a folding joint loses friction, tighten the tension screw. If a 3D printed joint is worn loose, replace the part.

* **Irregular Response:**
    * **Sound:** Cracking sounds indicate structural stress; grinding sounds indicate motor bearing failure.
    * **Takeoff Vibration:** Often caused by a loose fastener in the arm system.
    * **Overheating:** Electronics getting hot quickly may indicate a short circuit or bad connection. Note that motors naturally get warmer in summer.

### After impact & accident inspection list

#### Hard or failed landing

Any landing with an unsafe touchdown maneuver is considered a **Hard Landing**. If the aircraft suffers major damage, it is a **Crash**.

| Incident Level | Inspection Scope |
| :--- | :--- |
| **Heavy Landing** | **1. Landing Gear:** Check for cracks in mounts or tubes. |
| *(About to bounce)* | **2. Mission Attachments:** Verify security and pogo-pin connection. |
| | **3. Battery:** Check insertion alignment and connector integrity. |
| **Turn Over / Flip** | **1. Propellers & Motors:** Check for chips, bent shafts, or gravel in bells. |
| *(Props touched ground)* | **2. Motor Arms:** Check carbon tubes for crushing/cracking. |
| | **3. Arm Connectors:** Verify folding mechanism isn't bent. |
| | **4. Plates:** Check central chassis for twisting. |
| **Crash / Terrain Impact** | **1. Full Structural Audit:** All of the above. |
| | **2. 3D Printed Parts:** Check for shattering or layer split. |
| | **3. Flight Controller:** Re-calibrate IMUs; check isolation dampers. |
| | **4. Decommissioning:** Assess if repair cost exceeds replacement. |

**Tree Collision Specifics:**

* **Foliage (Leaves):** Check propellers for green stains/chips; check 3D printed parts for impact marks.
* **Branches:** Check external sensor cables and antennas for cuts/tears.
* **Stuck in Plant:** Consider as a full crash; perform full audit.

## 6. Remarks

This maintenance guide is a living document and may be updated based on flight experience and technical advancements.

*(End of content)*
