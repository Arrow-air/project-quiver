# Status

`Valid`

# Project Description

This information note describes the solution to the problem that the two diagonal motor pairs (in a quadcopter) have a significant difference in performance during operation.

# Methodology

A difference in performance between the diagonal motor pairs, as shown in the following illustration, can be eliminated by realigning the motors. The difference in performance may also be caused by other problems (e.g. defective propellers), but this information note only refers to the realignment.

Picture 1: Power level before realignment

![](https://raw.githubusercontent.com/Julius-eng/project-quiver-05032025/refs/heads/main/task-grant-bounty/pt2/troubleshooting/0001-diagonal-motor-pair-power-difference/pictures/01.png)

When motors on a drone are not mounted perfectly horizontally, their thrust is slightly angled, creating unintended torque and directional forces. Since drones rely on pairs of clockwise (CW) and counterclockwise (CCW) spinning motors to balance torque, any misalignment disrupts this balance. The flight controller compensates by adjusting thrust, often increasing power to one diagonal motor pair (either CW or CCW) to counter the imbalance. This causes that motor pair to draw more current than the other, leading to uneven power usage and possible long-term wear or performance issues.

### Steps to Fix the Imbalance:

#### 1. Identify the Issue:

Review flight logs to confirm a consistent power difference between diagonal motor pairs.

#### 2. Check Motor Alignment:

Place your flat tool across each motor pair:

- Front-Left ↔ Front-Right (FL-FR)
- Front-Right ↔ Back-Right (FR-BR)
- Back-Right ↔ Back-Left (BR-BL)
- Back-Left ↔ Front-Left (BL-FL)

Look closely for any visible gaps or angles between the motor surfaces and the tool. A tilt will be visible as a small gap or misalignment.

#### 3. Adjust Misaligned Motors:

Loosen the 4 screws on the misaligned motor’s mount (do not remove them).

Reposition the motor until it sits level. Use the tool to confirm there are no visible gaps.

#### 4. Secure the Motor:

Once level, carefully tighten the screws while maintaining alignment.

Recheck with your tool to ensure the motor hasn’t shifted during tightening.

#### 5. Final Check:

Repeat the leveling check across all four motor-to-motor positions to ensure full alignment.

#### 6. Test Flight:

Conduct a controlled test flight and review logs to confirm the power draw is now balanced.

# Results and Deliverables

#### 1. Identify the Issue:

- The performance level of two motors is much higher than that of the other two (see picture 1 in this information note)

#### 2. Check Motor Alignment:

- The alignment check was performed with a large spirit level:

  Picture 2: Alignment check

  ![](https://raw.githubusercontent.com/Julius-eng/project-quiver-05032025/refs/heads/main/task-grant-bounty/pt2/troubleshooting/0001-diagonal-motor-pair-power-difference/pictures/02.png)

  Some misalignments were visible:

  Picture 3: Small gap

  ![](https://raw.githubusercontent.com/Julius-eng/project-quiver-05032025/refs/heads/main/task-grant-bounty/pt2/troubleshooting/0001-diagonal-motor-pair-power-difference/pictures/03.png)

  #### 3. Adjust Misaligned Motors:
  - The motor tilt was adjusted by hand. During alignment the spirit level was kept on the motors. All four motors were realigned

  #### 4. Secure the Motor:
  - All motor mount screws were carefully tightened

  #### 5. Final Check:
  - A final check was performed between all motor pairs. No gaps are visible

  #### 6. Test Flight:
  - The logs show a much better power distribution between the motors. The alignment was successful

  Picture 4: Power level after realignment

  ![](https://raw.githubusercontent.com/Julius-eng/project-quiver-05032025/refs/heads/main/task-grant-bounty/pt2/troubleshooting/0001-diagonal-motor-pair-power-difference/pictures/04.png)


## Files

The photos can be found in a separate github folder.

# Remarks

- In this case I was performing the realignment two times, because i over-corrected it the first time
