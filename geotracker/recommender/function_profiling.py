import pstats
p = pstats.Stats('raw_data/recommender_profile.txt')
p.sort_stats('cumulative').print_stats(50)
