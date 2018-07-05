import pandas as pd


def read_ascii(filename, names=("x", "y", "z"), **kwargs):
    """Read an ascii file and store elements in pandas DataFrame.

    Parameters
    ----------
    filename: str
        Path to the filename
    names: list[str]
        Names to load from the file. Must include "x", "y" and "z"
    kwargs: pandas.read_csv supported kwargs
        Check pandas documentation for all possibilities.
    Returns
    -------
    data: dict
        Elements as pandas DataFrames.
    """

    if not {"x", "y", "z"}.issubset(names):
        raise ValueError("Required fields 'x','y','z' not in names")
    data = {}
    data["points"] = pd.read_csv(filename, names=names, **kwargs)

    return data


def write_ascii(filename, points, mesh=None, **kwargs):
    """Write points (and optionally mesh) content to filename.

    Parameters
    ----------
    filename: str
        Path to output filename
    points: pd.DataFrame
        Points data
    mesh: pd.DataFrame or None, optional
        Default: None
        If not None, 2 files will be written.

    kwargs: see pd.DataFrame.to_csv

    Returns
    -------
    bool
    """

    points.to_csv(filename, **kwargs)

    if mesh is not None:
        mesh.to_csv("mesh_{}".format(filename), **kwargs)
    return True
