from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.player.participant.vars["payoff_"+Constants.name_in_url] = 0


class Offer(Page):
    form_model = 'player'
    form_fields = ['kept']

    def before_next_page(self):
        self.group.set_random_dictator()


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_group_data()
        self.group.set_payoffs()


class Results(Page):

    def before_next_page(self):
        # pass payoff to new var
        self.player.participant.vars["payoff_"+Constants.name_in_url] += self.player.payoff
        print(f"self.player.participant.vars['payoff_'+Constants.name_in_url] = {self.player.participant.vars['payoff_'+Constants.name_in_url]}")

    def vars_for_template(self):
        return {
            'offer': Constants.endowment - self.group.group_kept,
        }


page_sequence = [
    Introduction,
    Offer,
    ResultsWaitPage,
    Results
]
