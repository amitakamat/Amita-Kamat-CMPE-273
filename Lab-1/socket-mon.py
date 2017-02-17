"""
Program to use psutil and implement a network socket monitoring tool
"""

import psutil
import numpy as np
from collections import defaultdict


class SocketConnection:
    def __init__(self, pid, localaddress, remoteaddress, status):
        self.pid = pid
        self.localaddress = localaddress
        self.remoteaddress = remoteaddress
        self.status = status

    def PrintConnections(self):

        """
            Prints and returns the connection details in csv format
        """
        connectionentry = '\n"' + str(self.pid) + '", "' + str(self.localaddress) + '", "' + str(self.remoteaddress) + '", "' + str(self.status) + '"'
        print(connectionentry)
        return connectionentry


def GetConnections():

    """
        Gets and returns all the socket connections for which local address and remote address exist
    """
    AllSocketConnections = []
    for connection in psutil.net_connections():
        if len(connection.laddr) > 0 and len(connection.raddr) > 0:
            AllSocketConnections.append(
                SocketConnection(connection.pid, str(connection.laddr[0]) + '@' + str(connection.laddr[1]),
                                 str(connection.raddr[0]) + '@' + str(connection.raddr[1]), connection.status))

    return AllSocketConnections


def GroupAndSortConnections(SocketConnections):

    """
        Groups the connections based on pid and sorts them according to the number of connections
    """
    pidgroups = defaultdict(list)
    SortedGroupedConnections = []

    for connection in SocketConnections:
        pidgroups[connection.pid].append(connection)

    for connection in sorted(pidgroups, key=lambda x: len(pidgroups[x]), reverse=True):
        pidconnectionarray = np.asarray(pidgroups[connection])
        for eachConnection in range(len(pidconnectionarray)):
            SortedGroupedConnections.append(pidconnectionarray[eachConnection])

    return SortedGroupedConnections


def PrintAllConnections(SortedGroupedConnections):

    """
        Prints the connection details in csv format on terminal and in an output file.
    """
    outputfile = open('SocketConnections', 'w')

    headerline = '\n"pid", "laddr", "raddr", "status"'
    print(headerline)
    outputfile.write(headerline)

    for connection in range(len(SortedGroupedConnections)):
        connectionentry = SortedGroupedConnections[connection].PrintConnections()
        outputfile.write(connectionentry)

SortedGroupedConnections = GroupAndSortConnections(GetConnections())
PrintAllConnections(SortedGroupedConnections)
