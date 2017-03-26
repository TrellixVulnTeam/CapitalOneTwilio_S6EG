import redis

conn = redis.Redis('localhost')

user = {
    'first_name': 'Joe',
    'last_name': 'Schmoe',
    'address': {
        'street_number': '1234',
        'street_name': 'example st',
        'city': 'Ann Arbor',
        'state': 'MI',
        'zip': '48109'
    }
}

#conn.hmset('+19255486767', user)

print(conn.hgetall('+19255486767'))