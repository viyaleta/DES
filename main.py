from timing_wheel import *
import random

# create an object, states, and add a state state_queue



car = Object('Car', 'idle', 1)
car.future_events = [
    ('traveling', 4),
    ('getting gas', 3),
    ('traveling', 20),
    ('arriving', 1)
]

# bus = Object('Bus', 'departing', 10)
# bus.future_events = [
#     ('traveling', 4),
#     ('at bus stop', 1),
#     ('traveling', 3),
#     ('at bus stop', 1),
#     ('traveling', 5),
#     ('at bus stop', 3),
#     ('traveling', 1),
#     ('at bus stop', 5)
# ]
#
# human = Object('Human', 'walking', 2)
# human_states = ['walking', 'standing', 'running', 'do push ups']
# for i in range(10):
#     random_state = random.choice(human_states)
#     random_state_duration = random.randint(1,10)
#     human.future_events.append((random_state, random_state_duration))

tw = TimerWheel([car], 90)
tw.simulate()
