def find_connected_sinks(file_address):
    '''
    Function that finds the connected sinks.
    This function has two helper functions:
     -   create_grid
     -   stream
    '''
    PIPE_DIRECTION = {  
        '═': ['E', 'W' ], 
        '║': ['N' , 'S'],
        '╔': ['S' , 'E' ],
        '╗': ['S', 'W' ],
        '╚': ['N', 'E' ],
        '╝': ['W', 'N'],
        '╠': ['N', 'S', 'E' ],
        '╣': ['N', 'S', 'W' ],
        '╦': ['W', 'E', 'S' ],
        '╩': ['W', 'E', 'N' ],
    }

    PIPE_DIR_OPP = {
        'N': 'S',
        'S': 'N',
        'E': 'W',
        'W': 'E'
    }

    # Mutable variables used across the function
    connected_sinks = []
    seen, grid      = None, None
    max_y, max_x    = 0, 0

    def create_grid(file_address):
        '''
        This will create the grid
        from the file's directions.
        '''
        nonlocal seen,  grid 
        nonlocal max_y, max_x  

        direct = []
        file   = open(file_address,'r')

        for line in file:
            line = line.strip()
            arr  = line.split(' ')
            
            arr[1] = int(arr[1])
            max_x  = arr[1] if arr[1] > max_x else max_x 
            arr[2] = int(arr[2])
            max_y  = arr[2] if arr[2] > max_y else max_y

            direct.append(arr)    

        grid  = [[None]  * (max_x + 1) for i in range(max_y + 1)]
        seen  = [[False] * (max_x + 1) for i in range(max_y + 1)]
        

        for line in direct:
            grid[abs(line[2] - max_y)][abs(line[1])] = line[0]
            
            if line[0] == '*':
                source = [abs(line[2] - max_y), abs(line[1])]

        return source


    def stream(y, x, coming):
        '''
        Recursive function that will get the breadth and add
        the sinks that are seen to the connected_sinks list.
        '''
        nonlocal seen, grid, connected_sinks
        nonlocal max_y, max_x  

        if y > max_y or x > max_x or y < 0 or x < 0 or grid[y][x] == None:
            return 

        elif seen[y][x] == True:
            return 
        
        val = grid[y][x]
        
        if val.isalpha() or val == '*':
            seen[y][x] = True
            if val != '*':
                connected_sinks.append(val)

            return [[] if coming == 'N' else stream(y+1,x,'S'), 
                    [] if coming == 'S' else stream(y-1,x,'N'),
                    [] if coming == 'W' else stream(y,x+1,'E'),
                    [] if coming == 'E' else stream(y,x-1,'W')]

        elif val in PIPE_DIRECTION:
            # Check if it can get in
            if not PIPE_DIR_OPP[coming] in PIPE_DIRECTION[val]:
                return 
            seen[y][x] = True

            return [[] if coming == 'N' or not 'S' in PIPE_DIRECTION[val] else stream(y+1,x,'S'), 
                    [] if coming == 'S' or not 'N' in PIPE_DIRECTION[val] else stream(y-1,x,'N'),
                    [] if coming == 'W' or not 'E' in PIPE_DIRECTION[val] else stream(y,x+1,'E'),
                    [] if coming == 'E' or not 'W' in PIPE_DIRECTION[val] else stream(y,x-1,'W')]

        else:
            return 

    # The code starts here
    source = create_grid(file_address)
    stream(source[0], source[1], 'START')

    connected_sinks.sort()

    result = ''
    for i in connected_sinks:
        result += i

    return result