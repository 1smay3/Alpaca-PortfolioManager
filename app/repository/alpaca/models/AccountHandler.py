from app.repository.alpaca.alpaca_service import AlpacaService
from app.repository.alpaca.models.Account import LocalAccount
from app.repository.alpaca.models.PortfolioHistory import LocalPortfolioHistory

alpaca = AlpacaService()


class AccountHandler:
    personalAccount = None
    portfolioHistory = None

    def refresh_account(self):
        account_observable = alpaca.get_account()
        account_observable.subscribe(lambda remoteAccount: self._create_account(remoteAccount))

    def refresh_portfolio_history(self):
        account_observable = alpaca.get_portfolio_history()
        account_observable.subscribe(lambda remoteHistory: self._create_portfolio_history(remoteHistory))

    def _create_account(self, remoteAccount):
        self.personalAccount = LocalAccount(remoteAccount=remoteAccount)

    def _create_portfolio_history(self, remoteHistory):
        print(remoteHistory)
        self.portfolioHistory = LocalPortfolioHistory(remoteHistory=remoteHistory)
