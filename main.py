import numpy as np
from random import shuffle
import emoji
from cardmap import card_map
from Player_Class import Player
from NPC_Class import NPC

Human_Player = Player()
NPC = NPC()

def create_deck():
    deck = np.array([])
    for card in range(2,11): # add 2-10
        heart={"Value":card, "Suit": ":heart_suit:"}
        spade={"Value":card, "Suit": ":spade_suit:"}
        club={"Value":card, "Suit": ":club_suit:"}
        dimond={"Value":card, "Suit": ":diamond_suit:"}
        deck = np.append(deck, [heart,spade,club,dimond])

    faceValues = ["J", "Q", "K", "A"]
    for card in faceValues: # add face values
        heart={"Value":card, "Suit":":heart_suit:"}
        spade={"Value":card, "Suit":":spade_suit:"}
        club={"Value":card, "Suit":":club_suit:"}
        dimond={"Value":card, "Suit":":diamond_suit:"}
        deck = np.append(deck, [heart,spade,club,dimond])
    shuffle(deck)
    return deck

def get_hand():
    global deck
    hand = np.array([])
    for i in range (10):
        card = deck[0]
        hand = np.append(hand,card)
        deck = np.delete(deck,0)
    return hand

def draw_card():
    global deck
    card = deck[0]
    deck = np.delete(deck,0)
    return card

def print_card(card):
    print(emoji.emojize(f"{card['Value']}{card['Suit']}"))

def player_discard_card(player, card):
    global discard
    # print("inside human discard", card,"++++", player.Hand[card])
    discard = player.Hand[card]
    # print("inside hd", discard)
    player.Hand = np.delete(player.Hand,card)


deck = create_deck()
discard = draw_card()
print("inital discard: ", end="")
print_card(discard)
Human_Player.Hand = get_hand()
Human_Player.set_score()
NPC.Hand = get_hand()
NPC.set_score()

# print(Human_Player)
# print(NPC)
while True:
    print("---- First while ----")
    if len(deck) < 3:
        print("Shuffling...")
        deck = create_deck()

    Human_Player.set_cards()
    NPC.set_cards()

    print(Human_Player)
    print(NPC)

    while True:
        print("---- Second while ----")
        print(f"Discard: ", end="")
        print_card(discard)

        action = input("\nDraw from discard or deck?(a/s): ")

        try:
            if action.lower() == "a":
                Human_Player.hit(discard)
                print("\nYou: ", Human_Player)
                break
            elif action.lower() == "s":
                Human_Player.hit(draw_card())
                print("\nYou: ", Human_Player)
                break
            else:
                print('Enter "h" to HIT or "s" to STAY.')
        except Exception as e:
            print('Enter "h" to HIT or "s" to STAY.')

    while True:
        print("---- Third while ----")
        Human_Player.print_discard_options()
        action = input("\nWhich do you want to discard?(1/2/3/4/5/6/7/8/9/10/11): ")

        try:
            if int(action) in range(1,12):
                print(f"it was {int(action)}")
                player_discard_card(Human_Player, int(action)-1)
                print("\nYou: ", Human_Player)
                print(f"Discard: ", end="")
                print_card(discard)
                break
            else:
                print('Enter a number 1-10 to discard')
        except Exception as e:
            print('Enter a number 1-10 to discard')

    print(f"Human Discard:", end="")
    print_card(discard)
    cards = Human_Player.Hand.copy()
    Human_Player.score_check(cards)

    print("---- NPC turn ----")
    print("\nNPC: ", NPC)
    NPC.hit(discard)
    NPC.suit_run_check()
    NPC.value_run_check()
    player_discard_card(NPC, NPC.npc_discard())
    print(f"NPC Discard: {discard}")
    # NPC.get_unmatched_pips()

    cards = NPC.Hand.copy()
    NPC.score_check(cards)

    print("\nNPC: ", NPC)


