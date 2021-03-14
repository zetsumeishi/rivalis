REGION_CHOICES = (
    ('br', 'BR'),
    ('eune', 'EUNE'),
    ('euw', 'EUW'),
    ('lan', 'LAN'),
    ('las', 'LAS'),
    ('na', 'NA'),
    ('oce', 'OCE'),
    ('tr', 'TR'),
    ('jp', 'JP'),
    ('kr', 'KR'),
)


# Tournament sizes
# [(4, 4), (8, 8), (16, 16), ...]
SIZE_CHOICES = [(2 ** i, 2 ** i) for i in range(2, 12, 1)]

# Number of rounds depending on the number of participants
# {4: 2, 8: 3, 16: 4, 32: 5, ...}
SIZES_ROUNDS = {2 ** i: j for i, j in zip(range(2, 10), range(2, 10))}

NB_MATCHES_PER_ROUND_LB = {2: 1, 4: 2, 8: 2, 16: 2, 32: 4, 64: 4, 128: 5, 256: 5}

SINGLE_ELIMINATION = 'single elimination'
DOUBLE_ELIMINATION = 'double elimination'

STAGE_FORMAT_CHOICES = (
    (SINGLE_ELIMINATION, SINGLE_ELIMINATION.title()),
    (DOUBLE_ELIMINATION, DOUBLE_ELIMINATION.title()),
)

# TournamentMembership
WAITING = 'waiting'
ACCEPTED = 'accepted'
REJECTED = 'rejected'

STATUS_CHOICES = (
    (WAITING, WAITING.title()),
    (ACCEPTED, ACCEPTED.title()),
    (REJECTED, REJECTED.title()),
)
