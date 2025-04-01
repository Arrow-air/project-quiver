# Quiver PT2 FEA analysis

The FEM demonstrates how the structure will behave under the following forces:

- 12.5 Kg of force acting at the end of each motor beam (full throttle).

- 50 kg of counterforce acting on the attachment plate.

- The materials in this study are:

  - Aluminum 6060 for all the foldable motor arm connectors, upper landing gear adapters, aluminum plates, rectangle aluminum tubes.
  - Carbon fiber for the motor arms and landing gear legs.

**Note:** The structure is constrained at the bottom landing legs. They will not feel any force, as the forces in flight only act in the cockpit, and this has been taken into account in this simulation (force and counterforce).

### Safety

#### Image 1: FEA safety

![](https://holocron.so/uploads/6f008d11-image.png)

### Displacement

#### Image 2: FEA displacement

![](https://holocron.so/uploads/c8a84756-image.png)

### Stress

#### Image 3: FEA stress

![](https://holocron.so/uploads/859d38cb-image.png)

#### Image 4: FEA stress 2

![](https://holocron.so/uploads/9ec4db9b-image.png)

Stress detail:

#### Image 5: FEA stress detail

![](https://holocron.so/uploads/937426df-image.png)

### Results Summary

- The aluminum structure has very low stress values indicating a high possibility of weight savings through the removal of material and the reduction of component thickness.

- The results yielded a 2.318 safety factor at the motor arm adapter. The required safety factor of 2.5 was not quite achieved, but this is no cause for concern as this condition only occurs in extreme cases. Under normal conditions, the safety factor is around 4.0. Furthermore, the adapter was tested under maximum thrust and no permanent deformations were detected. A dynamic simulation was not carried out.

- The max displacement of one of the motor beams reached 2.31 mm.

- The max stress occurred at the motor beam to foldable motor arm connector with a value of 159.175 Mpa.

**Recommendation:**

- Observation of the motor arm adapter.
- Dynamic simulation in the future.
- Weight reduction of the aluminum structure.