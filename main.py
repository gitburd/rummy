import numpy as np
from random import shuffle
import emoji
from cardmap import card_map

class Player:
    def __init__(self, Hand=np.array([])):
        self.Hand = Hand
        self.Score = self.set_score()
        self.cards = self.set_cards()
        self.meld_cards = np.array([])
        self.unmatched_cards = self.Hand.copy()
        self.runs=np.array([])
        self.sets=np.array([])
 
    def __str__(self):
        currentHand = ""
        for card in self.Hand:
            currentHand += f"{card['Value']}{card['Suit']} "

        return(emoji.emojize(f"{currentHand}"))

    def set_cards(self):
        user_cards = card_map.copy()
        switcher={
            ":heart_suit:":"H",
            ":spade_suit:":"S",
            ":club_suit:":"C",
            ":diamond_suit:":"D"
        }

        for card in self.Hand:
            card_key = f"{card['Value']}{switcher[card['Suit']]}"
            user_cards[card_key] = True

        self.cards = user_cards
        return user_cards

    def set_score(self):
        score = 0
        card_values = {
            "A" : 11, "K" : 10, "Q" : 10, "J" : 10, 
            "10":10, "9":9, "8":8, "7":7, "6":6, 
            "5":5, "4":4, "3":3, "2":2
        }
        for card in self.Hand:
            score += card_values[str(card['Value'])]
            # aces can be 1 or 11
        self.Score = score
        return score

    def hit(self, card):
        self.Hand = np.append(self.Hand, card)
        self.score = self.set_score()
    
    def discard_card(self, card):
        global discard
        discard = self.Hand[card]
        self.Hand = np.delete(self.Hand,card)
    
    # this should be called draw
    def play(self, new_hand):
        self.Hand = new_hand
        self.score = self.set_score()

    def print_cards(self):
        print(self.cards)
    
    def count_meld_check(self):
        switcher={
            ":heart_suit:":"H",
            ":spade_suit:":"S",
            ":club_suit:":"C",
            ":diamond_suit:":"D"
        }

        self.meld_cards = np.array([])
        self.unmatched_cards = self.Hand.copy()

        for card in self.Hand:
            count = 0
            if self.cards[f"{card['Value']}H"] == True:
                count += 1
            if self.cards[f"{card['Value']}S"] == True:
                count += 1
            if self.cards[f"{card['Value']}C"] == True:
                count += 1
            if self.cards[f"{card['Value']}D"] == True:
                count += 1

            if count > 2:
                self.meld_cards = np.append(self.meld_cards, card)
                self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != card]
        
        print("um", len(self.unmatched_cards))
        print("mc", len(self.meld_cards))

    def suit_pair_check(self):
        switcher={
            ":heart_suit:":"H",
            ":spade_suit:":"S",
            ":club_suit:":"C",
            ":diamond_suit:":"D"
        }

        card_values = {            
            "A" : 1, "K" : 13, "Q" : 12, "J" : 11,
            "10":10, "9":9, "8":8, "7":7, "6":6,
            "5":5, "4":4, "3":3, "2":2
        }
        valueCards = {11:"J", 12:"Q", 13:"K"}

        for card in self.Hand:
            try:
                card_value = card_values[str(card['Value'])]
                print("!!!!!!card value", card_value)
                above = int(card_value) + 1
                below = int(card_value) - 1

                if above > 10:
                    above = valueCards[above]
                if below > 10:
                    below = valueCards[below]
                if below == 1:
                    below = "A"
                if below == 0:
                    below == None
                if above == 14:
                    above = None
                print("?????", above, below)

                if above and self.cards[f"{above}{switcher[card['Suit']]}"] == True:
                    print("MATCH ABOVE MF!!!!!!")

                if below and self.cards[f"{below}{switcher[card['Suit']]}"] == True:
                    print("MATCH BELOW MF!!!!!!")

            except Exception as e:
                print("GOT THIS, ", e)


    def run_meld_check(self):
        switcher={
            ":heart_suit:":"H",
            ":spade_suit:":"S",
            ":club_suit:":"C",
            ":diamond_suit:":"D"
        }

        card_values = {
            "A" : 1, "K" : 13, "Q" : 12, "J" : 11,
            "10":10, "9":9, "8":8, "7":7, "6":6,
            "5":5, "4":4, "3":3, "2":2
        }
        valueCards = {11:"J", 12:"Q", 13:"K"}

        for card in self.Hand:
            try:
                card_value = card_values.get(str(card['Value']))
                # print("!!!!!!card value", cardValue)
                above = int(card_value) + 1
                below = int(card_value) - 1

                if above == 14:
                    above = None
                elif above > 10:
                    above = valueCards.get(above)

                if below == 0:
                    below == None
                elif below == 1:
                    below = "A"
                elif below > 10:
                    below = valueCards.get(below)

                # print("?????", above, below)

                if (above and self.cards[f"{above}{switcher[card['Suit']]}"] == True
                    and below and self.cards[f"{below}{switcher[card['Suit']]}"] == True):
                    print("3 CARD RUN!!!!!!")
                    self.runs = np.append(self.runs, card)
                    self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != card]

                    for user_card in self.Hand:
                        if user_card['Suit'] == card['Suit'] and user_card['Value'] == above:
                            self.runs = np.append(self.runs, user_card)
                            self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != user_card]
                        elif user_card['Suit'] == card['Suit'] and user_card['Value'] == below:
                            self.runs = np.append(self.runs, user_card)
                            self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != user_card]

                    print('len runs', len(self.runs))
                    print('unmatched,', len(self.unmatched_cards))

            except Exception as e:
                print("GOT THIS, ", e)




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
        heart={"Value":str(card), "Suit":":heart_suit:"}
        spade={"Value":str(card), "Suit":":spade_suit:"}
        club={"Value":str(card), "Suit":":club_suit:"}
        dimond={"Value":str(card), "Suit":":diamond_suit:"}
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
    return(emoji.emojize(f"{discard['Value']}{discard['Suit']}"))

deck = create_deck()
discard = draw_card()

Human_Player = Player()
House = Player()

Human_Player.Hand = get_hand()
Human_Player.set_score()
House.Hand = get_hand()
House.set_score()

while True:
    print("---- First while ----")
    if len(deck) < 3:
        print("Shuffling...")
        deck = create_deck()

    print(Human_Player)
    print(House)
    Human_Player.set_cards()
    House.set_cards()
    # print(Human_Player.print_cards())
    # print(House.print_cards())
    Human_Player.count_meld_check()
    Human_Player.run_meld_check()
    while True:
        print("---- Second while ----")
        print(f"Discard: {print_card(discard)}")

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

        action = input("\nWhich do you want to discard?(1/2/3/4/5/6/7/8/9/10): ")

        try:
            if int(action) in range(1,11):
                print(f"it was {int(action)}")
                Human_Player.discard_card(int(action)-1)
                print("\nYou: ", Human_Player)
                print(f"Discard: {print_card(discard)}")
                break
            else:
                print('Enter a number 1-10 to discard')
        except Exception as e:
            print('Enter a number 1-10 to discard')

    print("---- HOuse turn ----")
    House.hit(discard)
    House.discard_card(int(action))
    print("\nHouse: ", House)
    print(f"Discard: {print_card(discard)}")

