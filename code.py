#!/usr/bin/env python3.9

class Game:
    def __init__(self, players):
        self.players = players

    def mustHave(self, player_idx, item_idx, typename):
        target = self.players[player_idx]
        for i in range(len(self.players)):
            if i != player_idx:
                self.mustNotHave(i, item_idx, typename)
            else:
                if item_idx in target.canHave[typename]:
                    target.canHave[typename].remove(item_idx)
                    target.mustHave[typename].append(item_idx)
                    target.possibleCards -= 1
                    if (target.possibleCards == 1):
                        if len(target.canHave['names']) == 1:
                            self.mustHave(player_idx, target.canHave['names'][0], 'names')
                        elif len(target.canHave['items']) == 1:
                            self.mustHave(player_idx, target.canHave['items'][0], 'names')
                        else:
                            self.mustHave(player_idx, target.canHave['places'][0], 'places')

    def mustNotHave(self, player_idx, item_idx, typename):
        target = self.players[player_idx]
        target.canHave[typename].remove(item_idx)
        target.possibleCards -= 1

        if (target.possibleCards == 1):
            if len(target.canHave['names']) == 1:
                self.mustHave(player_idx, target.canHave['names'][0], 'names')
            elif len(target.canHave['items']) == 1:
                self.mustHave(player_idx, target.canHave['items'][0], 'names')
            else:
                self.mustHave(player_idx, target.canHave['places'][0], 'places')

    def display(self):
        for player in self.players:
            print('--\u001b[43m' + player.name.upper() + '\u001b[0m--')
            print("THIS PLAYER MUST HAVE")
            print("\u001b[1mNames:\u001b[0m")
            for n in player.mustHave['names']:
                print(player.possiblities['names'][n], end=", ")
            print()
            print("\u001b[1mItems:\u001b[0m")
            for n in player.mustHave['items']:
                print(player.possiblities['items'][n], end=", ")
            print()
            print("\u001b[1mPlaces:\u001b[0m")
            for n in player.mustHave['places']:
                print(player.possiblities['places'][n], end=", ")
            print()
            print("THIS PLAYER COULD HAVE")
            print("\u001b[1mNames:\u001b[0m")
            for n in player.canHave['names']:
                print(player.possiblities['names'][n], end=", ")
            print()
            print("\u001b[1mItems:\u001b[0m")
            for n in player.canHave['items']:
                print(player.possiblities['items'][n], end=", ")
            print()
            print("\u001b[1mPlaces:\u001b[0m")
            for n in player.canHave['places']:
                print(player.possiblities['places'][n], end=", ")
            print()

class Player:
    def __init__(self, name, maxCards):
        self.name = name
        self.possiblities = {}
        self.mustHave = {}
        self.canHave = {}
        self.maxCards = maxCards
        self.cardCount = 0
        self.possibleCards = -1

    def setPossiblities(self, names, items, places):
        self.possiblities['names'] = names
        self.possiblities['items'] = items
        self.possiblities['places'] = places
        self.canHave['names'] = list(range(len(names)))
        self.canHave['items'] = list(range(len(items)))
        self.canHave['places'] = list(range(len(places)))
        self.mustHave['names'] = []
        self.mustHave['items'] = []
        self.mustHave['places'] = []


        self.totalCards = len(names) + len(items) + len(places)
        self.possibleCards = len(names) + len(items) + len(places)

def readThing(s):
    l = []
    with open(s) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            l.append(line)

    return l


def getPlayers(names, items, places):
    player_count = int(input("how many players?: "))
    player_list = []
    for i in range(player_count):
        player = input(f"player {i} name: ")
        p = Player(player, 6)
        player_list.append(p)

        p.setPossiblities(names, items, places)
    return player_list

def whoAmI(players):
    for i in range(len(players)):
        print(f"({i}) {players[i].name}")
    me = int(input("Who are you?"))
    return me

def Menu():
    print("(0) Someone asks")
    print("(1) Someone enters room")
    print("(2) Someone teleports to room")
    choice = input("Choice: ")
    return int(choice)

def someone_asks(players, me):
    for i in range(len(players)):
        print(f"({i}) {players[i]}")
    asker = int(input("Who asks?"))
    print()


def ChoiceHandler(choice, players):
    if (choice == 0):
        pass
    elif (choice == 1):
        pass
    elif (choice == 2):
        pass
    elif (choice == 3):
        pass
    elif (choice == 4):
        pass

def get_choice_from_list(l):
    for i in range(len(l)):
        print(f"({i}) {l[i]}")

    return int(input("choice: "))


def get_named_choice(l, names):
    for i in range(len(l)):
        print(f"({l[i]}) {names[l[i]]}")

    return int(input("choice: "))




def repl(players, me, names, items, places, g):
    while True:
        for current_turn in range(len(players)):
            print("It's " + (players[current_turn].name + "\'s" if current_turn != me else 'your') + "turn:")
            if (current_turn == me):
                g.display()
            yn = input("Are they going to ask a question? (y/n)")
            if (yn == 'y'):
                name = get_choice_from_list(names)
                item = get_choice_from_list(items)
                place = get_choice_from_list(places)
                for i in range(current_turn + 1, len(players) + current_turn):
                    responder = i % len(players)
                    print(responder)
                    resp = input("Did " + (players[responder].name if current_turn != me else 'you') + " pass any cards? (y/n)")
                    if (resp == 'y'):
                        break
                    else:
                        g.mustNotHave(i, name, 'names')
                        g.mustNotHave(i, item, 'items')
                        g.mustNotHave(i, place, 'places')




def whatIHave(players, me, g):
    while True:
        print("Please enter what cards you have:")
        print("(0) Name card")
        print("(1) Item card")
        print("(2) Place card")
        print("(3) Stop")
        choice = int(input())
        if choice == 0:
            name = get_named_choice(players[me].canHave['names'], players[me].possiblities['names'])
            g.mustHave(me, name, 'names')
        elif choice == 1:
            item = get_named_choice(players[me].canHave['items'], players[me].possiblities['items'])
            g.mustHave(me, item, 'items')
        elif choice == 2:
            place = get_named_choice(players[me].canHave['places'], players[me].possiblities['places'])
            g.mustHave(me, place, 'places')
        else:
            break



def main():
    names = readThing('names')
    places = readThing('places')
    items = readThing('items')
    players = getPlayers(names, items, places)
    g = Game(players)
    me = whoAmI(players)

    whatIHave(players, me, g)
    repl(players, me, names, items, places, g)

main()
