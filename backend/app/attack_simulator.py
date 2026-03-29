import random


def generate_attack() -> dict:
    """
    Generates realistic transaction data mixing normal and attack patterns.
    ~60% chance of being a suspicious transaction for demo purposes.
    """
    is_attack = random.random() < 0.6

    if is_attack:
        return {
            "user_id": random.randint(100, 200),
            "amount": random.choice([25000, 50000, 75000, 100000]),
            "device_id": f"unknown_device_{random.randint(1, 99)}",
            "location": random.choice(["Moscow", "Lagos", "Bucharest", "Unknown"]),
            "device_new": True,
            "location_change": True,
            "rapid_transactions": random.choice([True, False]),
        }
    else:
        return {
            "user_id": random.randint(1, 50),
            "amount": random.randint(200, 3000),
            "device_id": f"device_{random.randint(1, 5)}",
            "location": random.choice(["Kolkata", "Mumbai", "Delhi", "Bangalore"]),
            "device_new": False,
            "location_change": False,
            "rapid_transactions": False,
        }