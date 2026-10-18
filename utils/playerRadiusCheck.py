import time


def areUnkownPlayersInRadius(m, players):
    pause = False
    m.echo("Player List:")
    for player in m.players():
        m.echo(" - " + player.name)
        if (
            player.name != "AllInMyFantasy"
            and player.name != "Jodu555"
            and player.name != "RedstoneAPI"
            and player.name != "TRyFlow"
            and player.name != "Editfusee"
        ):
            pause = True
            time.sleep(1)
            m.execute("/ph Jodu555")
            break
    return pause
