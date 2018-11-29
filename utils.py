def save(multitrack, filename, compressed=True):
    """
    Save the multitrack pianoroll to a (compressed) npz file, which can be
    later loaded by :meth:`pypianoroll.Multitrack.load`.

    Notes
    -----
    To reduce the file size, the pianorolls are first converted to instances
    of scipy.sparse.csc_matrix, whose component arrays are then collected
    and saved to a npz file.

    Parameters
    ----------
    filename : str
        The name of the npz file to which the mulitrack pianoroll is saved.
    compressed : bool
        True to save to a compressed npz file. False to save to an
        uncompressed npz file. Defaults to True.

    """

    def update_sparse(target_dict, sparse_matrix, name):
        """Turn `sparse_matrix` into a scipy.sparse.csc_matrix and update
        its component arrays to the `target_dict` with key as `name`
        suffixed with its component type string."""
        csc = csc_matrix(sparse_matrix)
        target_dict[name + '_csc_data'] = csc.data
        target_dict[name + '_csc_indices'] = csc.indices
        target_dict[name + '_csc_indptr'] = csc.indptr
        target_dict[name + '_csc_shape'] = csc.shape

    multitrack.check_validity()
    array_dict = {'tempo': multitrack.tempo}
    info_dict = {'beat_resolution': multitrack.beat_resolution,
                 'name': multitrack.name}

    if multitrack.downbeat is not None:
        array_dict['downbeat'] = multitrack.downbeat

    for idx, track in enumerate(multitrack.tracks):
        update_sparse(array_dict, track.pianoroll,
                      'pianoroll_{}'.format(idx))
        info_dict[str(idx)] = {'program': track.program,
                               'is_drum': track.is_drum,
                               'name': track.name}

    if not filename.endswith('.npz'):
        filename += '.npz'
    if compressed:
        np.savez_compressed(filename, **array_dict)
    else:
        np.savez(filename, **array_dict)

    compression = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
    with zipfile.ZipFile(filename, 'a') as zip_file:
        zip_file.writestr('info.json', json.dumps(info_dict), compression)