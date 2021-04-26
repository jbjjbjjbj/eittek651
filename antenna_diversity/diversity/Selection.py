import numpy as np
import typing as t


def selection(signal: np.ndarray,
              channel_h: np.ndarray) -> t.Tuple[t.Any, int]:
    """
        Signal is a N x M signal where N is the number of branches and M is the signal places,
        such for example that the signal[1] gives a array of M elements
        channel_h is a array of the h impulse response for each branch of the channel

        returns the signal y after selection and the index of the chosen h i.e. the chosen branch
    """
    # find the larges h and return the index (argument)
    index = np.argmax(channel_h)
    # return the signal at that index and the index.
    return signal[index], int(index)
