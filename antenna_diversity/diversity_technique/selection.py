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


def calculate_power(signal_array: np.ndarray) -> float:
    # the typical physical implementation of selection only uses x number bits
    # using same default of 4 bits, and oversamplerate of 32 as the default
    # for gfsk is set to 32
    # Calculation is from page 160 in wireless communication systems in matlab
    signal_abs_squared = np.square(np.abs(signal_array))
    return 1 / len(signal_array) * np.sum(signal_abs_squared)


def selection_from_power(signal_matrix: np.ndarray,
                         nr_bits: int = 4,
                         over_sample_rate: int = 32) -> t.Tuple[t.Any, int]:
    """
        Signal_matrix is a N x M signal where N is the number of branches and M is the signal places,
        such for example that the signal[1] gives a array of M elements

        This function uses the power of the signal to choose which branch to use
        nr_bits is the amount of bits to use for calculating the signal power
        over_sample_rate is the oversamplerate used to make the baseband representation in the gfsk module

        nr_bits = 4 is set as it is the common number of bits used in physical devices
        over_sample_rate = 32 is the same deafault as the gfsk module

        returns the signal y after selection and the index of the chosen h i.e. the chosen branch
    """
    sh = np.shape(signal_matrix)
    signal_powers = np.empty(shape=(sh[0]))
    for i, signal_row in enumerate(signal_matrix):
        signal_powers[i] = calculate_power(
            signal_row[: int(nr_bits * over_sample_rate)])

    index = np.argmax(signal_powers)
    return signal_matrix[index], int(index)


class CRCSelection:
    def __init__(self, branches: int):
        self.branches = branches
        self.last_good = True
        self.selected = 0

    def report_crc_status(self, good: bool):
        if not good:
            self.selected = (self.selected + 1) % self.branches

    def select(self, signal_matrix: np.ndarray) -> t.Tuple[np.ndarray, int]:
        return signal_matrix[self.selected], self.selected


# Range Enhancer Negative Erasure Diffential or R.E.N.E. Dif.

class ReneDif:
    def __init__(self):
        """
        #init internal variables
        """
        self.last_power = 0
        self.chosen_branch = 0
        self.received = 0
        self.nr_bits = 4
        self.over_sample_rate = 32

    def select(self, signal_matrix: np.ndarray) -> t.Tuple[np.ndarray, int]:
        """
        Compares the power of the last signal with the power
        of the current signal on the current branch.
        Selection diversity is used if the signal power
        of the current branch is lower than the last signal power.
        """   
        new_power = calculate_power(
            signal_matrix[self.chosen_branch]
            [:int(self.nr_bits * self.over_sample_rate)])
        if new_power >= self.last_power:
            self.last_power = calculate_power(
                signal_matrix[self.chosen_branch])
            return signal_matrix[self.chosen_branch], self.chosen_branch
        else:
            recieved, self.chosen_branch = selection_from_power(signal_matrix)
            self.last_power = calculate_power(recieved)
            return recieved, self.chosen_branch

