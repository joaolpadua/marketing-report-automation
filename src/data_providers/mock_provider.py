import random


class MockProvider:

    def generate_campaigns(self):
        """
        Gera campanhas simuladas para um período.
        """

        campaigns = [
            "Search Brand",
            "Search Produto",
            "Display Remarketing"
        ]

        results = []

        for campaign in campaigns:

            impressions = random.randint(5000, 20000)
            clicks = random.randint(100, 800)
            cost = round(random.uniform(100, 800), 2)
            conversions = random.randint(5, 40)

            results.append({
                "campaign_name": campaign,
                "impressions": impressions,
                "clicks": clicks,
                "cost": cost,
                "conversions": conversions
            })

        return results


    def get_campaign_data(self, client):
        """
        Retorna dados simulados para dois períodos:
        semana atual e semana anterior.
        """

        current_data = self.generate_campaigns()
        previous_data = self.generate_campaigns()

        return {
            "current": current_data,
            "previous": previous_data
        }