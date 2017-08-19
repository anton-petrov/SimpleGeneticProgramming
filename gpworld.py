import random
from individual import *


class GPWorld:
    SECRET_PATTERN = """To be, or not to be, that is the question;
Whether 'tis nobler in the mind to suffer
The Slings and Arrows of outrageous Fortune
Or to take arms against a sea of troubles,
And by opposing, end them. To die, to sleep;
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to - 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream. Ay, there's the rub,
For in that sleep of death what dreams may come,
When we have shuffled off this mortal coil,
Must give us pause. There's the respect
That makes calamity of so long life,
For who would bear the whips and scorns of time,
Th'oppressor's wrong, the proud man's contumely,
The pangs of dispriz'd love, the law's delay,
The insolence of office, and the spurns
That patient merit of th'unworthy takes,
When he himself might his quietus make
With a bare bodkin? who would fardels bear,
To grunt and sweat under a weary life,
But that the dread of something after death,
The undiscovered country from whose bourn
No traveller returns, puzzles the will,
And makes us rather bear those ills we have
Than fly to others that we know not of?
Thus conscience does make cowards of us all,
And thus the native hue of resolution
Is sicklied o'er with the pale cast of thought,
And enterprises of great pitch and moment
With this regard their currents turn away,
And lose the name of action."""

    SECRET_PATTERN_LENGTH = len(SECRET_PATTERN)
    generation = []
    generation_size = 10000
    crossover_probability = 0.4
    mutation_probability = 0.2

    def __init__(self):
        self.generation = GPWorld.generate_random_generation()
        self.generation.sort(key=lambda element: element.fitness, reverse=True)
#        print(len(self.generation))
        pass

    @staticmethod
    def random_possible_char():
        chars = "abcdefghijklmnopqrstuvwxyz' ABCDEFGHIJKLMNOPQRSTUVWXYZ,;.-? \r\n"
        return chars[random.randrange(0, len(chars))]

    @staticmethod
    def calc_fitness(genome: str) -> int:
        result = 0
        genome_length = len(genome)
        max_length = max(GPWorld.SECRET_PATTERN_LENGTH, genome_length)
        min_length = min(GPWorld.SECRET_PATTERN_LENGTH, genome_length)
        for i in range(0, max_length):
            if i >= min_length or genome[i] != GPWorld.SECRET_PATTERN[i]:
                result -= 1
            else:
                result += 1
        return result

    @staticmethod
    def generate_random_generation():
        result = []
        print("Generating zero generation...\n")
        for i in range(0, GPWorld.generation_size):
            genome = ""
            length = random.randint(1, GPWorld.SECRET_PATTERN_LENGTH * 2)
            for l in range(0, length):
                genome += GPWorld.random_possible_char()
            ind = Individual(genome, GPWorld.calc_fitness(genome))
            result.append(ind)
            print("\r", i)
        print("\n")
        return result

    @staticmethod
    def crossover(genome1: str, genome2: str):
        result = ""
        pos = random.randrange(0, len(genome1))
        for i in range(0, len(genome1)):
            if i > pos:
                result += genome1[i]
            elif i < len(genome2):
                result += genome2[i]
            else:
                result += GPWorld.random_possible_char()
        return result

    @staticmethod
    def mutate(genome: str):
        if random.random() < 0.33:
            pos = random.randint(0, len(genome))
            genome = genome[0:pos] + genome[pos:]
        if len(genome) > 0 and random.random() < 0.33:
            pos = random.randrange(0, len(genome))
            genome = genome[:pos] + genome[pos + 1:]
        if len(genome) > 0 and random.random() < 0.33:
            pos = random.randrange(0, len(genome))
            new_genome = ""
            for i in range(0, len(genome)):
                if i != pos:
                    new_genome += genome[i]
                else:
                    new_genome += GPWorld.random_possible_char()
            genome = new_genome
        return genome

    def next(self, use_elitism: bool):
        new_generation = []
        if use_elitism:
            new_generation.append(self.generation[0])
        while len(new_generation) < GPWorld.generation_size:
            parent1a = random.randrange(0, GPWorld.generation_size // 2)
            parent1b = random.randrange(0, GPWorld.generation_size // 2)
            parent2a = random.randrange(0, GPWorld.generation_size // 2)
            parent2b = random.randrange(0, GPWorld.generation_size // 2)
            parent1 = min(parent1a, parent1b)
            parent2 = max(parent2a, parent2b)
            if random.random() < GPWorld.crossover_probability:
                new_genome = GPWorld.crossover(self.generation[parent1].genome, self.generation[parent2].genome)
            else:
                new_genome = self.generation[parent1].genome
            if random.random() < GPWorld.mutation_probability:
                new_genome = GPWorld.mutate(new_genome)
            ind = Individual(new_genome, GPWorld.calc_fitness(new_genome))
            new_generation.append(ind)
        new_generation.sort(key=lambda element: element.fitness, reverse=True)
        self.generation = list(new_generation)
