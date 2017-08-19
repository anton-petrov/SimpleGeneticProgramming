class Individual:
    genome = ""
    fitness = 0

    def __init__(self, genome: str, fitness: int):
        self.genome = genome
        self.fitness = fitness
