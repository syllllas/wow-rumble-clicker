import datetime
import os

from imagesearch import *

IMAGES_PRIO_SORTED = [
    'resources/ok.png',  # error
    'resources/lvlup.png',  # level up
    'resources/claim-big.png',  # claim big lvlup
    'resources/claim.png',  # claim xp
    'resources/cont.png',  # continue
    'resources/try.png',  # try again
    'resources/play.png',  # play
    'resources/play2.png',  # also play
    'resources/start.png',  # start
    'resources/quest.png',  # quest
    'resources/questing.png',  # quest
    'resources/back.png'  # back
]


def main():
    stats = {}
    time_start = datetime.datetime.now()
    last = 'last'
    while True:
        if no_more_quests():
            return 666

        wait_random()
        elapsed = datetime.datetime.now() - time_start
        res = find_prio_click()
        btn = 'none'
        if 'btn' in res.keys():
            btn = res['btn']

        in_game = in_active_game()

        if in_game:
            drag()

        effi = 0.0
        played = 0
        if 'claim.png' in stats.keys() and 'start.png' in stats.keys():
            effi = stats['claim.png'] / stats['start.png'] * 100
            played = stats['start.png']

        if 'loc' in res.keys():
            if btn in stats.keys():
                if last != btn:
                    stats[btn] = stats[btn] + 1
            else:
                stats[btn] = 1
            click(res['loc'])

        claims = get_stat('claim.png', stats)
        level_ups = get_stat('lvlup.png', stats)
        errors = get_stat('ok.png', stats)
        big = get_stat('claim-big', stats)

        print(f'({str(in_game)[0]}) effi: {effi:.2f}% played: {played} elapsed: {pretty_print(elapsed)} '
              f'cl: {claims} lvl: {level_ups} big: {big} e: {errors} '
              f'btn: {btn}', end='\r')

        last = btn


def no_more_quests():
    return imagesearch('resources/quest-block.png')[0] > 0


def get_stat(key, stats):
    if key in stats.keys():
        return stats[key]
    return 0


def pretty_print(elapsed):
    return str(datetime.timedelta(seconds=elapsed.total_seconds()))


def found(location):
    return location[0] > 0 and location[1] > 0


def in_active_game():
    return imagesearch('resources/game_border.png')[0] > 0


def find_gold():
    # prio 1 gold units :)
    loc = imagesearch(f'resources/1_gold.png')
    if found(loc):
        return loc

    cnt = 0
    while True:
        cnt = cnt + 1
        i = random.randint(2, 4)
        loc = imagesearch(f'resources/{i}_gold.png')
        if found(loc):
            return loc
        if cnt > 100:
            return [10, 10]


def find_prio_click():
    for img in IMAGES_PRIO_SORTED:
        location = imagesearch(img)
        if found(location):
            image = os.path.basename(img)
            return {'loc': location, 'btn': image}
    return {}


def drag():
    gold_loc = find_gold()
    if gold_loc[0] == 10 and gold_loc[1] == 10:
        return
    drag_offset_x = random.randint(-100, 0)
    drag_offset_y = random.randint(-200, 100)
    pyautogui.moveTo(gold_loc[0], gold_loc[1] - 20)
    drag_time = random.randint(50, 100) / 100
    pyautogui.dragRel(drag_offset_x, drag_offset_y - 500, drag_time)


def wait_random():
    sec = random.randint(50, 300) / 100
    time.sleep(sec)


def click(location):
    pyautogui.leftClick(location[0] + 40, location[1] + 40)


if __name__ == "__main__":
    main()
