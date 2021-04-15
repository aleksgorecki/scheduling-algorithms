class Dict:


    def __init__(self, name: str):
        self.set = {
            'name': name,
            'johnson_c': 0,
            'johnson_t': 0,
            'neh_c': 0,
            'neh_t': 0,
            'neh1_c': 0,
            'neh1_t': 0,
            'neh2_c': 0,
            'neh2_t': 0,
            'neh3_c': 0,
            'neh3_t': 0,
            'neh4_c': 0,
            'neh4_t': 0
        }
        #self.set['name'] = name

    def getname(self):
        return self.set['name']

    def getdict(self):
        return self.set

    def setJohnson(self, johnson_c: int, johnson_t: int):
        self.set['johnson_c'] = johnson_c
        self.set['johnson_t'] = johnson_t

    def setNeh(self, neh_c: int, neh_t:float, neh1_c: int, neh1_t:float, neh2_c: int, neh2_t:float, neh3_c: int, neh3_t:float, neh4_c: int, neh4_t:float):
        self.set['neh_c'] = neh_c
        self.set['neh_t'] = neh_t
        self.set['neh1_c'] = neh1_c
        self.set['neh1_t'] = neh1_t
        self.set['neh2_c'] = neh2_c
        self.set['neh2_t'] = neh2_t
        self.set['neh3_c'] = neh3_c
        self.set['neh3_t'] = neh3_t
        self.set['neh4_c'] = neh4_c
        self.set['neh4_t'] = neh4_t
