# Copyright 2021 Christian Schneider Pedersen <cspe18@student.aau.dk>, Helene Bach Vistisen, Julian Teule, Mikkel Filt Bengtson, Victor Büttner <beer@0x23.dk>
#
# SPDX-License-Identifier: Beerware OR MIT
from .noise import awgn, awgn_matrix
from .fading import rayleigh
import numpy as np
import math
import typing as t

# This file is for the constructed channel models
# The constructed channel models (like the RayAWGNchannel function shown below)
# can be made in this file.
# Other channel models can be made below.


class RayleighAWGNChannel:
    def __init__(self, N: int, snr: float, frame_per_block: int = 3,
                 intermediate_point: bool = True) -> None:
        """
            N: number of branches for the channel
            snr: the starting SNR of the channel in dB
            frame_per_block: Number of frames per channel block,
                standard is 6 frames per block, equal to sending
                at a coherence time of 60ms
            intermediate_point: Whether to let the last fade in a block move
                towards the next block value.

            The channel is based on DECT frames, i.e. the channel
            should be updated with frame_sent()
            after each frame have been passed through the channel.
        """
        self.N = N
        self.snr = snr
        self.nr_frames_into_frame = 0
        self.frame_per_channel_block = frame_per_block
        self.h = self.__sample_rayleigh()
        self.h_next = np.empty(self.N)
        self.intermediate_point = intermediate_point

    def run(self, signal: np.ndarray) -> t.Tuple[np.ndarray, np.ndarray]:
        """
            signal: array of complex signal points
            returns: matrix that is N x len(signal) where
            N is number of branches
            The channel is a Rayleigh distributed and AWGN i.e.
            y = h*x+n
        """
        noise = awgn_matrix(self.N, len(signal), self.snr)

        # makes the outer product between the h vector and the signal vector
        h_times_signal = np.outer(self.h, signal)
        return h_times_signal + noise, self.h

    def frame_sent(self) -> None:
        """
            Method to be called after a frame have been sendt
            Must be called by the user, updates the number of frames sendt
            and updates the channel h if the number of frames sendt
            is bigger then or equal to the frames per block
        """
        self.nr_frames_into_frame += 1

        # Check if we interpolate is on and we are on the last of a block.
        # If yes we should sample the next rayleigh and make h the value in
        # between.
        if self.intermediate_point and \
                self.nr_frames_into_frame == (self.frame_per_channel_block-1):

            self.next_h = self.__sample_rayleigh()
            self.h = self.h + (self.next_h - self.h) / 2
        elif self.nr_frames_into_frame >= self.frame_per_channel_block:
            if self.intermediate_point:
                self.h = self.next_h
            else:
                self.h = self.__sample_rayleigh()
            self.nr_frames_into_frame = 0

    def __sample_rayleigh(self) -> np.ndarray:
        return np.transpose(np.random.rayleigh(
            size=self.N, scale=1 / math.sqrt(2)))

    def print_parameters(self) -> None:
        print(self.__dict__)


class RayleighAWGNChannelOld:
    def __init__(self, N: int, snr: float, frame_per_block: int = 6) -> None:
        """
            N: number of branches for the channel
            snr: the starting SNR of the channel in dB
            frame_per_block: Number of frames per channel block,
                standard is 6 frames per block, equal to sending
                at a coherence time of 60ms

            The channel is based on DECT frames, i.e. the channel
            should be updated with frame_sent()
            after each frame have been passed through the channel.
        """
        self.N = N
        self.snr = snr
        self.number_of_send_frame = 0
        self.frame_per_channel_block = frame_per_block
        self.update_h()

    def run(self, signal: np.ndarray) -> t.Tuple[np.ndarray, np.ndarray]:
        """
            signal: array of complex signal points
            returns: matrix that is N x len(signal) where
            N is number of branches
            The channel is a Rayleigh distributed and AWGN i.e.
            y = h*x+n
        """
        noise = awgn_matrix(self.N, len(signal), self.snr)

        # makes the outer product between the h vector and the signal vector
        h_times_signal = np.outer(self.h, signal)
        return h_times_signal + noise, self.h

    def frame_sent(self) -> None:
        """
            Method to be called after a frame have been sendt
            Must be called by the user, updates the number of frames sendt
            and updates the channel h if the number of frames sendt
            is bigger then or equal to the frames per block
        """
        self.number_of_send_frame += 1
        if self.number_of_send_frame >= self.frame_per_channel_block:
            self.update_h()
            self.number_of_send_frame = 0

    def update_h(self) -> None:
        """
            Method for updating the h array i.e. channel parameter
        """
        self.h = np.transpose(np.random.rayleigh(
            size=self.N, scale=1 / math.sqrt(2)))

    def print_parameters(self) -> None:
        print(self.__dict__)


def rayleigh_awgn(x, snr):
    n = len(x)
    alpha = rayleigh(n)
    W = awgn(n, snr)
    y = alpha * x + W
    return y
