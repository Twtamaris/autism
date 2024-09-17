        beat_length = 200
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            # if active beat is not the last beat than go to next beat
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            # if the fucking beat if last beat than go to first beat
            else:
                active_beat = 0
                beat_changed = True