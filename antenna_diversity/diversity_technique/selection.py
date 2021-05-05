import numpy as np
import typing as t


def selection_from_h(signal: np.ndarray,
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


def calculate_power(signal_array: np.ndarray, numb_bits, over_sample_rate):
    # first cut out numb_bits of signal_array.
    # the typical physical implementation of selection only uses x number bits
    # using same deafault of 4 bits, and oversampelrate of 32 as the deafault
    # for gfsk is set to 32
    # Calculation is from page 160 in wireless communication systems in matlab
    signal_part = signal_array[0: int(numb_bits * over_sample_rate)]
    signal_abs_sqaured = np.square(np.abs(signal_part))
    return 1 / len(signal_part) * np.sum(signal_abs_sqaured)


def selection_from_power(signal_matrix: np.ndarray,
                         numb_bits: int = 4,
                         over_sample_rate: int = 32) -> t.Tuple[t.Any,
                                                                int]:
    """
        Signal_matrix is a N x M signal where N is the number of branches and M is the signal places,
        such for example that the signal[1] gives a array of M elements

        This function uses the power of the signal to choose which branch to use
        numb_bits is the amount of bits to use for calculating the signal power
        over_sample_rate is the oversamplerate used to make the baseband representation in the gfsk module

        numb_bits = 4 is set as it is the common number of bits used in physical devices
        over_sample_rate = 32 is the same deafault as the gfsk module

        returns the signal y after selection and the index of the chosen h i.e. the chosen branch
    """
    sh = np.shape(signal_matrix)
    signal_powers = np.empty(shape=(sh[0]))
    for i, signal_row in enumerate(signal_matrix):
        signal_powers[i] = calculate_power(
            signal_row,
            numb_bits=numb_bits,
            over_sample_rate=over_sample_rate)
    index = np.argmax(signal_powers)
    return signal_matrix[index], int(index)
