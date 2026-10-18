import time
import minescript as m
import playerRadiusCheck as prc

# ---------------- Config ----------------

SWORD_SLOT = 0  # Slot 1 (0-indexed)
FOOD_SLOT = 7  # Slot 8 (0-indexed)

ATTACKS = 4
ATTACK_INTERVAL = 1.0

BACK_TIME = 0.5
FORWARD_TIME = 0.5

LOOP_DELAY = 30

# ---------------- Helpers ----------------


def attack():
    m.player_press_attack(True)
    time.sleep(0.1)
    m.player_press_attack(False)


def hold_use(seconds):
    m.player_press_use(True)
    time.sleep(seconds)
    m.player_press_use(False)


def walk_back(seconds):
    m.press_key_bind("key.back", True)
    time.sleep(seconds)
    m.press_key_bind("key.back", False)


def walk_forward(seconds):
    m.press_key_bind("key.forward", True)
    time.sleep(seconds)
    m.press_key_bind("key.forward", False)


def hunger():
    return m.player().food


# ---------------- Main Loop ----------------


def main():
    m.echo("Killing: Starting combat loop.")

    p = m.player()

    pause = False

    while not pause:
        m.echo("Killing: Restarting")

        pause = prc.areUnkownPlayersInRadius(m, m.players())

        # Select sword
        m.player_inventory_select_slot(SWORD_SLOT)

        # Attack 4 times
        for i in range(ATTACKS):
            attack()
            if i < ATTACKS - 1:
                time.sleep(ATTACK_INTERVAL)

        time.sleep(1)

        # Move
        walk_back(BACK_TIME)
        time.sleep(1)
        walk_forward(FORWARD_TIME)

        # Eat if needed
        m.echo("Killing: Eating...")
        m.player_inventory_select_slot(FOOD_SLOT)
        hold_use(2.5)
        m.player_inventory_select_slot(SWORD_SLOT)

        # Wait
        time.sleep(LOOP_DELAY)


if __name__ == "__main__":
    main()
