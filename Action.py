class Action:
    def __init__(self, vertix_start, vertix_end):
        self.edge_start = vertix_start
        self.edge_end =vertix_end

class ActionDA(Action):
    def __init__(self, vertix_start, vertix_end):
        super().__init__(vertix_start, vertix_end)
        self.new_path_length = float('inf')
        self.previous_length = float('inf')
    
    def update_path_length(self, length, previous_length):
        self.new_path_length: tuple[str,int] = length
        self.previous_length = previous_length