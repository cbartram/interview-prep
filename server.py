import string
from collections import defaultdict
# You're running a pool of servers where the servers are numbered sequentially starting from 1. Over time, any given server might explode, in which case its server number is made available for reuse. When a new server is launched, it should be given the lowest available number.

# Write a function which, given the list of currently allocated server numbers, returns the number of the next server to allocate. In addition, you should demonstrate your approach to testing that your function is correct. You may choose to use an existing testing library for your language if you choose, or you may write your own process if you prefer.

# For example, your function should behave something like the following:

#   >> next_server_number([5, 3, 1])
#   2
#   >> next_server_number([5, 4, 1, 2])
#   3
#   >> next_server_number([3, 2, 1])
#   4
#   >> next_server_number([2, 3])
#   1
#   >> next_server_number([])
#   1
#   >> next_server_number([1,1.5,2,2.5,3,3.5,4,5,5.5])
#   6
#   >> next_server_number([2.5])


def next_server_number(servers: list) -> int:
    if not servers or len(servers) == 0:
        return 1

    for i in range(1, max(servers)): # [1, 2, 3, 4, 5]
        if i not in servers:
            return i

    return max(servers) + 1

# Server names consist of an alphabetic host type (e.g. "apibox") concatenated with the server number,
# with server numbers allocated as before (so "apibox1", "apibox2", etc. are valid hostnames).

# Write a name tracking class with two operations, allocate(host_type) and deallocate(hostname).
# The former should reserve and return the next available hostname, while the latter should release that hostname back into the pool.

# For example:

# >> tracker = Tracker()
# >> tracker.allocate("apibox")
# "apibox1"
# >> tracker.allocate("apibox")
# "apibox2"
# >> tracker.deallocate("apibox1")
# nil
# >> tracker.allocate("apibox")
# "apibox1"
# >> tracker.allocate("sitebox")
# "sitebox1
# >> tracker.allocate("#$@%")


class Tracker:
    def __init__(self):
        self.servers = defaultdict(list)

    def allocate(self, server_name):
        if server_name in self.servers:
            next = next_server_number(self.servers[server_name])
            self.servers[server_name].append(next)
            return server_name + str(next)
        else:
            self.servers[server_name] = [1]
            return server_name + "1"

    def deallocate(self, server_name):
        last = 0
        for i, char in enumerate(server_name):
            if char in string.ascii_letters:
                last = i

        name = server_name[0:last + 1]
        num = server_name[last + 1::]
        self.servers[name].remove(int(num))
        print(self.servers)
        return None

if __name__ == "__main__":
    t = Tracker()
    print(t.allocate("apibox"))
    print(t.allocate("apibox"))
    print(t.allocate("apibox"))
    print(t.allocate("apibox"))
    print(t.allocate("apibox"))
    print(t.deallocate("apibox4"))
    print(t.deallocate("apibox3"))
    print(t.deallocate("apibox2"))