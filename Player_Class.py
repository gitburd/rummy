
import numpy as np
from cardmap import card_map
import emoji

class Player:
    def __init__(self, Hand=np.array([])):
        self.Hand = Hand
        self.Score = self.set_score()
        self.cards = self.set_cards()
        self.meld_cards = np.array([])
        self.unmatched_cards = self.Hand.copy()
        self.runs=np.array([])

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
    
    def play(self, new_hand):
        self.Hand = new_hand
        self.score = self.set_score()

    def print_cards(self):
        print(self.cards)
    
    def count_meld_check(self):
        switcher={
            ":heart_suit:":"H",":spade_suit:":"S",":club_suit:":"C",":diamond_suit:":"D"
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


    def run_meld_check(self):
        switcher={
            ":heart_suit:":"H",":spade_suit:":"S",":club_suit:":"C",":diamond_suit:":"D"
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
                print("GOT THIS 2, ", e)