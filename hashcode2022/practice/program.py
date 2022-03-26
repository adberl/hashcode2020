inputs = {
    "example":"input_data/a_an_example.in.txt", 
    "basic":"input_data/b_basic.in.txt",
    "coarse":"input_data/c_coarse.in.txt",
    "difficult":"input_data/d_difficult.in.txt",
    "elaborate":"input_data/e_elaborate.in.txt",
    }

def read_file(file):
    input = inputs[file]
    clients = [i.rstrip() for i in open(input, 'r').readlines()]
    clients.pop(0)
    return clients

def add_clients(clients):
    client_data = []
    for i in range(0, len(clients)-1, 2):
        c_likes = clients[i].split(' ')
        c_dislikes = clients[i+1].split(' ')
        c_likes.pop(0)
        c_dislikes.pop(0)
        cl = Client(c_likes, c_dislikes)
        client_data.append(cl)
    return client_data

class Client:

    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes
        self.conflicts = []

    @classmethod
    def add_conflict(cls, c1, c2):
        c1.conflicts.append(c2)
        c2.conflicts.append(c1)

    @classmethod
    def remove_conflict(cls, c1, c2):
        c1.conflicts.remove(c2)
        c2.conflicts.remove(c1)

    @classmethod
    def remove_client(cls, clients, client):
        for clt in clients:
            if client in clt.conflicts:
                clt.conflicts.remove(client)
        clients.remove(client)

    @classmethod
    def has_conflict(cls, c1, c2):
        if c1.dislikes == [] and c2.dislikes == []:
            return False
        for ing in c1.dislikes:
            if ing in c2.likes:
                return True
        for ing in c2.dislikes:
            if ing in c1.likes:
                return True
        return False

    @classmethod
    def sort_conflicts(cls, clients):
        clients.sort(key=lambda x: len(x.conflicts), reverse=True)

    def __str__(self):
        ret_str = f"Client {str(hash(self))} | Likes: {self.likes} | Dislikes: {self.dislikes} | Conflicts {len(self.conflicts)}"
        return ret_str
		
    def __repr__(self):
        return self.__str__()


def calculate_conflicts(clients):
    added = False
    for i in range(len(clients)):
        for j in range(i+1, len(clients)):
            c1 = clients[i]
            c2 = clients[j]
            if(Client.has_conflict(c1, c2)):
                Client.add_conflict(c1, c2)
                added = True
    return added

def exist_conflicts(clients):
    for i in clients:
        if i.conflicts != []:
            return True
    return False

for name in inputs.keys():
    file = read_file(name)
    clients = add_clients(file)
    calculate_conflicts(clients)
    while True:
        if not exist_conflicts(clients):
            break
        Client.sort_conflicts(clients)
        Client.remove_client(clients, clients[0])

    pizza = set()
    for client in clients:
        pizza |= set(client.likes)

    output = open(f"output_{name}.txt", "w")
    output.write(str(len(pizza)))
    for ing in pizza:
        output.write(" " + ing) 
    print(f"FILE {name} IS DONE!")

#    for cl in clients:
#        print(cl)