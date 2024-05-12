class GPSNode():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def calc_dis(node1:GPSNode, node2:GPSNode):
    '''
    Given 2 GPS nodes, return the distance between them.
    '''
    pass

def log_gps(node:GPSNode, name = None, time = None, fname = 'gps_log.json'):
    '''
    Given a GPS node, log the GPS node into the following format.

    [
        {
            "index", <INDEX_OF_LOG>,
            "x": <GPS_LOCATION_X>,
            "y": <GPS_LOCATION_Y>,
            "z": <GPS_LOCATION_Z>,
            "name": <NAME_OF_NEAREST_LOC>,
            "time": <TIME_OF_LOG>
        }
    ]

    Every 1 second, this function is called.
    '''
    pass

def get_nearest_loc(node:GPSNode):
    '''
    Given a GPS node, return the nearest node.

    Add more parameters to the function if needed.
    '''
    pass

