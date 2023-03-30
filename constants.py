# SENTINEL_WORDS are terms that are often used by paid agent provocateurs to intentionally offend a particular CONTRA_TOPICS or user.
SENTINEL_WORDS = {'schwurbler': 1, 'verschwörungstheoretiker': 1, 'vtler': 1, 'dunning': 1, 'kruger': 1, 'flacherdler': 1, 'covidiot': 1, 'aluhut': 1, 'schwachsinn': 1, 'leerdenker': 1, 'querdenker': 1, 'paulanergarten': 1, 'impfgegner': 1}

# AGGRESSIVENESS_WORDS are terms that distract from a fair discussion, poison the atmosphere, and lead to nowhere, which is the intended goal.
AGGRESSIVENESS_WORDS = {'oberpfeife': 1, 'dummheit': 1, 'flasche': 1, 'vollpfosten': 1, 'idioten': 1, 'spinner': 1, 'rechtsextreme': 1, 'antisemit': 1, 'leugner': 1, 'rechter': 1}

# PRO_TOPICS are topics where paid influencers push, spread, or endorse as positive and serious threads.
PRO_TOPICS = {'co2': 1, 'klimawandel': 1, 'transgender': 1, 'flache erde': 1, 'flatearth': 1, 'alien': 1, 'impfskeptiker': 1, 'reichsbürger': 1, 'klimaleugner': 1}

# CONTRA_TOPICS are topics where ordinary people are critical or skeptical.
CONTRA_TOPICS = ['mondlandung', 'chemtrails', 'impfung', 'bilderberger', 'covid', 'alternative']

# PRO_ACCOUNTS are paid influencers who spread #PRO_TOPICS and use #AGGRESSIVENESS_WORDS and #SENTINEL_WORDS.
PRO_ACCOUNTS = ['@goldeneraluhut', '@volksverpetzer']

# CONTRA_ACCOUNTS are ordinary people discussing or spreading #CONTRA_TOPICS, but who may get distracted or attacked by #PRO_ACCOUNTS.
CONTRA_ACCOUNTS = ['@danieleganser', '@kenfm', '@mz_storymakers', '@maxotte_says']
