import emoji
from cardmap import card_map
from Player_Class import Player
from NPC_Class import NPC
import settings

settings.init()


def get_hand():
    hand = []
    for i in range(10):
        card = settings.deck.pop()
        hand.append(card)
    return hand


def draw_card():
    card = settings.deck.pop()
    return card


def print_card(card):
    try:
        return (emoji.emojize(f"{card['value']}{card['suit']}"))
    except Exception as e:
        print(emoji.emojize(f"{card['value']}{card['suit']}"))


def player_discard_card(player, idx):
    settings.discard = player.hand[idx]
    player.discard(player.hand[idx])


print("inital discard:", end=" ")
print(print_card(settings.discard))
human_hand = [{'value': 10, 'order': 10, 'pips': 10, 'suit': ':spade_suit:'},
              {'value': 'J', 'order': 11, 'pips': 10, 'suit': ':spade_suit:'},
              {'value': 'Q', 'order': 12, 'pips': 10, 'suit': ':spade_suit:'},
              {'value': 5, 'order': 5, 'pips': 5, 'suit': ':spade_suit:'},
              {'value': 4, 'order': 4, 'pips': 4, 'suit': ':club_suit:'},
              {'value': 9, 'order': 9, 'pips': 9, 'suit': ':spade_suit:'},
              {'value': 5, 'order': 5, 'pips': 5, 'suit': ':club_suit:'},
              {'value': 3, 'order': 3, 'pips': 3, 'suit': ':heart_suit:'},
              {'value': 'K', 'order': 13, 'pips': 10, 'suit': ':spade_suit:'},
              {'value': 5, 'order': 5, 'pips': 5, 'suit': ':diamond_suit:'}]

npc_hand = [{'value': 'J', 'order': 11, 'pips': 10, 'suit': ':diamond_suit:'},
            {'value': 5, 'order': 5, 'pips': 5, 'suit': ':heart_suit:'},
            {'value': 'Q', 'order': 12, 'pips': 10, 'suit': ':club_suit:'},
            {'value': 'Q', 'order': 12, 'pips': 10, 'suit': ':heart_suit:'},
            {'value': 'A', 'order': 1, 'pips': 1, 'suit': ':spade_suit:'},
            {'value': 2, 'order': 2, 'pips': 2, 'suit': ':spade_suit:'},
            {'value': 3, 'order': 3, 'pips': 3, 'suit': ':club_suit:'},
            {'value': 10, 'order': 10, 'pips': 10, 'suit': ':diamond_suit:'},
            {'value': 'Q', 'order': 12, 'pips': 10, 'suit': ':diamond_suit:'},
            {'value': 9, 'order': 9, 'pips': 9, 'suit': ':diamond_suit:'}]

# Human_Player = Player(get_hand())
Human_Player = Player(human_hand)
# Human_Player.score_check()
ComputerPlayer = NPC(npc_hand)
knock = False


while not knock:
    print("---- First while ----")
    if len(settings.deck) < 3:
        print("Shuffling...")
        settings.init()

    print(Human_Player)
    print(ComputerPlayer)

    while True:
        print("---- Second while ----")
        print(f"Discard:", end=" ")
        print(print_card(settings.discard))

        action = input("\nDraw from discard or deck?(a/s): ")

        try:
            if action.lower() == "a":
                Human_Player.draw(settings.discard)
                print("\nYou: ", Human_Player)
                break
            elif action.lower() == "s":
                draw_card()
                Human_Player.draw(draw_card())
                print("\nYou: ", Human_Player)
                break
            else:
                print('Enter "h" to draw or "s" to STAY.')
        except Exception as e:
            print('Exception', e)

    while True:
        print("---- Third while ----")
        Human_Player.print_discard_options()
        action = input(
            "\nWhich do you want to discard?(1/2/3/4/5/6/7/8/9/10/11): ")

        try:
            if int(action) in range(1, 12):
                player_discard_card(Human_Player, int(action)-1)
                print("\nYou: ", Human_Player)
                print(f"Discard:", end=" ")
                print(print_card(settings.discard))
                break
            else:
                print('Enter a number 1-10 to discard')
        except Exception as e:
            print('There was an issue', e)

    pips = Human_Player.score_check()
    print("Socre check then got pips on main...", pips)
    if pips < 60:
        while True:
            print("---- fourth while ----")
            action = input("\nDo you want to knock?(y/n): ")
            try:
                if action.lower() == "y":
                    knock = Human_Player.knock()
                    break
                elif action.lower() == "n":
                    break
                else:
                    print('Enter "y" to KNOCK or "n" not to.')
            except Exception as e:
                print('Exception', e)
    if knock == True:
        break

    print(f"Human Discard:", end=" ")
    print(print_card(settings.discard))

    Human_Player.score_check()

    print("---- NPC turn ----")
    print("\nNPC: ", ComputerPlayer)
    ComputerPlayer.npc_turn(settings.discard)
    print("\nNPC: ", ComputerPlayer)
    knock = ComputerPlayer.knock()

print('KNOCK!', knock)
if Human_Player.has_knocked:
    print('THE HUMAN KNOCKED')
    Human_Player.score_hand(ComputerPlayer)
else:
    ComputerPlayer.score_hand(Human_Player)
    print("THE NPC KNOCKED")

print("New Scores: ", Human_Player.score, ComputerPlayer.score)
