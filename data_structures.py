import data_tracker

data_tracker.data_structure_add(
    "pos_ts",
    [
        ('x', 'f8'),
        ('y', 'f8'),
        ('z', 'f8'),
        ('ts_grab', 'i8'),
        ('ts_infer', 'i8'),
        ('ts_publish', 'i8')
    ],
    [
        '%.16f',
        '%.16f',
        '%.16f',
        '%d',
        '%d',
        '%d'
    ]
)
