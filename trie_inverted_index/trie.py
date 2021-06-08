class Node():
    def __init__(self,c):
        self.char = ''
        self.parent = None
        self.children = {}

class trie():
    def __init__(self):
        # root node
        self.root = Node('_')

    def insert(self,name,mapping=None):
        name = name.lower()
        current_node  = self.root
        for c_name in name:
            if  c_name in current_node.children:
                current_node = current_node.children[c_name]
            else:
                current_node.children[c_name] = Node(c_name)
                current_node.children[c_name].parent = current_node
                current_node = current_node.children[c_name]
        
        current_node.children["EOS"] = mapping

    def search(self,name):
        name = name.lower()
        current_node = self.root
        for c_name in name:     
            if  c_name in current_node.children:
                current_node = current_node.children[c_name]
            else:
                return None
        if "EOS" in current_node.children:
            return current_node.children["EOS"]
        else:
            return None


if __name__=="__main__":
    mytrie = trie()
    import json
    import numpy as np
    with open("data_generating/random_data.json","r") as f:
        random_data = json.load(f)

    people2ID = { x:i for i,x in enumerate(random_data["names"])}

    for i,p in enumerate(random_data["names"]):
        # print(p)
        mytrie.insert(p,i)
    

    HOUR_COUNT = len(random_data["data"])

    # print(people2ID)

    # declare a table
    people_place_table = np.zeros((len(random_data["names"]),len(random_data["places"])*HOUR_COUNT))
    # convert to bool dtype
    people_place_table = people_place_table > 0

    for hour_data_i,hour_data in enumerate(random_data["data"]):
        for place_i,place in enumerate(hour_data):
            for person in hour_data[place]:
                # print(person)
                people_place_table[people2ID[person],hour_data_i*len(random_data["places"])+place_i] = True
    

    target_person = ["Christine_Aguistin_Eric","Dyana_Clarence_Hodess"]

    for tp in target_person:
        print("Searching for {}".format(tp))
        mapping = mytrie.search(tp)
        if mapping == None:
            print("Person not exist")
        else:
            affected_people = []
            # print("people_place_table",people_place_table.shape)
            people_place_table_t = np.transpose(people_place_table)
            # print("people_place_table_t",people_place_table_t.shape)
            # print("mapping",mapping)
            slots_ids = np.squeeze(people_place_table[mapping])
            # print("slots_ids",slots_ids.shape)

            peoples = np.array(random_data["names"])
            hour_place_contacts = people_place_table_t[slots_ids] 
            # print("hour_place_contacts",hour_place_contacts.shape)
            
            # remove the target person
            hour_place_contacts[:,mapping] = False

            for h in range((HOUR_COUNT)):
                people_selected = peoples[hour_place_contacts[h]]
                affected_people.extend(people_selected)
            
            affected_people = set(affected_people)
            
            print("Affected people :",affected_people)
            print("="*30)