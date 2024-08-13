class Event:
    def __init__(self, current_time, arrival_time, hub_completion, red_completion, yellow_completion, green_completion,
                 white_completion, color=None):
        self.current = current_time
        self.arrival = arrival_time
        self.color = color
        self.hub_completion = hub_completion
        self.red_completion = red_completion
        self.yellow_completion = yellow_completion
        self.green_completion = green_completion
        self.white_completion = white_completion
