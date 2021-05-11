import numpy as np
from cardmap import card_map
import emoji
from Player_Class import Player

class NPC(Player):
    def __init__(self, Hand=np.array([])):
       Player.__init__(self, Hand)
    #    suit_pairs = np.array([])
    #    value_pairs = np.array([])
       discards = np.array([])

    def print_discards(self):
        print(len(self.discards), self.discards)

    def npc_discard(self):
        if len(self.unmatched_cards) > 0:
            if len(self.discards) > 0:
                # todo: discard highest pip card
                discard = self.discards[0]
                self.discards = self.discards[self.discards != discard]
                self.Hand = self.Hand[self.Hand != discard]
                return discard
            else:
                # todo: discard highest pip card
                discard = self.unmatched_cards[0]
                self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != discard]
                self.Hand = self.Hand[self.Hand != discard]
                return discard
        else:
            return("NPC has gin!")

    def suit_run_check(self):
        self.discards = self.Hand.copy()
        self.unmatched_cards = self.Hand.copy()
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

        for card in self.Hand:
            run = 1
            try:
                card_value = card_values[str(card['Value'])]
                # print("!!!!!!card value", card_value)
                above = int(card_value) + 1
                while above < 14:
                    above_label = valueCards[above]
                    if above and self.cards[f"{above_label}{switcher[card['Suit']]}"] == True:
                        print("NPC MATCH ABOVE MF!!!!!!")
                        # remove card - how remove all mathces?
                        self.discards = self.discards[self.discards != card]
                        run += 1
                        if run > 2:
                            # print("RUN > 2, all of these need to be moved to matched")
                            self.discards = self.discards[self.discards != card]
                            self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != card]
                    else:
                        break

                    above += 1
            except Exception as e:
                print("Error matching above card, ", e)

            try:
                below = int(card_value) - 1
                while below > 0:
                    below_label = valueCards[below]
                    if above and self.cards[f"{below_label}{switcher[card['Suit']]}"] == True:
                        print("NPC MATCH BELOW MF!!!!!!")
                        # remove card - how remove all mathces?
                        self.discards = self.discards[self.discards != card]
                        run += 1
                        if run > 2:
                            # print("RUN > 2, all of these need to be moved to matched")
                            self.discards = self.discards[self.discards != card]
                            self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != card]
                    else:
                        break
                    below -= 1
                # print("discards!", len(self.discards), self.discards)
            except Exception as e:
                print("Error matching below card, ", e)
        # print("HERE! end of suit loop:", "unmatched:", len(self.unmatched_cards), self.unmatched_cards, "\ndiscards:",len(self.discards), self.discards)

    def value_run_check(self):
        switcher={
            ":heart_suit:":"H",
            ":spade_suit:":"S",
            ":club_suit:":"C",
            ":diamond_suit:":"D"
        }

        for card in self.unmatched_cards:
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
                print("NPC has value run")
                # remove from dicard list
                # add to matched list
                self.discards = self.discards[self.discards != card]
                self.unmatched_cards = self.unmatched_cards[self.unmatched_cards != card]

            elif count > 1:
                print("NPC has value pair")
                self.discards = self.discards[self.discards != card]
                # remove from dicard list
            
        # print("HERE! end of value loop :", "unmatched:", len(self.unmatched_cards), self.unmatched_cards, "\ndiscards:",len(self.discards), self.discards)