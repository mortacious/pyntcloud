import sys
import numpy as np
import pandas as pd
from pycloud.io.external import PlyElement, PlyData

ply_dtypes = dict([
    (b'int8', 'i1'),
    (b'char', 'i1'),
    (b'uint8', 'u1'),
    (b'uchar', 'b1'),
    (b'uchar', 'u1'),
    (b'int16', 'i2'),
    (b'short', 'i2'),
    (b'uint16', 'u2'),
    (b'ushort', 'u2'),
    (b'int32', 'i4'),
    (b'int', 'i4'),
    (b'uint32', 'u4'),
    (b'uint', 'u4'),
    (b'float32', 'f4'),
    (b'float', 'f4'),
    (b'float64', 'f8'),
    (b'double', 'f8')
])


def read_ply(filename, fields=None, ignore_missing=True):
    """
    Read a .ply (binary or ascii) file and store the elements in pandas DataFrame
    Parameters.

    Parameters
    ----------
    filename: str
        Path to the file
    fields: list[str]
        List of the field names to load from the file.
        default: None = all fields in the file
    ignore_missing: boolean
        Ignore missing fields in the fields list

    Returns
    -------

    data: dict
        Elements as pandas DataFrames; comments and ob_info as list of string

    """
    with open(filename, 'rb') as ply:
        cloud = PlyData.read(ply)
    cloud_fields = [p.name for p in cloud['vertex'].properties]
    if fields is None:
        fields = cloud_fields # load all
    elif isinstance(fields, str):
        fields = [fields]

    if not set(fields).issubset(cloud_fields) and not ignore_missing:
        raise ValueError("fields %s not in file".format(set(fields).difference(cloud_fields)))

    data = {"points": pd.DataFrame(cloud['vertex'][fields])}

    return data


def write_ply(filename, points, fields=None, ascii=False, byte_order='<'):
    """
    Write a ply file from a pandas dataframe

    Parameters
    ----------
    filename: str
        The created file will be named with this
    points: pd.dataframe
        The points to write into the file
    fields: list
        List of fields to write into the file. default:None = all fields
    ascii:
        Ascii or binary mode
    byte_order:
        The byte order of the created file. default: little endian

    Returns
    -------
    True if no problems
    """

    if not filename.endswith('ply'):
        filename += '.ply'

    # get fields to write
    cloud_fields = points.columns
    if fields is None:
        fields = cloud_fields  # save all
    elif isinstance(fields, str):
        fields = [fields]

    # get dtypes
    dtypes = __describe_elements(points, fields)

    vert = PlyElement.describe(np.core.records.fromarrays(points[fields].values.T, names=fields, formats=dtypes), 'vertex')

    PlyData([vert], text=ascii, byte_order=byte_order).write(filename)

    return True


def __describe_elements(df, fields):
    """
    Takes the columns of the dataframe and builds a description for a numpy structured array

    Parameters
    ----------
    df: pd.dataframe
        The dataframe to build a description of
    fields: list
        The fields to consider

    Returns
    -------
    Description string of the dataframe in numpy record format
    """

    dtypes = [ply_dtypes[dtype] for name, dtype in zip(df.columns, df.dtypes) if name in fields]
    return ','.join(dtypes)