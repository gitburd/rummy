from cardmap import card_map
import emoji
from Player_Class import Player
import settings

switcher = {
    ":heart_suit:": "H",
    ":spade_suit:": "S",
    ":club_suit:": "C",
    ":diamond_suit:": "D"
}


class NPC(Player):
    def __init__(self, hand):
        Player.__init__(self, hand, "computer")
        self.discards = []

    def print_discards(self):
        print(len(self.discards), self.discards)

    def npc_discard(self):
        if len(self.unmatched_cards) > 0:
            if len(self.discards) > 0:
                # todo: discard highest pip card
                discard = self.discards.pop()
                # self.discards = self.discards[self.discards != discard]
                if card in self.unmatched_cards:
                    self.unmatched_cards.remove(discard)
                # if card in self.unmatched_cards:
                self.hand.remove(card)
                self.set_card(discard, False)
                return discard
            else:
                # todo: discard highest pip card
                discard = self.unmatched_cards.pop()
                if card in self.unmatched_cards:
                    self.unmatched_cards.remove(discard)
                self.hand.remove(discard)
                self.set_card(discard, False)
                return discard
        else:
            return("NPC has gin!")

    def suit_run_check(self):

        self.discards = self.hand.copy()
        self.unmatched_cards = self.hand.copy()

        for card in self.hand:
            run = self.card_suit_check(card)
            try:
                if run > 2:
                    if card in self.discards:
                        self.discards.remove(card)
                    if card in self.unmatched_cards:
                        self.unmatched_cards.remove(card)
                elif run > 1:
                    if card in self.discards:
                        self.discards.remove(card)
            except Exception as e:
                pass

    def card_suit_check(self, card):
        global switcher
        valueCards = {13: "K", 12: "Q", 11: "J", 10: "10", 9: "9", 8: "8", 7: "7", 6: "6",
                      5: "5", 4: "4", 3: "3", 2: "2", 1: "A"}
        run = 1
        try:
            above = int(card['order']) + 1
            while above < 14:
                above_label = valueCards[above]
                if above and self.cards[f"{above_label}{switcher[card['suit']]}"] == True:
                    # remove card - how remove all mathces?
                    # self.discards = self.discards[self.discards != card]
                    if card in self.discards:
                        self.discards.remove(card)
                    run += 1
                    if run > 2:
                        if card in self.unmatched_cards:
                            self.unmatched_cards.remove(card)
                        self.suit_melds.append(card)
                        return run
                else:
                    break
                    above += 1
        except Exception as e:
            print("Error matching above card, ", e)

        try:
            below = int(card['order']) - 1
            while below > 0:
                below_label = valueCards[below]
                if above and self.cards[f"{below_label}{switcher[card['suit']]}"] == True:
                    # remove card - how remove all mathces?
                    if card in self.discards:
                        self.discards.remove(card)
                    run += 1
                    if run > 2:
                        if card in self.unmatched_cards:
                            self.unmatched_cards.remove(card)
                        self.suit_melds.append(card)
                        return run
                else:
                    break
                below -= 1
            return run
            # print("discards!", len(self.discards), self.discards)
        except Exception as e:
            print("Error matching below card, ", e)

    def value_run_check(self):
        if len(self.unmatched_cards) == 0:
            print("GIN")
            return False
        else:
            print("not gin", len(self.unmatched_cards))
            for card in self.unmatched_cards:
                count = self.card_value_check(card)
                if count > 2:
                    # remove from dicard list
                    # add to matched list
                    self.unmatched_cards.remove(card)
                elif count > 1:
                    if card in self.discards:
                        self.discards.remove(card)
                    # remove from dicard list

    def card_value_check(self, card):
        # print("/////////", card)
        global switcher
        count = 0
        if self.cards[f"{card['value']}H"] == True:
            count += 1
        if self.cards[f"{card['value']}S"] == True:
            count += 1
        if self.cards[f"{card['value']}C"] == True:
            count += 1
        if self.cards[f"{card['value']}D"] == True:
            count += 1

        return count

    def choose_card(self, discard):
        count = self.card_value_check(discard)
        if count > 0:
            return "discard"

        run = self.card_suit_check(discard)
        if run > 1:
            return "discard"
        else:
            return "deck"

    def npc_turn(self, discard):
        draw = self.choose_card(discard)
        if draw == "discard":
            print("npc took discard")
            self.draw(discard)
        else:
            print("npc took rom deck")
            card = settings.deck[0]
            settings.deck = settings.deck[1:]
            self.draw(card)

        self.suit_run_check()
        con = self.value_run_check()

        if not con:
            print("npc gin")
            self.knock()
        else:
            print("npc discard")
            discard = self.npc_discard()
            print(f"NPC Discard: {discard}")
            # self.get_unmatched_pips()
            self.score_check()
