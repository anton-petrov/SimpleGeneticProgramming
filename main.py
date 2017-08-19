from gpworld import *


def print_world_state(generation, world):
    print("Best individual ", generation, ":\n")
    print("  Genome=", world.generation[0].genome, "\n")
    print("  Length=", len(world.generation[0].genome), "\n")
    print("  Fitness=", world.generation[0].fitness, "\n")
    print("--------------------------------------------------\n")

if __name__ == "__main__":
    world = GPWorld()
    generation = 0
    while world.generation[0].genome != GPWorld.SECRET_PATTERN:
        print_world_state(generation, world)
        world.next(True)
        generation += 1
    print_world_state("last", world)
    print("Solution is found!")