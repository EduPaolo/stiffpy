"""
Truss Package, this package overwrites the class Node, Member, Structure,
Force, Moment, and DistributedForce.

These new classes make easy the construction of new trusses.

No Documentation will be provided for these new classes, they are a particular
case of the base classes
"""
from .truss import Truss
from .member import Member
from .node import Node
from .action.distributed_force import DistributedForce
from .action.force import Force
from .action.moment import Moment
