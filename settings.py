from random import shuffle


def init():
    global deck
    global discard
    deck = create_deck()
    discard = deck.pop()


def create_deck():
    deck = []
    for card in range(2, 11):  # add 2-10
        heart = {"value": card, "order": card,
                 "pips": card, "suit": ":heart_suit:"}
        spade = {"value": card, "order": card,
                 "pips": card, "suit": ":spade_suit:"}
        club = {"value": card, "order": card,
                "pips": card, "suit": ":club_suit:"}
        dimond = {"value": card, "order": card,
                  "pips": card, "suit": ":diamond_suit:"}
        deck.extend((heart, spade, club, dimond))

    facevalues = [{"value": "J", "order": 11, "pips": 10}, {"value": "Q", "order": 12, "pips": 10}, {
        "value": "K", "order": 13, "pips": 10}, {"value": "A", "order": 1, "pips": 1}]
    for card in facevalues:  # add face values
        heart = {"value": card['value'], "order": card['order'],
                 "pips": card['pips'], "suit": ":heart_suit:"}
        spade = {"value": card['value'], "order": card['order'],
                 "pips": card['pips'], "suit": ":spade_suit:"}
        club = {"value": card['value'], "order": card['order'],
                "pips": card['pips'], "suit": ":club_suit:"}
        dimond = {"value": card['value'], "order": card['order'],
                  "pips": card['pips'], "suit": ":diamond_suit:"}
        deck.extend((heart, spade, club, dimond))
    shuffle(deck)
    return deck
