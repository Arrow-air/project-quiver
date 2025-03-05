# Engineering Meeting 2/4/25

Date: February 4, 2025
Created time: February 4, 2025 9:02 AM
Recording: 2025-02-04 09-01-57.mp4 


### Notes

- Suggestion to place HV positive trace on top layer of PCB and neg trace on bottom layer
    - would be a good solution to reduce the size of the PCB
    - Pushback on that solution for this prototype. We are not too worried about spacing yet
- Cockpit changes
    - Not too many new ideas
    - Suggestion to place battery vertical in the cockpit
        - can not make the aircraft smaller because we will need clearance between props
        - Alperen thinks that the structural weight might be too much
            
            ![image.png](image.png)
            
    - hard to make modifications without knowing any of PT1 performance
    - Can arms be folded in the vertical direction
        - horizontal folding can conflict with oversized equipment
            - saves more cockpit space because it removes the space consideration
        - there are connectors that allow for this
            - compatible with the current design and wouldn’t require changes to bolt pattern
        - depends on the landing gear selection
            - most drones use direct assembly
            - we want folding for storage purposes
        - adding connection points reduces reliability of the beams
    - Motors are pretty maxed out for thrust
        - will fall short if we’re at 25kg MTOW
            - dependent on maneuverability limits we will set
            - can not assess that without flight data from the model
            - chassis can change if we upgrade the motors and they have a larger size tube
    - telescopic motor arms can be an option but that might be harder to manufacture or practical
    - In the future we might have to design our own motor arms
- Potato updates
    - unsure when it will fly
    - might try to do a motor test this week
    - Thoughts on making modifications to Potato to work with Pixhawk
        - shouldn’t be difficult to work with current PCB
        - Julius is eager to get Potato flying as is in since he is so close to being done
    - powered on today and the ESCs lit up
        
        ![image.png](image%201.png)
        
- We really need to see test data ASAP in order to meet the deadline for PT2 design
    - eager to see the performance with the brush bullet
        - can fill the dispenser with a mock payload (stones) to meet the 25 kg MTOW
            - 4-5 kg with current battery
