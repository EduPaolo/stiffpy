"""
Frame Package, this packages inherint from the classes Node, Member, Structure,
Force, Moment and DistributedForce

This new classes make easy the construction of 2D frames

No Documentation will be provided for these new classes, they are a particular
case of the base classes
"""
from .frame import Frame
from .member import Member
from .node import Node
from .action.distributed_force import DistributedForce
from .action.force import Force
from .action.moment import Moment
