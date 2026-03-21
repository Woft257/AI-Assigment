class TrafficBayesNetwork:
    def __init__(self):
        self.nodes = ['Time_Slot', 'Road_Type', 'Traffic_Level']
        self.edges = [
            ('Time_Slot', 'Traffic_Level'), 
            ('Road_Type', 'Traffic_Level')
        ]
        
        self.cpt_time_slot = {}       # P(Time_Slot)
        self.cpt_road_type = {}       # P(Road_Type)
        self.cpt_traffic = {}         # P(Traffic_Level | Time_Slot, Road_Type)

    def print_network_structure(self):
        print("--- Cấu trúc Mạng Bayes ---")
        print(f"Biến (Nodes): {self.nodes}")
        print(f"Quan hệ (Edges): {self.edges}")

    def train_probabilities(self, data):
        pass