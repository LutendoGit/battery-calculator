# practice & TO DO LIST

# First to do: practice the cycle estimator class and its methods

# creating cycleEstimator class 

class lifecycleEstimator():
     def __init___(self):
        # base_life_cycle Dictionary
        self.base_life_cycle = {
            "LiFePO4":2000,
            "Li-ion": 500,


        }
        

        self.dod_multiplier = {
            "100":1.0,
            "80" :1.5,
            "60": 2.0
        }
     def estimate(self,chemistry:str,dod:int):
         base = self.base_life_cycle.get(chemistry,2000)
         multiplier = self.dod_multiplier.get(dod,1.0)
         return int(base * multiplier)
     