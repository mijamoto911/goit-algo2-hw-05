import os
import time
import re
import mmh3
import random
import pandas as pd
from collections import defaultdict
from hyperloglog import HyperLogLog


def extract_ip_addresses(log_file):
    """Зчитує лог-файл та вилучає IP-адреси, ігноруючи некоректні рядки"""
    ip_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
    ip_addresses = set()
    with open(log_file, "r", encoding="utf-8") as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                ip_addresses.add(match.group())
    return list(ip_addresses)


def exact_unique_count(ip_addresses):
    """Точний підрахунок унікальних IP-адрес за допомогою set"""
    return len(set(ip_addresses))


def approximate_unique_count(ip_addresses, precision=0.01):
    """Наближений підрахунок унікальних IP-адрес за допомогою HyperLogLog"""
    hll = HyperLogLog(precision)
    for ip in ip_addresses:
        hll.add(ip)
    return len(hll)


if __name__ == "__main__":
    log_file = "lms-stage-access.log"
    log_file = os.path.abspath(log_file)

    if not os.path.exists(log_file):
        print(f"Помилка: Файл {log_file} не знайдено.")
        exit(1)

    print("Завантаження IP-адрес...")
    ip_addresses = extract_ip_addresses(log_file)
    print(f"Знайдено {len(ip_addresses)} унікальних IP-адрес у файлі.")

    # Точний підрахунок
    start_time = time.time()
    exact_count = exact_unique_count(ip_addresses)
    exact_time = time.time() - start_time

    # Наближений підрахунок
    start_time = time.time()
    approx_count = approximate_unique_count(ip_addresses)
    approx_time = time.time() - start_time

    # Порівняння результатів
    error_rate = abs(exact_count - approx_count) / exact_count * 100

    # Вивід у вигляді таблиці
    results_df = pd.DataFrame(
        {
            "Метод": ["Точний підрахунок", "HyperLogLog"],
            "Унікальні елементи": [exact_count, approx_count],
            "Час виконання (сек.)": [exact_time, approx_time],
        }
    )
    print("\nРезультати порівняння:")
    print(results_df.to_string(index=False))
    print(f"Похибка HyperLogLog: {error_rate:.2f}%")
