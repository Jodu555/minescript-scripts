import time
import minescript as m

# ---------------- Config ----------------

FOOD_SLOT = 0  # Slot 8 (0-indexed)

BACK_TIME = 0.2
FORWARD_TIME = 0.2

LOOP_DELAY = 30

# ---------------- Helpers ----------------


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


# ---------------- Main Loop ----------------


def main():
    m.echo("ANTI-AFK: Starting loop.")

    p = m.player()

    m.echo(str(p.nbt))

    while True:
        m.echo("ANTI-AFK: Restarting")

        time.sleep(1)
        # Move
        walk_back(BACK_TIME)
        time.sleep(1)
        walk_forward(FORWARD_TIME)

        # Eat if needed
        m.echo("ANTI-AFK: Eating...")
        m.player_inventory_select_slot(FOOD_SLOT)
        hold_use(2.5)
        
        # Wait
        time.sleep(LOOP_DELAY)


if __name__ == "__main__":
    main()
