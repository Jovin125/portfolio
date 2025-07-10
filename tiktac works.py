import tkinter as tk
import random

place = tk.Tk()
place.title('tic-tac-toe')
place.geometry('400x400')

boxcolours = []
playerbox = []
randobox = []
stuff = (randobox, playerbox)

def restart():
    boxcolours.clear()
    playerbox.clear()
    randobox.clear()
    delete()

    print('restart')
    main()

def update():
    global hold
    if hold and hold.winfo_exists():
        for items in hold.winfo_children():
            items.destroy()


def delete():
    for items in place.winfo_children():
        items.destroy()


def result(r, num):
    delete()

    after = tk.Frame()
    after.pack(expand=True, fill='both')
    for places in range(5):
        after.columnconfigure(index=places, weight=1)
        after.rowconfigure(index=places, weight=1)

    names = ['random', 'players']
    print(f'the result is {names[num]}: {r}')
    title = tk.Label(after, text='Result', font=('Arial', 30))
    title.grid(columnspan=5, row=0, column=2)
    result = tk.Label(after, text=f'the result is {names[num]}: {r}', font=('Arial', 25))
    result.grid(columnspan=5, row=1, column=2)
    again = tk.Button(after, text='restart', command=lambda: restart())
    again.grid(columnspan=3, row=2, column=1)
    exit = tk.Button(after, text='Exit', command=place.quit)
    exit.grid(columnspan=2, row=2, column=4)


def ranturn():
    while True:
        rando = random.choice(choosablebox)
        if rando != '1':
            print(rando)
            turn = '2nd'
            idk = [int(rando[0]), int(rando[2])]
            break
    check(turn, idk)


def win(nameboxes):
    for things in range(2):
        if nameboxes[0] in stuff[things] and nameboxes[1] in stuff[things] and nameboxes[2] in stuff[things]:
            break
        elif nameboxes[3] in stuff[things] and nameboxes[4] in stuff[things] and nameboxes[5] in stuff[things]:
            break
        elif nameboxes[6] in stuff[things] and nameboxes[7] in stuff[things] and nameboxes[8] in stuff[things]:
            break

        elif nameboxes[0] in stuff[things] and nameboxes[3] in stuff[things] and nameboxes[6] in stuff[things]:
            break
        elif nameboxes[1] in stuff[things] and nameboxes[4] in stuff[things] and nameboxes[7] in stuff[things]:
            break
        elif nameboxes[2] in stuff[things] and nameboxes[5] in stuff[things] and nameboxes[8] in stuff[things]:
            break


        elif nameboxes[0] in stuff[things] and nameboxes[4] in stuff[things] and nameboxes[8] in stuff[things]:
            break
        elif nameboxes[2] in stuff[things] and nameboxes[4] in stuff[things] and nameboxes[6] in stuff[things]:
            break
        else:
            things = 3
    return things

def check(turn, idk):
    nameboxes = ["0x0_box", "0x1_box", "0x2_box",
                 "1x0_box", "1x1_box", "1x2_box",
                 "2x0_box", "2x1_box", "2x2_box"]
    for things in range(len(nameboxes)):
        if int(nameboxes[things][0]) == idk[0] and int(nameboxes[things][2]) == idk[1]:
            used = nameboxes[things]
            choosablebox[things] = '1'
            if turn == 'players':
                replace = ['x', 'red', 'disabled']
                playerbox.append(used)
                turn = '2nd'
            else:
                replace = ['o', 'green', 'disabled']
                randobox.append(used)
                turn = 'players'
            boxcolours[things] = replace
            break

    if win(nameboxes) == 0:
        result('win', 0)
    elif win(nameboxes) == 1:
        result('win', 1)

    elif int(len(randobox)) != int(len(playerbox)):
        if int(len(playerbox)) < 5:
            ranturn()
        else:
            result('draw', 1)
    else:
        pressing(turn, nameboxes)


def pressing(turn, boxes):
    update()
    turn = 'players'
    for p in range(len(boxes)):
        x = int(boxes[p][0])
        y = int(boxes[p][2])
        idk = [x, y]
        s = boxcolours

        boxes[p] = tk.Button(hold, text=s[p][0], bg=s[p][1],
                             command=lambda idk=idk: check(turn, idk))
        boxes[p].grid(row=x, column=y)
        boxes[p].configure(state=s[p][2])


def main():
    global hold, boxes, choosablebox

    boxes = ["0x0_box", "0x1_box", "0x2_box",
             "1x0_box", "1x1_box", "1x2_box",
             "2x0_box", "2x1_box", "2x2_box"]
    choosablebox = ["0x0_box", "0x1_box", "0x2_box",
                    "1x0_box", "1x1_box", "1x2_box",
                    "2x0_box", "2x1_box", "2x2_box"]

    hold = tk.Frame()
    hold.pack(expand=True, fill='both')
    for places in range(5):
        hold.columnconfigure(index=places, weight=1)
        hold.rowconfigure(index=places, weight=1)
    turn = 'players'

    for stuff in boxes:
        normalstate = ['     ', 'light blue', 'normal']
        boxcolours.append(normalstate)

    pressing(turn, boxes)


main()
place.mainloop()