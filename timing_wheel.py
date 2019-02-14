class Object:
    def __init__(self, name, init_state, init_state_duration=1):
        self.name = name
        self.current_state = init_state
        self.current_state_duration = init_state_duration
        self.future_events = [] # tuple pairs of [state, duration]

    def update_state(self):
        # get state out of future events and set it as current state
        # also pop it out of future events
        new_state, new_state_duration = self.future_events.pop(0)
        self.current_state = new_state
        self.current_state_duration = new_state_duration
        print('{} state changed to {}'
            .format(self.name, self.current_state))

    def schedule_next_event(self):
        if len(self.future_events)>0:
            return self.future_events[0][1]
        else:
            return -1


class TimerWheel:
    def __init__(self, objects=[], ticks=60):
        self.ticks = ticks
        self.current_time = -1
        self.objects = objects
        self.slots = {i:[] for i in range(ticks)}
        self.__initialize_wheel()

    def __initialize_wheel(self):
        self.__tick_tock()
        for object in self.objects:
            self.slots[self.current_time+object.current_state_duration].append(object)
            print('{} - {} added to time wheel'.format(object.name, object.current_state))
            self.__process_queue()

    def simulate(self):
        while self.current_time < self.ticks - 1:
            self.__tick_tock()
            self.__process_queue()

    def __tick_tock(self):
        self.current_time += 1
        print 'Time:', self.current_time

    def __process_queue(self):
        ''' 1. Update state
            2. Schedule future events
        '''

        for object in self.slots[self.current_time]:
            # update state
            object.update_state()

        for object in self.slots[self.current_time]:
            # schedule future event
            next_event_time = object.schedule_next_event()
            if next_event_time > 0:
                self.slots[self.current_time+next_event_time].append(object)
            else:
                print('Simulation for {} complete'.format(object.name))

        self.slots[self.current_time] = []
