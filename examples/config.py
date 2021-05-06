
class Collection:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


ber_over_snr = Collection(
    bits_per_slot=440,
    slot_per_frame=1,
    give_up_value=1e-6,
    # How many bits to aim for at give_up_value
    certainty=20,
    # Stop early at x number of errors. Make sure to scale together with
    # slots_per_frame, as this number number must include several different
    # h values.
    stop_at_errors=100000,
    snr_stop=100,
    snr_step=1,
    branches=10
)

