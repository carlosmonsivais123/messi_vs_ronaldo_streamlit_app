class GeneralComponents:
    def competition_type_dictionary_argcontains(self, item):
        competition_type_dict={"World Cup": ["World Cup"],
                               "League": ["Primeira Liga", "Premier League", "La Liga", "Serie A", "Pro League", "MLS", "Ligue 1"],
                               "Champions League": ["Champions Lg"],
                               "Europa League": ["UEFA Cup", "Europa Lg"],
                               "League Cups": ["Coupe de France", "Coppa Italia", "Copa del Rey", "Super Cup", "FA Cup", 
                                               "Trophée des Champions", "Supercopa de España", "Supercoppa"],
                               "Friendlies": ["Friendlies (M)"],
                               "International Tournaments": ["Copa América", "Copa América Centenario", "UEFA Nations League", 
                                                             "FIFA Confederations Cup", "UEFA Euro", "UEFA Euro Qualifying", "WCQ"]}

        for i, v in competition_type_dict.items():
            if item in v:
                return i
