datastore = {
    'oxigen': 100,
}


def get_all():
    return datastore


def get(key):
    return datastore.get(key)


def set(key, value):
    print('{} = {}'.format(key, value))
    datastore[key] = value
