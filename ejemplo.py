import simpy


def ejemplo(env):
    while True:
        print("Evento en el tiempo {}".format(env.now))
        yield env.timeout(24)


env = simpy.Environment()
env.process(ejemplo(env))
env.run(until=100)