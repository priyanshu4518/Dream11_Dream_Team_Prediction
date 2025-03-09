#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import json 
import pandas as pd
#function for calculating fantasy points through json file of ball by ball
# Point system constants
BAT_POINT_RUN = 1
BAT_POINT_BOUNDARY = 1
BAT_POINT_SIX = 2
BAT_POINT_HALF_CENTURY = 4
BAT_POINT_CENTURY = 8
BAT_POINT_DUCK = -3

BOWL_POINT_WICKET = 25
BOWL_POINT_BONUS = 8
BOWL_POINT_4_WICKET_BONUS = 4
BOWL_POINT_5_WICKET_BONUS = 8
BOWL_POINT_MAIDEN = 4

FIELD_POINT_CATCH = 8
FIELD_POINT_3_CATCH_BONUS = 4
FIELD_POINT_STUMPING = 12
FIELD_POINT_RUN_OUT_DIRECT = 12
FIELD_POINT_RUN_OUT = 6

ECONOMY_POINT_2_5 = 6
ECONOMY_POINT_3_49 = 4
ECONOMY_POINT_4_5 = 2
ECONOMY_POINT_7_8 = -2
ECONOMY_POINT_8_9 = -4
ECONOMY_POINT_ABOVE_9 = -6

STRIKE_RATE_POINT_140 = 6
STRIKE_RATE_POINT_120_140 = 4
STRIKE_RATE_POINT_100_120 = 2
STRIKE_RATE_POINT_40_50 = -2
STRIKE_RATE_POINT_30_40 = -4
STRIKE_RATE_POINT_BELOW_30 = -6


def calculate_fantasy_points_from_json(json_file):
    with open(json_file, 'r') as f:
        match_data = json.load(f)

    # Initialize fantasy points
    players = {player: 0 for team in match_data['info']['players'].values() for player in team}
    batter_scores = {player: 0 for player in players}
    bowler_wickets = {player: 0 for player in players}
    fielder_catches = {player: 0 for player in players}
    batter_balls = {player: 0 for player in players}
    bowler_runs = {player: 0 for player in players}
    bowler_balls = {player: 0 for player in players}

    # Process deliveries
    for inning in match_data.get('innings', []):
        for over in inning['overs']:
            for delivery in over['deliveries']:
                batter = delivery['batter']
                bowler = delivery['bowler']
                runs = delivery['runs']['batter']
                wickets = delivery.get('wickets', [])

                # Batting points
                players[batter] += BAT_POINT_RUN * runs
                batter_scores[batter] += runs
                batter_balls[batter] += 1
                if runs >= 6:
                    players[batter] += BAT_POINT_SIX
                elif runs >= 4:
                    players[batter] += BAT_POINT_BOUNDARY

                if any(wicket['player_out'] == batter for wicket in wickets) and batter_scores[batter] == 0:
                    players[batter] += BAT_POINT_DUCK

                # Bowling and fielding points
                for wicket in wickets:
                    if wicket['kind'] != 'run out':
                        players[bowler] += BOWL_POINT_WICKET
                        bowler_wickets[bowler] += 1
                        if wicket['kind'] in ['lbw', 'bowled']:
                            players[bowler] += BOWL_POINT_BONUS
                    for fielder in wicket.get('fielders', []):
                        field_name = fielder['name']
                        if wicket['kind'] == 'caught':
                            players[field_name] += FIELD_POINT_CATCH
                            fielder_catches[field_name] += 1
                        elif wicket['kind'] == 'stumped':
                            players[field_name] += FIELD_POINT_STUMPING
                        elif wicket['kind'] == 'run out':
                            if 'direct_hit' in fielder:
                                players[field_name] += FIELD_POINT_RUN_OUT_DIRECT
                            else:
                                players[field_name] += FIELD_POINT_RUN_OUT

                # Update bowler stats
                bowler_runs[bowler] += runs
                bowler_balls[bowler] += 1

    # Additional scoring
    for player in batter_scores:
        if batter_scores[player] >= 100:
            players[player] += BAT_POINT_CENTURY
        elif batter_scores[player] >= 50:
            players[player] += BAT_POINT_HALF_CENTURY

    for player in fielder_catches:
        if fielder_catches[player] >= 3:
            players[player] += FIELD_POINT_3_CATCH_BONUS

    for player in bowler_wickets:
        if bowler_wickets[player] >= 5:
            players[player] += BOWL_POINT_5_WICKET_BONUS
        elif bowler_wickets[player] >= 4:
            players[player] += BOWL_POINT_4_WICKET_BONUS

    for player in bowler_runs:
        if bowler_balls[player] >= 30:
            economy_rate = bowler_runs[player] / (bowler_balls[player] / 6)
            if economy_rate < 2.5:
                players[player] += ECONOMY_POINT_2_5
            elif economy_rate < 3.5:
                players[player] += ECONOMY_POINT_3_49
            elif economy_rate < 4.5:
                players[player] += ECONOMY_POINT_4_5
            elif economy_rate >= 8 and economy_rate < 9:
                players[player] += ECONOMY_POINT_8_9
            elif economy_rate >= 9:
                players[player] += ECONOMY_POINT_ABOVE_9

    for player in batter_scores:
        if batter_balls[player] >= 20:
            strike_rate = (batter_scores[player] / batter_balls[player]) * 100
            if strike_rate > 140:
                players[player] += STRIKE_RATE_POINT_140
            elif strike_rate > 120:
                players[player] += STRIKE_RATE_POINT_120_140
            elif strike_rate > 100:
                players[player] += STRIKE_RATE_POINT_100_120
            elif strike_rate >= 40:
                players[player] += STRIKE_RATE_POINT_40_50
            elif strike_rate >= 30:
                players[player] += STRIKE_RATE_POINT_30_40
            elif strike_rate < 30:
                players[player] += STRIKE_RATE_POINT_BELOW_30

    return players 


