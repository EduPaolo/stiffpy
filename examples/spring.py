from stiffpy.spring import *


def main():
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
    members = [member_1, member_2]
    spring.members = members
    spring.solve()
    print(spring.reactions)


if __name__ == '__main__':
    main()
