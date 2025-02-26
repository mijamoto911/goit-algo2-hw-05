from base_bloomfilter import BloomFilter


def check_password_uniqueness(passwords, bloom_filter):
    results = {}
    for password in passwords:
        if not password or not isinstance(password, str):
            results[password] = "Invalid password format"
            continue
        if bloom_filter.check(password):
            results[password] = "Possible duplicate"
        else:
            bloom_filter.add(password)
            results[password] = "Unique"
    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(1000000, 0.01)

    # Додавання існуючих паролів
    test_passwords = ["password123", "admin123", "qwerty123"]
    for password in test_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(new_passwords_to_check, bloom)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
