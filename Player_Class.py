
from cardmap import card_map
import emoji


class Player:
    def __init__(self, hand, id="human"):
        self.hand = hand
        self.id = id
        self.score = 0
        self.cards = card_map.copy()
        self.unmatched_cards = hand.copy()
        self.suit_melds = []
        self.value_melds = []
        self.has_knocked = False
        self.lay_offs = []
        self.set_cards()
        self.unmatched_pips = 100

    def __str__(self):
        currenthand = ""
        for card in self.hand:
            currenthand += f"{card['value']}{card['suit']} "

        return(emoji.emojize(f"{currenthand}"))

    def print_status(self):
        currenthand = ""
        for card in self.unmatched_cards:
            currenthand += f"{card['value']}{card['suit']} "

        return(emoji.emojize(f"{currenthand}"))

    def set_cards(self):
        for card in self.hand:
            self.set_card(card)

    def set_card(self, card, in_hand=True):
        switcher = {
            ":heart_suit:": "H",
            ":spade_suit:": "S",
            ":club_suit:": "C",
            ":diamond_suit:": "D"
        }
        card_key = f"{card['value']}{switcher[card['suit']]}"
        self.cards[card_key] = in_hand

    def draw(self, card):
        self.hand.append(card)
        self.unmatched_cards.append(card)
        self.set_card(card)

    def discard(self, card):
        self.set_card(card, False)
        self.hand.remove(card)

    def play(self, new_hand):
        self.hand = new_hand

    def print_cards(self, cards):
        for card in cards:
            print(self.print_card(card), end=" ")

    def print_card(self, card):
        return(emoji.emojize(f"{card['value']}{card['suit']}"))

    def print_discard_options(self):
        print(f"\nDiscard options:")
        for i in range(len(self.hand)):
            print(f"{i+1}:{self.print_card(self.hand[i])}", end="  ")

    def value_meld_check(self, cards):
        switcher = {
            ":heart_suit:": "H", ":spade_suit:": "S", ":club_suit:": "C", ":diamond_suit:": "D"
        }
        melds = []
        unmatched_cards = cards.copy()
        for card in self.hand:
            count = 0

            if self.cards[f"{card['value']}H"] == True:
                count += 1
            if self.cards[f"{card['value']}S"] == True:
                count += 1
            if self.cards[f"{card['value']}C"] == True:
                count += 1
            if self.cards[f"{card['value']}D"] == True:
                count += 1

            if count > 2:
                if card in unmatched_cards:
                    unmatched_cards.remove(card)
                melds.append(card)

        return unmatched_cards, melds

    def suit_meld_check(self, cards):
        unmatched_cards = cards.copy()
        switcher = {
            ":heart_suit:": "H", ":spade_suit:": "S", ":club_suit:": "C", ":diamond_suit:": "D"
        }

        valueCards = {13: "K", 12: "Q", 11: "J", 10: "10", 9: "9", 8: "8", 7: "7", 6: "6",
                      5: "5", 4: "4", 3: "3", 2: "2", 1: "A"}

        melds = []

        for card in cards:
            run = 1

            try:
                above = int(card['order']) + 1
                while above < 14:
                    above_label = valueCards[above]
                    if self.cards[f"{above_label}{switcher[card['suit']]}"]:
                        run += 1
                        if run > 2:
                            if card in unmatched_cards:
                                unmatched_cards.remove(card)
                            if not card in melds:
                                melds.append(card)
                            break
                        above += 1
                    else:
                        break
            except Exception as e:
                print("Error matching above card, ", e)

            try:
                below = int(card['order']) - 1
                while below > 0:
                    below_label = valueCards[below]
                    if self.cards[f"{below_label}{switcher[card['suit']]}"]:
                        run += 1
                        if run > 2:
                            if card in unmatched_cards:
                                unmatched_cards.remove(card)
                            if not card in melds:
                                melds.append(card)
                            break
                        below -= 1
                    else:
                        break

            except Exception as e:
                print("Error matching below card, ", e, card)

        return unmatched_cards, melds

    def get_unmatched_pips(self, cards):
        pips = 0
        for card in cards:
            pips += card['pips']
            # print(card['value'], end=" ")
        return pips

    def score_check(self):
        hand = self.hand.copy()

        temp_unmatched, sf_suit_melds = self.suit_meld_check(hand)
        suit_first_unmatched,  sf_value_melds = self.value_meld_check(
            temp_unmatched)
        suit_first_score = self.get_unmatched_pips(suit_first_unmatched)

        hand = self.hand.copy()
        temp_unmatched,  vf_value_melds = self.value_meld_check(
            hand)
        value_first_unmatched, vf_suit_melds = self.suit_meld_check(
            temp_unmatched)
        value_first_score = self.get_unmatched_pips(value_first_unmatched)

        if suit_first_score <= value_first_score:
            self.unmatched_cards = suit_first_unmatched
            self.value_melds = sf_value_melds
            self.suit_melds = sf_suit_melds
            return suit_first_score
        else:
            self.unmatched_cards = value_first_unmatched
            self.value_melds = vf_value_melds
            self.suit_melds = vf_suit_melds
            self.unmatched_cards = value_first_unmatched
            return value_first_score

    def knock(self):
        if self.id == "human":
            print("The Human Knocked")
        else:
            print("The NPC Knocked")
        global knock
        pips = self.score_check()
        if pips > 90:
            print("You can't knock yet. Build more matches.")
            return False
        else:
            self.has_knocked = True
            return True

    def score_hand(self, opponent):
        if self.has_knocked:
            self.unmatched_pips = self.score_check()
            # print("")
            if self.unmatched_pips > 10:
                print("OH NO! you have too many pips to knock")
            # your oppent can play off you cards... so add all your cards to their deck and then recount their meld
        if self.id == "human":
            who = "HUMAN"
            opp = "COMPUTER"
        else:
            who = "COMPUTER"
            opp = "HUMAN"
        print(f"{who}\nMelds:", end=" ")
        self.print_cards(self.suit_melds)
        self.print_cards(self.value_melds)

        print("\nUnmatched cards:", end=" ")
        self.print_cards(self.unmatched_cards)

        print(f"\nTotal unmatched pips:{self.unmatched_pips}")

        opponent.score_check()

        print(f"\n{opp}\nMelds:", end=" ")
        opponent.print_cards(opponent.suit_melds)
        opponent.print_cards(opponent.value_melds)

        suit_melds = self.suit_melds
        value_melds = self.value_melds

        opponent_unmatched = opponent.layoff_value_check(
            opponent.unmatched_cards, value_melds)
        opponent_unmatched = opponent.layoff_suit_check(
            opponent_unmatched, suit_melds)
        opponent_unmatched_pips = opponent.get_unmatched_pips(
            opponent_unmatched)

        print("\nLayoffs:", end=" ")
        opponent.print_cards(opponent.lay_offs)

        print("\nUnmatched cards:", end=" ")
        opponent.print_cards(opponent_unmatched)
        print(f"\nTotal unmatched pips:{opponent_unmatched_pips}")

        if self.unmatched_pips < opponent_unmatched_pips:
            self.score += 10
            self.score += opponent_unmatched_pips - self.unmatched_pips

            if self.id == "human":
                print(
                    f"\nGood job!, you got {10 + opponent_unmatched_pips - self.unmatched_pips} points")
            else:
                print(
                    f"\nThe computer won {10 + opponent_unmatched_pips - self.unmatched_pips} points")
        else:
            print("\nThe knock was lost.")
            opponent.score += 25 - opponent_unmatched_pips + self.unmatched_pips

        # print("new scores: ", self.score, opponent.score)

    def layoff_value_check(self, cards, played_melds):
        for card in cards:
            for played_card in played_melds:
                if card['value'] == played_card['value']:
                    self.lay_offs.append(card)
                    cards.remove(card)
                    break
        return cards

    def layoff_suit_check(self, cards, played_melds):
        for card in cards:
            for played_card in played_melds:
                # the prblem here is if u have 2 cards that play, you need to do this on a loop until there are no results
                if card['suit'] == played_card['suit'] and (card['order'] == played_card['order']+1) or (card['order'] == played_card['order']-1):
                    self.lay_offs.append(card)
                    cards.remove(card)
                    break
        return cards
