
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
    
    
    def play(self, new_hand):
        self.Hand = new_hand
        self.score = self.set_score()

    def print_cards(self):
        print(self.cards)
    
    def value_meld_check(self, cards):
        switcher={
            ":heart_suit:":"H",":spade_suit:":"S",":club_suit:":"C",":diamond_suit:":"D"
        }

        self.meld_cards = np.array([])

        for card in cards:
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
                cards = cards[cards != card]
        return cards
        

    def suit_meld_check(self, cards):
        switcher={
            ":heart_suit:":"H",":spade_suit:":"S",":club_suit:":"C",":diamond_suit:":"D"
        }

        card_values = {
            "A" : 1, "K" : 13, "Q" : 12, "J" : 11,
            "10":10, "9":9, "8":8, "7":7, "6":6,
            "5":5, "4":4, "3":3, "2":2
        }
        
        valueCards = { 13:"K", 12:"Q", 11:"J", 10:"10", 9:"9", 8:"8", 7:"7", 6:"6",
            5:"5", 4:"4", 3:"3", 2:"2", 1:"A"}

        for card in cards:
            run = 1
            try:
                card_value = card_values[str(card['Value'])]
                above = int(card_value) + 1
                while above < 14:
                    above_label = valueCards[above]
                    if above_label and self.cards[f"{above_label}{switcher[card['Suit']]}"] == True:
                        run += 1
                        if run > 2:
                           cards = cards[cards != card]
                    else:
                        break

                    above += 1
            except Exception as e:
                print("Error matching above card, ", e)

            try:
                below = int(card_value) - 1
                while below > 0:
                    below_label = valueCards[below]
                    if below_label and self.cards[f"{below_label}{switcher[card['Suit']]}"] == True:
                        run += 1
                        if run > 2:
                            cards = cards[cards != card]
                    else:
                        break
                    below -= 1
            except Exception as e:
                print("Error matching below card, ", e)
        return cards
    
    def get_unmatched_pips(self,cards):
        card_values = {            
            "A" : 1, "K" : 10, "Q" : 10, "J" : 10,
            "10":10, "9":9, "8":8, "7":7, "6":6,
            "5":5, "4":4, "3":3, "2":2
        }
        pips = 0
        
        for card in cards:
            pips += card_values[str(card['Value'])]
            print(card['Value'])
        
        print("unmatched pips: ", pips)
        return pips
    
    def knock(self, opponent):
        print('knock')
    
    def score_check(self,cards):
        print("SCORE CHECK")
        unmatched_cards = self.suit_meld_check(cards)
        # print("unmatched after suit check", unmatched_cards)
        unmatched_cards = self.value_meld_check(unmatched_cards)
        # print("unmatched after value check", unmatched_cards)
        suit_first_score = self.get_unmatched_pips(unmatched_cards)
        # print("!!!! suit first PIPS:", pips)

        unmatched_cards = self.value_meld_check(cards)
        # print("unmatched after value check", unmatched_cards)
        unmatched_cards = self.suit_meld_check(unmatched_cards)
        # print("unmatched after suit check", unmatched_cards)
        value_first_score = self.get_unmatched_pips(unmatched_cards)
        
        print("!!!! PIPS:", suit_first_score, "OR",value_first_score)
        return min(suit_first_score,value_first_score)



