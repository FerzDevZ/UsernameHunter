def is_valid_username(username, platform=None):
    import re
    if not (3 <= len(username) <= 32):
        return False, 'Username harus 3-32 karakter'
    if ' ' in username:
        return False, 'Username tidak boleh mengandung spasi'
    if not re.match(r'^[A-Za-z0-9_.-]+$', username):
        return False, 'Username hanya boleh huruf, angka, underscore, dash, titik'
    if platform == 'Twitter' and len(username) > 15:
        return False, 'Username Twitter max 15 karakter'
    if platform == 'Instagram' and not re.match(r'^[A-Za-z0-9_.]+$', username):
        return False, 'Username Instagram hanya huruf, angka, underscore, titik'
    return True, ''
