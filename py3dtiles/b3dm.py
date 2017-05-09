# -*- coding: utf-8 -*-
import struct
import numpy as np

from .tile import Tile, TileHeader, TileBody, TileType
from .gltf import GlTF

class B3dm(Tile):

    @staticmethod
    def from_glTF(gltf):
        """
        gltf : GlTF
            glTF object representing a set of objects

        Returns
        -------
        tile : Tile
        """

        tb = B3dmBody()
        tb.glTF = gltf

        th = B3dmHeader()

        t = Tile()
        t.body = tb
        t.header = th

        return t


class B3dmHeader(TileHeader):
    BYTELENGTH = 28

    def __init__(self):
        self.type = TileType.BATCHED3DMODEL
        self.magic_value = "b3dm"
        self.version = 1
        self.tile_byte_length = 0
        self.ft_json_byte_length = 0
        self.ft_bin_byte_length = 0
        self.bt_json_byte_length = 0
        self.bt_bin_byte_length = 0
        self.bt_length = 0  # number of models in the batch

    def to_array(self):
        header_arr = np.fromstring(self.magic_value, np.uint8)

        header_arr2 = np.array([self.version,
                                self.tile_byte_length,
                                self.ft_json_byte_length,
                                self.ft_bin_byte_length,
                                self.bt_json_byte_length,
                                self.bt_bin_byte_length,
                                self.bt_length], dtype=np.uint32)

        return np.concatenate((header_arr, header_arr2.view(np.uint8)))

    def sync(self, body):
        """
        Allow to synchronize headers with contents.
        """

        # extract array
        glTF_arr = body.glTF.to_array()
        #bth_arr = body.batch_table.header.to_array()
        #btb_arr = body.batch_table.body.to_array()

        # sync the tile header with feature table contents
        self.magic_value = "b3dm"
        self.tile_byte_length = len(glTF_arr) + B3dmHeader.BYTELENGTH #+ len(bth_arr) + len(btb_arr)
        #self.bt_json_byte_length = len(bth_arr)
        #self.bt_bin_byte_length = len(btb_arr)
        #self.bt_length = ???

    @staticmethod
    def from_array(array):
        """
        Parameters
        ----------
        array : numpy.array

        Returns
        -------
        h : TileHeader
        """

        h = PntsHeader()

        if len(array) != PntsHeader.BYTELENGTH:
            raise RuntimeError("Invalid header length")

        h.magic_value = "b3dm"
        h.version = struct.unpack("i", array[4:8])[0]
        h.tile_byte_length = struct.unpack("i", array[8:12])[0]
        h.ft_json_byte_length = struct.unpack("i", array[12:16])[0]
        h.ft_bin_byte_length = struct.unpack("i", array[16:20])[0]
        h.bt_json_byte_length = struct.unpack("i", array[20:24])[0]
        h.bt_bin_byte_length = struct.unpack("i", array[24:28])[0]
        h.bt_length = struct.unpack("i", array[28:32])[0]

        h.type = TileType.BATCHED3DMODEL

        return h

class B3dmBody(TileBody):
    def __init__(self):
        #self.batch_table = BatchTable()
        self.glTF = GlTF()

    def to_array(self):
        # TODO : export batch table
        return self.glTF.to_array()

    @staticmethod
    def from_glTF(th, glTF):
        """
        Parameters
        ----------
        th : TileHeader

        glTF : GlTF

        Returns
        -------
        b : TileBody
        """

        # build tile body
        b = B3dmBody()
        b.glTF = glTF

        return b
