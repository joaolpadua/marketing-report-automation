"""
google_ads_client_provider.py

Provider para cenários onde cada cliente possui sua própria
conta Google Ads com credenciais individuais.

Esse modelo é menos comum em agências, mas o sistema
é preparado para suportar esse cenário.
"""


class GoogleAdsClientProvider:

    def __init__(self):
        """
        Inicializa provider.
        No futuro aqui entra configuração OAuth por cliente.
        """
        pass


    def get_campaign_data(self, client):
        """
        Busca dados de campanhas do cliente.

        Estrutura de retorno deve seguir padrão do sistema:

        {
            "current": [...],
            "previous": [...]
        }
        """

        raise NotImplementedError(
            "GoogleAdsClientProvider ainda não implementado"
        )