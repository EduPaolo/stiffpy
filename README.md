# stiffpy
___

This repo has code for structural analysis with the direct stiffness method,
a matrix method that uses stiffness relations. The code can handle various elements,
loads and boundary conditions.

**This project is still in development**

## Install stiffpy
To install stiffpy you need to manually clone the repository.

## Features
* Shear Force Diagrams
* Bending Moment Diagrams
* Displacements
* Fixed Supports
* Hinged Supports
* Custom Supports
* Point Actions in Nodes and Elements
* Distributed Forces in Elements
* Hinged Elements
* Releases at Element end nodes


## Programs
* __Truss__
* __Beam__
* __Frame__
* __Spring__
* __Linear Triangle__ (Soon)

## Examples
### Spring Example

```python
# Import Modules
from stiffpy.spring import *
# Define Nodes
node_1 = Node(0)
node_2 = Node(10)
node_3 = Node(20)
# Define Members
member_1 = Member(node_1, node_2, 10)
member_2 = Member(node_2, node_3, 20)
# Define Beam
spring = Spring()
# Add Node Loads
node_2.force = Force(-10)
# Add Restrains
node_1.restrains = True
node_3.restrains = True
# Add Members to Beam Object
spring.members = member_1
spring.members = member_2
spring.solve()
print(spring.reactions)
```

### Beam Example

```python
"""
Integrated Matrix Analysis of Structures, Mario Paz & William Leigh
Illustrative Example 1.4, pp 17
"""
# Import Modules
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.beam import *
# Define Material and Section
material = Material(E=29e3, f_y=1, f_u=1)
section = Section(A=1, Ix=882, material=material)
# Define Nodes
node_1 = Node(0)
node_2 = Node(90)
node_3 = Node(180)
node_4 = Node(300)
node_5 = Node(396)
# Define Members
member_1 = Member(node_1, node_2, section)
member_2 = Member(node_2, node_3, section)
member_3 = Member(node_3, node_4, section)
member_4 = Member(node_4, node_5, section)
# Define Beam
beam = Beam()
# Add Node Loads
node_2.force = Force(-10)
node_3.moment = Moment(-50)
# Add Member Loads
member_1.forces = [10, Force(-30)]
member_1.forces = [20, Force(-10)]
member_2.distributed_loads = [0, DistributedForce(-.1, -.1, 90)]
member_3.distributed_loads = [20, DistributedForce(-.1, -.2, 75)]
member_4.distributed_loads = [0, DistributedForce(-.05, -.05, 96)]
member_4.moments = [48, Moment(100)]
# Add Restrains
node_1.restrains = [True, True]
node_3.restrains = [True, False]
node_4.restrains = [True, False]
node_5.restrains = [True, True]
# Add Members to Beam Object
beam.members = member_1
beam.members = member_2
beam.members = member_3
beam.members = member_4
beam.solve()
print(beam.reactions)
```

### Truss Example

```python
"""
Integrated Matrix Analysis of Structures, Mario Paz & William Leigh
Illustrative Example 6.1, pp 207
"""
# Import modules
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.truss import *
# Define Material and Section
material = Material(E=30e3, f_y=1, f_u=1)
section = Section(A=10, Ix=882, material=material)
# Define Nodes
node_1 = Node((0, 0))
node_2 = Node((100, 0))
node_3 = Node((0, 100))
# Define Members
member_1 = Member(node_1, node_2, section)
member_2 = Member(node_1, node_3, section)
member_3 = Member(node_3, node_2, section)
# Define Beam
truss = Truss()
# Add Node Loads
node_3.force = Force((10, 0))
# Add Restrains
node_1.restrains = [True, True]
node_2.restrains = [False, True]
# Add Members to Beam Object
truss.members = member_1
truss.members = member_2
truss.members = member_3
truss.solve()
print(truss.reactions)
```

### Frame Example

```python
# Import Modules
from stiffpy.material import Material
from stiffpy.section import Section
from stiffpy.frame import *
# Define Material
material = Material(E=2e7, f_y=1, f_u=1)
# Define Section
section = Section(A=11.8*0.0254**2, Ix=518*0.0254**4, material=material)
# Define Frame Object
frame = Frame()
# Define Nodes
node_1: Node = Node([0, 0])
node_2: Node = Node([0, 10])
node_3: Node = Node([5, 10])
node_4: Node = Node([10, 10])
node_5: Node = Node([15, 5])
node_6: Node = Node([5, 5])
# Define Members
member_1 = Member(node_1, node_2, section)
member_2 = Member(node_2, node_3, section)
member_3 = Member(node_3, node_4, section)
member_4 = Member(node_4, node_5, section)
member_5 = Member(node_3, node_6, section)
# Add Actions
member_1.distributed_loads = [0, DistributedForce([0, -10], [0, -10], 10)]
member_2.distributed_loads = [0, DistributedForce([0, -10], [0, -10], 5)]
member_3.distributed_loads = [0, DistributedForce([0, -10], [0, -10], 5)]
member_4.distributed_loads = [0, DistributedForce([10/2**0.5, -10/2**0.5],
    [10/2**0.5, -10/2**0.5], 5*2**0.5)]
# Add Restrains
node_1.restrains = [True, True, True]
node_5.restrains = [True, True, True]
node_6.restrains = [True, True, True]
# Add Members to Frame Objects
frame.members = member_1
frame.members = member_2
frame.members = member_3
frame.members = member_4
frame.members = member_5
# Solve
frame.solve()
print(frame.reactions)
frame.draw_deformations(20)
```

---

## Todo's

* Deformed shape error
* Instead of using a vector for the rotation of the local coordinates, use euler angles.
* Improve typing

---
## About
```
Developer: Eduardo Paolo Oros
Email: eduardoom_@outlook.com
```
