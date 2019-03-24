class Object:
    def __init__(self, name, init_state, init_state_duration=1):
        self.name = name
        self.current_state = init_state
        self.current_state_duration = init_state_duration
        self.future_events = [] # tuple pairs of [state, duration]

    def update_state(self):
        # if nothing scheduled for the future, return -1
        if len(self.future_events) == 0:
            return 0

        # get state out of future events and set it as current state
        # also pop it out of future events
        new_state, new_state_duration = self.future_events.pop(0)
        self.current_state = new_state
        self.current_state_duration = new_state_duration
        print('{} state changed to {} for {} ticks'
              .format(self.name, self.current_state, self.current_state_duration))
        return self.current_state_duration

    def get_next_event(self):
        if len(self.future_events)>0:
            return self.future_events[0][1]
        else:
            return -1


class TimerWheel:
    def __init__(self, objects=[], ticks=60):
        self.ticks = ticks
        self.wheel_number = 0
        self.current_time = -1
        self.objects = objects
        self.slots = {i:[] for i in range(ticks)}
        self.__initialize_wheel()

    def __initialize_wheel(self):
        # set time to 1 = begin
        self.__tick_tock()

        for object in self.objects:
            # add object to slot of "current time + duration of current state of this object"
            self.slots[self.current_time+object.current_state_duration].append(object)
            print('{} - {} added to time wheel'.format(object.name, object.current_state))
            self.__process_queue()

    def simulate(self):
        while self.current_time < self.ticks - 1:
            self.__tick_tock()
            self.__process_queue()

    def __tick_tock(self):
        self.current_time += 1
        if len(self.slots[self.current_time])>0:
            print('Time:', self.current_time)

    def __process_queue(self):
        ''' 1. Update state
            2. Schedule future events
        '''

        # update state for each object
        for object in self.slots[self.current_time]:
            # update state
            current_state_duration = object.update_state()

        # schedule future event for each object
        for object in self.slots[self.current_time]:

            # calculate next event time = now + how long current state will last
            next_event_time = self.current_time + current_state_duration

            # add object to the slot of next event time or complete journey
            if next_event_time > self.current_time:
                self.slots[next_event_time].append(object)
            else:
                print('Simulation for {} complete'.format(object.name))

        self.slots[self.current_time] = []
