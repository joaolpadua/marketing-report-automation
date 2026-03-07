import random


class MockProvider:

    def get_campaign_data(self, client):

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