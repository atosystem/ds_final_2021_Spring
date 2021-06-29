class Node():
    def __init__(self,c,_parent=None):
        self.char = ''
        self.parent = _parent
        self.children = {}
        self.mark = 0

class AddressNode(Node):
    def __init__(self,address_part,_count=1,_parent=None):
        super().__init__(address_part,_parent=None)
        self.accum_count = _count


class Person(Node):
    def __init__(self,person_name,entire_address,_parent=None):
        super().__init__(person_name,_parent=None)
        self.entire_address = entire_address

class trie():
    def __init__(self):
        # root node
        self.root = AddressNode('_')
        self.accum_mark_threshold = 1

    def insert(self,person):
        current_node  = self.root
        for addr_part in person['address']:
            if  addr_part in current_node.children and type(current_node.children[addr_part]) == AddressNode:
                current_node.accum_count += 1
                current_node = current_node.children[addr_part]
            else:
                current_node.children[addr_part] = Node(addr_part,current_node)
                current_node.children[addr_part].parent = current_node
                current_node = current_node.children[addr_part]
        
        current_node.children[person['name']] = Person(person_name=person['name'],entire_address=person['address'])

    def search(self,person):
        current_node = self.root
        for addr_part in person['address']:
            if  addr_part in current_node.children and type(current_node.children[addr_part]) == AddressNode:
                current_node = current_node.children[addr_part]
            else:
                return None
        if person['name'] in current_node.children and type(current_node.children[person['name']]) == Person:
            return current_node.children[person['name']]
        else:
            return None

    def fetchAllSubNode(self,_addr_node,mark_threshold=1):
        # node with mark >= 1 are consider unvisted
        temp_list = [_addr_node]
        while(len(temp_list) > 0):
            _n = temp_list.pop()
            if type(_n) == AddressNode and _n.mark < mark_threshold:
                # mark that the node has been visted one more time
                _n.mark += 1
                temp_list.extend(_n.children)
        
        return temp_list



    def searchArea(self,person,level=0,_threshold=None):
        # level 0 = empty list return
        # level 1 = same store

        if _threshold == None:
            _threshold = self.accum_mark_threshold
            self.accum_mark_threshold += 1

        return_list = []
        person_node = self.search(person)

        for _l in range(level):
            current_node = person_node.parent
            return_list.append(self.fetchAllSubNode(current_node,mark_threshold=_threshold))
        
        return return_list


if __name__=="__main__":
    mytrie = trie()
    SEARCH_LEVEL = 2
    import json
    import numpy as np
    with open("../test/input.json","r") as f:
        sim_data = json.load(f)
    
    print(sim_data)
    
    # insert into trie
    for _person in sim_data['people_list']:
        mytrie.insert({"name":_person,"address":sim_data['people_list'][_person]})

    results = []
    # search area
    for _infected_person in sim_data['infected_people']:
        _r = mytrie.searchArea(_infected_person,SEARCH_LEVEL)    
        results.append(_r)


    