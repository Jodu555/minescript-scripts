import minescript as m
import time
import math

# ─── Configuration ────────────────────────────────────────────────
FISHING_ROD_SLOT = 0  # Hotbar slot (0-8) where your fishing rod sits
FOOD_SLOT = 1  # Hotbar slot where your food sits
CAST_DELAY = 3.0  # Seconds after casting before we start checking for a bite
MAX_WAIT_FOR_BITE = 30.0  # Safety timeout: if no bite in this many seconds, recast
ANTI_AFK_DURATION = 0.1  # How long to walk forward/backward each time
EAT_DURATION = 0.5  # How long to hold right‑click while eating
# ──────────────────────────────────────────────────────────────────


def select_slot(slot: int):
    """Switch to the given hotbar slot (0-8)."""
    m.player_inventory_select_slot(slot)
    time.sleep(0.1)  # small delay to let the slot change register


def press_use(hold_time: float = 0.0):
    """Press the use (right-click) key. If hold_time > 0, hold it for that long."""
    m.player_press_use(True)
    if hold_time > 0:
        time.sleep(hold_time)
    m.player_press_use(False)


def find_bobber():
    """Return the bobber entity that belongs to us, or None."""
    for entity in m.entities():
        if "bobber" in entity.type:
            return entity
    return None


def wait_for_bite(timeout: float = MAX_WAIT_FOR_BITE) -> bool:
    """
    Wait until the bobber shows the characteristic 'bite' motion.
    Returns True if a bite was detected, False on timeout.
    """
    start = time.time()
    bobber = None

    # First, wait for the bobber to appear after casting.
    while time.time() - start < 2.0:
        bobber = find_bobber()
        if bobber is not None:
            break
        time.sleep(0.05)

    if bobber is None:
        return False  # never saw a bobber – cast failed?

    # Now poll the bobber's velocity. When a fish bites, the bobber
    # briefly moves vertically (or its motion changes sharply).
    while time.time() - start < timeout:
        # Re‑fetch the entity each loop; the original object may go stale.
        current = None
        for e in m.entities():
            if e.uuid == bobber.uuid:
                current = e
                break
        if current is None:
            return False  # bobber disappeared (reeled in or broken)

        # The bite is usually marked by a sudden change in vertical velocity.
        # We check for a non‑negligible Y velocity while X/Z are nearly zero.
        vx, vy, vz = current.velocity
        if abs(vy) > 0.19:
            return True

        time.sleep(0.01)  # 0.05 == poll 20× per second

    return False  # timed out


def reel_in():
    """Right-click to reel the fish in."""
    press_use(0.0)
    time.sleep(0.3)  # give the server a moment to process


def anti_afk():
    """Walk forward and backward briefly to simulate player activity."""
    m.player_press_forward(True)
    time.sleep(ANTI_AFK_DURATION)
    m.player_press_forward(False)

    m.player_press_backward(True)
    time.sleep(ANTI_AFK_DURATION)
    m.player_press_backward(False)


def eat_food():
    """Switch to the food slot, hold right‑click to eat, then switch back."""
    select_slot(FOOD_SLOT)
    press_use(EAT_DURATION)  # hold right‑click for EAT_DURATION seconds
    time.sleep(0.2)  # let the eating animation finish
    select_slot(FISHING_ROD_SLOT)


def fish_once():
    """Complete one fishing cycle: cast → wait → reel → anti‑AFK → eat."""
    # 1. Make sure we hold the fishing rod.
    select_slot(FISHING_ROD_SLOT)

    # 2. Cast the rod.
    press_use(0.0)
    time.sleep(CAST_DELAY)

    # 3. Wait for a bite.
    if not wait_for_bite():
        # No bite – reel in to reset and try again next loop.
        reel_in()
        return

    # 4. Reel the fish in.
    reel_in()

    # 5. Anti‑AFK movement.
    anti_afk()

    # 6. Eat some food.
    eat_food()


def main():
    """Main loop - runs until you stop the script."""
    m.echo("§aAuto-Fishing started. Press Ctrl+C or stop the script to end.")
    try:
        pause = False
        while not pause:
            m.echo("Player List:")
            for player in m.players():
                m.echo(" - " + player.name)
                if (
                    player.name != "AllInMyFantasy"
                    and player.name != "Jodu555"
                    and player.name != "RedstoneAPI"
                ):
                    pause = True
                    time.sleep(1)
                    m.execute("/ph Jodu555")
                    break
            fish_once()
    except KeyboardInterrupt:
        m.echo("§cAuto - Fishing stopped.")


if __name__ == "__main__":
    main()
