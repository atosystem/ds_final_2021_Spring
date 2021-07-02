class Node():
    def __init__(self,v,_parent=None):
        self.value = v
        self.parent = _parent
        self.children = {}
        self.mark = 0
        self.weight = 0

class AddressNode(Node):
    def __init__(self,address_part,_count=1,_parent=None):
        super().__init__(v=address_part,_parent=_parent)
        self.accum_count = _count
    def __str__(self):
        return ("[AddressNode] mark#{} addr_part={} accum_count={} ".format(self.mark,self.value,self.accum_count))


class Person(Node):
    def __init__(self,person_name,entire_address,_parent=None):
        super().__init__(v=person_name,_parent=_parent)
        self.entire_address = entire_address
    def __str__(self):
        return ("[Person] mark#{} name={} addr={} ".format(self.mark,self.value,"->".join(self.entire_address)))

class trie():
    def __init__(self):
        # root node
        self.root = AddressNode('_')
        self.accum_mark_threshold = 1
        self.people = []

    def insert(self,person):
        current_node  = self.root
        for addr_part in person['address']:
            if  addr_part in current_node.children and type(current_node.children[addr_part]) == AddressNode:
                current_node.accum_count += 1
                current_node = current_node.children[addr_part]
            else:
                current_node.children[addr_part] = AddressNode(addr_part,_parent=current_node)
                current_node = current_node.children[addr_part]
        
        self.people.append(Person(person_name=person['name'],entire_address=person['address'],_parent=current_node))
        current_node.children[person['name']] = self.people[-1]

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

    def fetchAllSubNode(self,_addr_node,mark_threshold=1,_weight=1):
        # node with mark >= 1 are consider unvisted
        temp_list = []
        temp_list.append(_addr_node)
        people_fetched = []
        while(len(temp_list) > 0):
            _n = temp_list.pop()
            if  _n.mark < mark_threshold:
                # mark that the node has been visted one more time
                _n.mark += 1
                if type(_n) == AddressNode:
                    temp_list.extend(_n.children.values())
                else:
                    _n.weight += _weight
                    people_fetched.append(_n)

        return people_fetched



    def searchArea(self,person,level=0,_threshold=None):
        # level 0 = empty list return
        # level 1 = same store

        if _threshold == None:
            _threshold = self.accum_mark_threshold
            self.accum_mark_threshold += 1

        return_list = []
        people_set = set()
        person_node = self.search(person)
        person_node.weight+=100000
        current_node = person_node
        for _l in range(level):
            current_node = current_node.parent
            # print("Searching level {} at {}".format(_l,current_node.value))
            _r = self.fetchAllSubNode(current_node,mark_threshold=_threshold,_weight=8-_l)
            return_list.extend(_r)
        
        return return_list


def trie_search(sim_data):
    mytrie = trie()
    SEARCH_LEVEL = 5
    PEOPLE_LIST_TIMESTEP = 0
    import numpy as np

    
    # insert into trie
    for _person in sim_data['people_list'][PEOPLE_LIST_TIMESTEP]:
        # print({"name":_person,"address":sim_data['people_list'][_person]})
        mytrie.insert({"name":_person,"address":sim_data['people_list'][PEOPLE_LIST_TIMESTEP][_person]})

    results = []
    # search area
    print("Search")
    for _infected_person in sim_data['infected_people']:
        # print()
        # print({"name":_infected_person,"address":sim_data['people_list'][PEOPLE_LIST_TIMESTEP][_infected_person]})
        _r = mytrie.searchArea({"name":_infected_person,"address":sim_data['people_list'][PEOPLE_LIST_TIMESTEP][_infected_person]},SEARCH_LEVEL)    
        results.extend(_r)


    results = list(set(results))
    results.sort(key=lambda a:-a.weight)
    # people_names = []
    # for c in results:
        # print((c.weight,c.value , c.entire_address))
        # people_names.append((c.value , c.entire_address))
    #     people_names.extend([(c.value , c.entire_address) for c in x])
    # print("result")
    
    return [c.value for c in results]

if __name__=="__main__":
    mytrie = trie()
    SEARCH_LEVEL = 1
    import json
    import numpy as np
    with open("../raw_data/init_data.json","r") as f:
        sim_data = json.load(f)
    
    # print(sim_data)

    
    
    # insert into trie
    for _person in sim_data['people_list']:
        # print({"name":_person,"address":sim_data['people_list'][_person]})
        mytrie.insert({"name":_person,"address":sim_data['people_list'][_person]})

    results = []
    # search area
    print("Search")
    for _infected_person in sim_data['infected_people']:
        # print()
        print({"name":_infected_person,"address":sim_data['people_list'][_infected_person]})
        _r = mytrie.searchArea({"name":_infected_person,"address":sim_data['people_list'][_infected_person]},SEARCH_LEVEL)    
        results.extend(_r)

    results = list(set(results))
    results.sort(key=lambda a:-a.weight)
    people_names = []
    for c in results:
        print((c.weight,c.value , c.entire_address))
        people_names.append((c.value , c.entire_address))
    #     people_names.extend([(c.value , c.entire_address) for c in x])
    print("result")
    # for p in people_names:
    #     print(p)
    # print(people_names)

    