from app.repository.alpaca.AlpacaService import AlpacaService
from app.repository.alpaca.models.Account import LocalAccount
from app.repository.alpaca.models.PortfolioHistory import LocalPortfolioHistory
from app.repository.alpaca.models.Positions import RemotePositions

alpaca = AlpacaService()

"""
Makes network calls and passes to account -  static/metadata. Live trade data is handled in PortfolioManager
"""


class AccountHandler:
    personalAccount = None
    portfolioHistory = None
    portfolioPositions = None

    def refresh_account(self):
        account_observable = alpaca.get_account()
        account_observable.subscribe(lambda remoteAccount: self._create_account(remoteAccount))

    def refresh_portfolio_history(self):
        account_observable = alpaca.get_portfolio_history()
        account_observable.subscribe(lambda remoteHistory: self._create_portfolio_history(remoteHistory))

    def _create_account(self, remoteAccount):
        self.personalAccount = LocalAccount(remoteAccount=remoteAccount)

    def _create_portfolio_history(self, remoteHistory):
        self.portfolioHistory = LocalPortfolioHistory(remoteHistory=remoteHistory)
