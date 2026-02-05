#!/usr/bin/env python3
"""
NFL Conference Championship - Team vs Team Matchup
Championship Weekend: Jan 25-26, 2026

Team 1 vs Team 2 - Fantasy Scoring Breakdown

Usage:
    python championship_matchup.py

Author: Jon Korsgard  
Date: February 2026
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any


class ChampionshipMatchup:
    """Calculate fantasy points for two teams from Championship weekend"""
    
    def __init__(self):
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
        
        # Your league's CORRECT scoring rules
        self.scoring = {
            'passing_yards_per_point': 25,
            'passing_td': 8,
            'passing_2pt': 2,
            'interception': -3,
            'passing_bonus_300': 5,
            'passing_bonus_400': 10,
            'rushing_yards_per_point': 10,
            'rushing_td': 10,
            'rushing_2pt': 2,
            'rushing_bonus_100': 5,
            'rushing_bonus_200': 10,
            'reception': 1,
            'receiving_yards_per_point': 10,
            'receiving_td': 10,
            'receiving_2pt': 2,
            'receiving_bonus_100': 5,
            'receiving_bonus_200': 10,
            'fumble_lost': -3,
            'pat_made': 1,
            'pat_missed': -3,
            'fg_0_39': 3,
            'fg_40_49': 4,
            'fg_50_plus': 6,
            'fg_miss_0_39': -3,
            'fg_miss_40_49': -2,
            'fg_miss_50_plus': 0,
            'dst_points_0': 15,
            'dst_points_1_6': 12,
            'dst_points_7_13': 9,
            'dst_points_14_17': 6,
            'dst_points_18_21': 3,
            'dst_points_22_27': 0,
            'dst_points_28_34': -3,
            'dst_points_35_45': -6,
            'dst_points_46_plus': -9,
            'dst_sack': 1,
            'dst_interception': 5,
            'dst_fumble_recovery': 5,
            'dst_safety': 5,
            'dst_blocked_kick': 5,
            'dst_return_td': 5,
        }
        
        # Define the two teams
        self.team1 = {
            'name': 'TEAM 1',
            'roster': [
                ('Drake Maye', 'QB', 'NE'),
                ('RJ Harvey', 'RB', 'DEN'),
                ('Kyren Williams', 'RB', 'LAR'),
                ('Puka Nacua', 'WR', 'LAR'),
                ('Davante Adams', 'WR', 'LAR'),
                ('Hunter Henry', 'TE', 'NE'),
                ('Kayshon Boutte', 'WR', 'NE'),
                ('Patriots D/ST', 'D/ST', 'NE'),
                ('Jason Myers', 'K', 'SEA'),
            ]
        }
        
        self.team2 = {
            'name': 'TEAM 2',
            'roster': [
                ('Matthew Stafford', 'QB', 'LAR'),
                ('Kenneth Walker', 'RB', 'SEA'),
                ('Rhamondre Stevenson', 'RB', 'NE'),
                ('Jaxon Smith-Njigba', 'WR', 'SEA'),
                ('Courtland Sutton', 'WR', 'DEN'),
                ('Colby Parkinson', 'TE', 'LAR'),
                ('Stefon Diggs', 'WR', 'NE'),
                ('Seahawks D/ST', 'D/ST', 'SEA'),
                ('Will Lutz', 'K', 'DEN'),
            ]
        }
    
    def fetch_playoff_games(self) -> List[Dict]:
        """Fetch Championship weekend games"""
        print("Fetching Championship Weekend games...")
        
        url = f"{self.base_url}/scoreboard"
        params = {
            'dates': '20260125-20260126',
            'seasontype': 3,
            'limit': 100
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                print(f"✓ Found {len(events)} games\n")
                return events
            else:
                print(f"✗ API Error: {response.status_code}")
                return []
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            return []
    
    def fetch_game_stats(self, game_id: str) -> Dict:
        """Fetch detailed stats for a game"""
        url = f"{self.base_url}/summary"
        params = {'event': game_id}
        
        try:
            response = requests.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
    
    def calculate_fantasy_points(self, stats: Dict) -> float:
        """Calculate fantasy points"""
        points = 0.0
        
        # PASSING
        pass_yds = stats.get('passing_yards', 0)
        pass_tds = stats.get('passing_tds', 0)
        pass_2pt = stats.get('passing_2pt', 0)
        ints = stats.get('interceptions', 0)
        
        if pass_yds > 0 or pass_tds > 0:
            points += pass_yds / self.scoring['passing_yards_per_point']
            points += pass_tds * self.scoring['passing_td']
            points += pass_2pt * self.scoring['passing_2pt']
            points += ints * self.scoring['interception']
            if 300 <= pass_yds < 400:
                points += self.scoring['passing_bonus_300']
            elif pass_yds >= 400:
                points += self.scoring['passing_bonus_400']
        
        # RUSHING
        rush_yds = stats.get('rushing_yards', 0)
        rush_tds = stats.get('rushing_tds', 0)
        rush_2pt = stats.get('rushing_2pt', 0)
        
        if rush_yds > 0 or rush_tds > 0:
            points += rush_yds / self.scoring['rushing_yards_per_point']
            points += rush_tds * self.scoring['rushing_td']
            points += rush_2pt * self.scoring['rushing_2pt']
            if 100 <= rush_yds < 200:
                points += self.scoring['rushing_bonus_100']
            elif rush_yds >= 200:
                points += self.scoring['rushing_bonus_200']
        
        # RECEIVING
        recs = stats.get('receptions', 0)
        rec_yds = stats.get('receiving_yards', 0)
        rec_tds = stats.get('receiving_tds', 0)
        rec_2pt = stats.get('receiving_2pt', 0)
        
        if recs > 0 or rec_tds > 0:
            points += recs * self.scoring['reception']
            points += rec_yds / self.scoring['receiving_yards_per_point']
            points += rec_tds * self.scoring['receiving_td']
            points += rec_2pt * self.scoring['receiving_2pt']
            if 100 <= rec_yds < 200:
                points += self.scoring['receiving_bonus_100']
            elif rec_yds >= 200:
                points += self.scoring['receiving_bonus_200']
        
        # FUMBLES
        fumbles = stats.get('fumbles_lost', 0)
        points += fumbles * self.scoring['fumble_lost']
        
        # KICKING
        pat_made = stats.get('pat_made', 0)
        pat_missed = stats.get('pat_missed', 0)
        fg_0_39 = stats.get('fg_0_39', 0)
        fg_40_49 = stats.get('fg_40_49', 0)
        fg_50_plus = stats.get('fg_50_plus', 0)
        fg_miss_0_39 = stats.get('fg_miss_0_39', 0)
        fg_miss_40_49 = stats.get('fg_miss_40_49', 0)
        
        points += pat_made * self.scoring['pat_made']
        points += pat_missed * self.scoring['pat_missed']
        points += fg_0_39 * self.scoring['fg_0_39']
        points += fg_40_49 * self.scoring['fg_40_49']
        points += fg_50_plus * self.scoring['fg_50_plus']
        points += fg_miss_0_39 * self.scoring['fg_miss_0_39']
        points += fg_miss_40_49 * self.scoring['fg_miss_40_49']
        
        # DEFENSE
        points_allowed = stats.get('points_allowed', -1)
        if points_allowed >= 0:
            if points_allowed == 0:
                points += self.scoring['dst_points_0']
            elif 1 <= points_allowed <= 6:
                points += self.scoring['dst_points_1_6']
            elif 7 <= points_allowed <= 13:
                points += self.scoring['dst_points_7_13']
            elif 14 <= points_allowed <= 17:
                points += self.scoring['dst_points_14_17']
            elif 18 <= points_allowed <= 21:
                points += self.scoring['dst_points_18_21']
            elif 22 <= points_allowed <= 27:
                points += self.scoring['dst_points_22_27']
            elif 28 <= points_allowed <= 34:
                points += self.scoring['dst_points_28_34']
            elif 35 <= points_allowed <= 45:
                points += self.scoring['dst_points_35_45']
            else:
                points += self.scoring['dst_points_46_plus']
        
        dst_sacks = stats.get('sacks', 0)
        dst_ints = stats.get('defensive_interceptions', 0)
        dst_fumbles = stats.get('fumble_recoveries', 0)
        dst_safeties = stats.get('safeties', 0)
        dst_blocked = stats.get('blocked_kicks', 0)
        dst_return_tds = stats.get('return_tds', 0)
        
        points += dst_sacks * self.scoring['dst_sack']
        points += dst_ints * self.scoring['dst_interception']
        points += dst_fumbles * self.scoring['dst_fumble_recovery']
        points += dst_safeties * self.scoring['dst_safety']
        points += dst_blocked * self.scoring['dst_blocked_kick']
        points += dst_return_tds * self.scoring['dst_return_td']
        
        return round(points, 2)
    
    def parse_defense_stats(self, game_data: Dict) -> Dict[str, Dict]:
        """
        Parse defense/special teams statistics.
        Returns dict keyed by team abbreviation with D/ST stats.
        """
        defense_stats = {}
        
        # Get final scores for points allowed
        header = game_data.get('header', {})
        competitions = header.get('competitions', [])
        if not competitions:
            return defense_stats
        
        competitors = competitions[0].get('competitors', [])
        
        # Build score lookup
        scores = {}
        for competitor in competitors:
            team_abbr = competitor.get('team', {}).get('abbreviation', '')
            score = int(competitor.get('score', 0))
            scores[team_abbr] = score
        
        # Parse defensive stats from boxscore
        boxscore = game_data.get('boxscore', {})
        players_data = boxscore.get('players', [])
        
        for team in players_data:
            team_info = team.get('team', {})
            team_abbr = team_info.get('abbreviation', 'UNK')
            
            # Points allowed (opponent's score)
            points_allowed = None
            for abbr, score in scores.items():
                if abbr != team_abbr:
                    points_allowed = score
                    break
            
            # Initialize defense stats
            defense_stats[team_abbr] = {
                'points_allowed': points_allowed if points_allowed is not None else 0,
                'sacks': 0,
                'defensive_interceptions': 0,
                'fumble_recoveries': 0,
                'safeties': 0,
                'blocked_kicks': 0,
                'return_tds': 0
            }
            
            # Sum defensive stats from all players
            statistics = team.get('statistics', [])
            
            for stat_cat in statistics:
                category = stat_cat.get('name', 'Unknown')
                labels = stat_cat.get('labels', [])
                athletes = stat_cat.get('athletes', [])
                
                if category == 'defensive':
                    # Labels: ['TOT', 'SOLO', 'SACKS', 'TFL', 'PD', 'QB HTS', 'TD']
                    sacks_idx = labels.index('SACKS') if 'SACKS' in labels else -1
                    
                    if sacks_idx >= 0:
                        for athlete in athletes:
                            stats_array = athlete.get('stats', [])
                            if len(stats_array) > sacks_idx and stats_array[sacks_idx] != '--':
                                try:
                                    sacks = float(stats_array[sacks_idx])
                                    defense_stats[team_abbr]['sacks'] += sacks
                                except:
                                    pass
                
                elif category == 'interceptions':
                    # Labels: ['INT', 'YDS', 'TD']
                    for athlete in athletes:
                        stats_array = athlete.get('stats', [])
                        
                        # Count INTs
                        if len(stats_array) > 0 and stats_array[0] != '--':
                            try:
                                ints = int(stats_array[0])
                                defense_stats[team_abbr]['defensive_interceptions'] += ints
                            except:
                                pass
                        
                        # Count INT return TDs
                        if len(stats_array) > 2 and stats_array[2] != '--':
                            try:
                                int_tds = int(stats_array[2])
                                defense_stats[team_abbr]['return_tds'] += int_tds
                            except:
                                pass
        
        # Parse fumble recoveries and blocked kicks from play-by-play
        import re
        drives_data = game_data.get('drives', {})
        previous_drives = drives_data.get('previous', [])
        
        for drive in previous_drives:
            plays = drive.get('plays', [])
            
            for play in plays:
                text = play.get('text', '')
                text_lower = text.lower()
                
                # Look for fumble recoveries
                if 'fumble' in text_lower and 'recovered by' in text_lower:
                    # Extract team that recovered
                    # Format: "FUMBLES (player) [player], RECOVERED by TEAM-Player"
                    match = re.search(r'recovered by ([A-Z]{2,3})-', text, re.IGNORECASE)
                    if match:
                        recovering_team = match.group(1)
                        if recovering_team in defense_stats:
                            defense_stats[recovering_team]['fumble_recoveries'] += 1
                
                # Look for muffed punts/kicks recovered (also counts as fumble recovery)
                if 'muff' in text_lower and 'recovered by' in text_lower:
                    # Format: "X.Smith MUFFS catch, RECOVERED by SEA-D.Young"
                    match = re.search(r'recovered by ([A-Z]{2,3})-', text, re.IGNORECASE)
                    if match:
                        recovering_team = match.group(1)
                        if recovering_team in defense_stats:
                            defense_stats[recovering_team]['fumble_recoveries'] += 1
                
                # Look for blocked kicks
                if 'blocked' in text_lower and ('field goal' in text_lower or 'kick' in text_lower):
                    # Check if this play has teamParticipants showing which team made the block
                    team_participants = play.get('teamParticipants', [])
                    
                    # Look for the team with type="defense" (they made the block)
                    for participant in team_participants:
                        if participant.get('type') == 'defense':
                            team_id = participant.get('id')
                            
                            # Find this team's abbreviation in boxscore
                            blocking_team = None
                            for team_data in players_data:
                                team_info_check = team_data.get('team', {})
                                if team_info_check.get('id') == team_id:
                                    blocking_team = team_info_check.get('abbreviation')
                                    break
                            
                            # Increment that team's blocked kicks
                            if blocking_team and blocking_team in defense_stats:
                                defense_stats[blocking_team]['blocked_kicks'] += 1
                            break  # Only process first defense participant

        
        return defense_stats
    
    def parse_kicker_stats(self, game_data: Dict) -> Dict[str, Dict]:
        """
        Parse kicker statistics from play-by-play data.
        Returns dict keyed by kicker name with their stats.
        """
        import re
        
        kicker_stats = {}
        
        # Get play-by-play from drives
        drives_data = game_data.get('drives', {})
        previous_drives = drives_data.get('previous', [])
        
        for drive in previous_drives:
            plays = drive.get('plays', [])
            
            for play in plays:
                text = play.get('text', '').lower()
                
                # Look for field goal attempts
                if 'field goal' in text:
                    # Extract kicker name (before "yard field goal")
                    # Format: "W.Lutz 54 yard field goal is No Good"
                    fg_match = re.search(r'([a-z]+\.[a-z]+)\s+(\d+)\s+yard\s+field\s+goal', text, re.IGNORECASE)
                    
                    if fg_match:
                        kicker_name = fg_match.group(1)
                        distance = int(fg_match.group(2))
                        
                        # Initialize kicker if not exists
                        if kicker_name not in kicker_stats:
                            kicker_stats[kicker_name] = {
                                'pat_made': 0,
                                'pat_missed': 0,
                                'fg_0_39': 0,
                                'fg_40_49': 0,
                                'fg_50_plus': 0,
                                'fg_miss_0_39': 0,
                                'fg_miss_40_49': 0,
                                'fg_miss_50_plus': 0
                            }
                        
                        # Determine if made or missed
                        is_good = 'is good' in text
                        is_blocked = 'blocked' in text
                        is_missed = 'no good' in text or 'missed' in text or is_blocked
                        
                        # Categorize by distance and result
                        if is_good:
                            if distance <= 39:
                                kicker_stats[kicker_name]['fg_0_39'] += 1
                            elif distance <= 49:
                                kicker_stats[kicker_name]['fg_40_49'] += 1
                            else:
                                kicker_stats[kicker_name]['fg_50_plus'] += 1
                        elif is_missed:
                            if distance <= 39:
                                kicker_stats[kicker_name]['fg_miss_0_39'] += 1
                            elif distance <= 49:
                                kicker_stats[kicker_name]['fg_miss_40_49'] += 1
                            else:
                                # No penalty for 50+ yard misses
                                kicker_stats[kicker_name]['fg_miss_50_plus'] += 1
                
                # Look for extra points
                elif 'extra point' in text:
                    # Format: "W.Lutz extra point is GOOD"
                    pat_match = re.search(r'([a-z]+\.[a-z]+)\s+extra\s+point', text, re.IGNORECASE)
                    
                    if pat_match:
                        kicker_name = pat_match.group(1)
                        
                        # Initialize kicker if not exists
                        if kicker_name not in kicker_stats:
                            kicker_stats[kicker_name] = {
                                'pat_made': 0,
                                'pat_missed': 0,
                                'fg_0_39': 0,
                                'fg_40_49': 0,
                                'fg_50_plus': 0,
                                'fg_miss_0_39': 0,
                                'fg_miss_40_49': 0,
                                'fg_miss_50_plus': 0
                            }
                        
                        # Check if made or missed
                        is_good = 'is good' in text
                        is_blocked = 'blocked' in text or 'no good' in text
                        
                        if is_good:
                            kicker_stats[kicker_name]['pat_made'] += 1
                        else:
                            kicker_stats[kicker_name]['pat_missed'] += 1
        
        return kicker_stats
    
    def parse_kicker_stats(self, game_data: Dict) -> Dict[str, Dict]:
        """
        Parse kicker statistics from play-by-play data.
        Returns dict keyed by kicker name with their stats.
        """
        kickers = {}
        
        # Get play-by-play data
        drives_data = game_data.get('drives', {})
        previous_drives = drives_data.get('previous', [])
        
        import re
        
        for drive in previous_drives:
            plays = drive.get('plays', [])
            
            for play in plays:
                text = play.get('text', '').lower()
                
                # Look for field goal attempts
                if 'field goal' in text:
                    # Extract kicker name (format: "Name yards field goal")
                    # Example: "W.Lutz 54 yard field goal is No Good"
                    name_match = re.search(r'([A-Z]\.[A-Za-z]+)', play.get('text', ''))
                    if name_match:
                        kicker_name = name_match.group(1)
                        
                        # Initialize kicker if not exists
                        if kicker_name not in kickers:
                            kickers[kicker_name] = {
                                'name': kicker_name,
                                'pat_made': 0,
                                'pat_missed': 0,
                                'fg_0_39': 0,
                                'fg_40_49': 0,
                                'fg_50_plus': 0,
                                'fg_miss_0_39': 0,
                                'fg_miss_40_49': 0,
                                'fg_miss_50_plus': 0
                            }
                        
                        # Extract distance
                        dist_match = re.search(r'(\d+)\s*yard', text)
                        if dist_match:
                            distance = int(dist_match.group(1))
                            
                            # Check if made or missed
                            is_good = 'is good' in text or kicker_name.lower() in text and 'is good' in text
                            is_missed = 'no good' in text or 'missed' in text or 'blocked' in text
                            
                            # Categorize by distance and result
                            if is_good:
                                if distance <= 39:
                                    kickers[kicker_name]['fg_0_39'] += 1
                                elif 40 <= distance <= 49:
                                    kickers[kicker_name]['fg_40_49'] += 1
                                else:  # 50+
                                    kickers[kicker_name]['fg_50_plus'] += 1
                            elif is_missed:
                                if distance <= 39:
                                    kickers[kicker_name]['fg_miss_0_39'] += 1
                                elif 40 <= distance <= 49:
                                    kickers[kicker_name]['fg_miss_40_49'] += 1
                                else:  # 50+
                                    kickers[kicker_name]['fg_miss_50_plus'] += 1
                
                # Look for extra points
                elif 'extra point' in text:
                    # Format: "W.Lutz extra point is GOOD"
                    # Need to find name directly before "extra point"
                    pat_match = re.search(r'([A-Z]\.[A-Za-z]+)\s+extra\s+point', play.get('text', ''))
                    
                    if pat_match:
                        kicker_name = pat_match.group(1)
                        
                        if kicker_name not in kickers:
                            kickers[kicker_name] = {
                                'name': kicker_name,
                                'pat_made': 0,
                                'pat_missed': 0,
                                'fg_0_39': 0,
                                'fg_40_49': 0,
                                'fg_50_plus': 0,
                                'fg_miss_0_39': 0,
                                'fg_miss_40_49': 0,
                                'fg_miss_50_plus': 0
                            }
                        
                        if 'is good' in text:
                            kickers[kicker_name]['pat_made'] += 1
                        elif 'no good' in text or 'missed' in text or 'blocked' in text:
                            kickers[kicker_name]['pat_missed'] += 1
        
        return kickers
    
    def parse_all_players(self, game_data: Dict) -> Dict[str, Dict]:
        """Parse all players and return dictionary by name"""
        players_dict = {}
        
        boxscore = game_data.get('boxscore', {})
        if not boxscore:
            return players_dict
        
        players_data = boxscore.get('players', [])
        
        for team in players_data:
            team_info = team.get('team', {})
            team_abbr = team_info.get('abbreviation', 'UNK')
            statistics = team.get('statistics', [])
            
            for stat_category in statistics:
                category = stat_category.get('name', '').lower()
                athletes = stat_category.get('athletes', [])
                
                for athlete in athletes:
                    athlete_info = athlete.get('athlete', {})
                    player_name = athlete_info.get('displayName', 'Unknown')
                    player_id = athlete_info.get('id', player_name)
                    position = athlete_info.get('position', {}).get('abbreviation', 'N/A')
                    stats_array = athlete.get('stats', [])
                    
                    player_key = f"{team_abbr}_{player_id}"
                    
                    if player_key not in players_dict:
                        players_dict[player_key] = {
                            'name': player_name,
                            'team': team_abbr,
                            'position': position,
                            'passing_yards': 0,
                            'passing_tds': 0,
                            'passing_2pt': 0,
                            'interceptions': 0,
                            'rushing_yards': 0,
                            'rushing_tds': 0,
                            'rushing_2pt': 0,
                            'receptions': 0,
                            'receiving_yards': 0,
                            'receiving_tds': 0,
                            'receiving_2pt': 0,
                            'fumbles_lost': 0
                        }
                    
                    try:
                        if category == 'passing' and len(stats_array) >= 5:
                            # CORRECT INDICES: Index 1=YDS, Index 3=TD, Index 4=INT
                            players_dict[player_key]['passing_yards'] += int(stats_array[1]) if stats_array[1] != '--' else 0
                            players_dict[player_key]['passing_tds'] += int(stats_array[3]) if stats_array[3] != '--' else 0
                            players_dict[player_key]['interceptions'] += int(stats_array[4]) if stats_array[4] != '--' else 0
                        elif category == 'rushing' and len(stats_array) >= 4:
                            players_dict[player_key]['rushing_yards'] += int(stats_array[1]) if stats_array[1] != '--' else 0
                            players_dict[player_key]['rushing_tds'] += int(stats_array[3]) if stats_array[3] != '--' else 0
                        elif category == 'receiving' and len(stats_array) >= 4:
                            players_dict[player_key]['receptions'] += int(stats_array[0]) if stats_array[0] != '--' else 0
                            players_dict[player_key]['receiving_yards'] += int(stats_array[1]) if stats_array[1] != '--' else 0
                            players_dict[player_key]['receiving_tds'] += int(stats_array[3]) if stats_array[3] != '--' else 0
                        elif category == 'fumbles' and len(stats_array) >= 2:
                            # ADDED: Parse fumbles lost
                            players_dict[player_key]['fumbles_lost'] += int(stats_array[1]) if stats_array[1] != '--' else 0
                    except:
                        continue
        
        return players_dict
    
    def find_player(self, player_name: str, team_abbr: str, all_players: Dict) -> Dict:
        """Find a player in the all_players dictionary"""
        # Try exact match first
        for key, player in all_players.items():
            if player['name'] == player_name and player['team'] == team_abbr:
                return player
        
        # Try partial match
        for key, player in all_players.items():
            if player_name.lower() in player['name'].lower() and player['team'] == team_abbr:
                return player
        
        # Return empty player
        return {
            'name': player_name,
            'team': team_abbr,
            'position': 'N/A',
            'passing_yards': 0,
            'passing_tds': 0,
            'passing_2pt': 0,
            'interceptions': 0,
            'rushing_yards': 0,
            'rushing_tds': 0,
            'rushing_2pt': 0,
            'receptions': 0,
            'receiving_yards': 0,
            'receiving_tds': 0,
            'receiving_2pt': 0,
            'fumbles_lost': 0
        }
    
    def find_kicker(self, player_name: str, all_kickers: Dict) -> Dict:
        """Find a kicker in the kicker stats dictionary"""
        # Kickers are stored with format "W.Lutz" in play-by-play
        # Try to match last name
        last_name = player_name.split()[-1].lower()
        
        for kicker_key, stats in all_kickers.items():
            if last_name in kicker_key.lower():
                return stats.copy()
        
        # Return empty kicker stats
        return {
            'pat_made': 0,
            'pat_missed': 0,
            'fg_0_39': 0,
            'fg_40_49': 0,
            'fg_50_plus': 0,
            'fg_miss_0_39': 0,
            'fg_miss_40_49': 0,
            'fg_miss_50_plus': 0
        }
    
    def display_team_results(self, team_data: Dict, team_results: List[Dict]):
        """Display fantasy results for a team"""
        print(f"\n{'='*80}")
        print(f"{team_data['name']} - CHAMPIONSHIP WEEKEND RESULTS")
        print(f"{'='*80}\n")
        
        total_points = 0.0
        
        for i, player_result in enumerate(team_results, 1):
            name = player_result['name']
            pos = player_result['roster_pos']
            team = player_result['team']
            pts = player_result['points']
            stats = player_result['stats']
            
            total_points += pts
            
            print(f"{i}. {name} ({pos}, {team}) - {pts} pts")
            
            # Show relevant stats (check if keys exist first)
            if stats.get('passing_yards', 0) > 0:
                print(f"   Passing: {stats.get('passing_yards', 0)} yds, {stats.get('passing_tds', 0)} TD, {stats.get('interceptions', 0)} INT")
            if stats.get('rushing_yards', 0) > 0:
                print(f"   Rushing: {stats.get('rushing_yards', 0)} yds, {stats.get('rushing_tds', 0)} TD")
            if stats.get('receptions', 0) > 0:
                print(f"   Receiving: {stats.get('receptions', 0)} rec, {stats.get('receiving_yards', 0)} yds, {stats.get('receiving_tds', 0)} TD")
            
            # Show defense stats
            if pos == 'D/ST' or stats.get('position') == 'D/ST':
                pa = stats.get('points_allowed', 0)
                sacks = stats.get('sacks', 0)
                ints = stats.get('defensive_interceptions', 0)
                fum_rec = stats.get('fumble_recoveries', 0)
                ret_tds = stats.get('return_tds', 0)
                
                print(f"   Points Allowed: {pa}")
                print(f"   Sacks: {sacks}, INTs: {ints}, Fumbles Recovered: {fum_rec}")
                if ret_tds > 0:
                    print(f"   Return TDs: {ret_tds}")
            
            # Show offense D/ST stats (for backwards compatibility)
            elif stats.get('points_allowed', -1) >= 0:
                print(f"   Defense: {stats.get('points_allowed', 0)} pts allowed, {stats.get('sacks', 0)} sacks")
            
            # Show kicker stats
            if pos == 'K':
                fg_made = stats.get('fg_0_39', 0) + stats.get('fg_40_49', 0) + stats.get('fg_50_plus', 0)
                fg_miss = stats.get('fg_miss_0_39', 0) + stats.get('fg_miss_40_49', 0) + stats.get('fg_miss_50_plus', 0)
                pat_made = stats.get('pat_made', 0)
                pat_miss = stats.get('pat_missed', 0)
                
                if fg_made > 0 or fg_miss > 0 or pat_made > 0:
                    print(f"   FG: {fg_made}/{fg_made + fg_miss}, XP: {pat_made}/{pat_made + pat_miss}")
                    if stats.get('fg_0_39', 0) > 0:
                        print(f"     0-39 yds: {stats['fg_0_39']} made")
                    if stats.get('fg_40_49', 0) > 0:
                        print(f"     40-49 yds: {stats['fg_40_49']} made")
                    if stats.get('fg_50_plus', 0) > 0:
                        print(f"     50+ yds: {stats['fg_50_plus']} made")
                    if stats.get('fg_miss_0_39', 0) > 0:
                        print(f"     0-39 yds: {stats['fg_miss_0_39']} missed (-3 pts each)")
                    if stats.get('fg_miss_40_49', 0) > 0:
                        print(f"     40-49 yds: {stats['fg_miss_40_49']} missed (-2 pts each)")
                    if stats.get('fg_miss_50_plus', 0) > 0:
                        print(f"     50+ yds: {stats['fg_miss_50_plus']} missed (0 pts)")
            
            print()
        
        print(f"{'='*80}")
        print(f"TOTAL POINTS: {total_points}")
        print(f"{'='*80}\n")
        
        return total_points
    
    def run_matchup(self):
        """Run the team vs team matchup"""
        print("\n" + "="*80)
        print("NFL CONFERENCE CHAMPIONSHIP - TEAM VS TEAM MATCHUP")
        print("="*80)
        print("Weekend: Jan 25-26, 2026")
        print("="*80 + "\n")
        
        # Fetch games
        games = self.fetch_playoff_games()
        if not games:
            print("✗ No games found")
            return
        
        # Collect all player stats, kicker stats, and defense stats
        all_players = {}
        all_kickers = {}
        all_defenses = {}
        
        for event in games:
            game_id = event.get('id')
            game_data = self.fetch_game_stats(game_id)
            if game_data:
                # Get offensive player stats
                players = self.parse_all_players(game_data)
                all_players.update(players)
                
                # Get kicker stats from play-by-play
                kickers = self.parse_kicker_stats(game_data)
                all_kickers.update(kickers)
                
                # Get defense stats
                defenses = self.parse_defense_stats(game_data)
                all_defenses.update(defenses)
        
        print(f"\n✓ Parsed {len(all_players)} offensive players")
        print(f"✓ Parsed {len(all_kickers)} kickers from play-by-play")
        print(f"✓ Parsed {len(all_defenses)} defenses\n")
        
        # Calculate Team 1 results
        team1_results = []
        print("\n[DEBUG] Processing Team 1 roster...")
        for player_name, roster_pos, team_abbr in self.team1['roster']:
            print(f"[DEBUG] Processing: {player_name} ({roster_pos}, {team_abbr})")
            
            if 'D/ST' in player_name or 'DST' in player_name:
                # Handle defense - look up actual stats
                if team_abbr in all_defenses:
                    player_stats = all_defenses[team_abbr].copy()
                    player_stats['name'] = player_name
                    player_stats['team'] = team_abbr
                    player_stats['position'] = 'D/ST'
                else:
                    player_stats = {
                        'name': player_name,
                        'team': team_abbr,
                        'position': 'D/ST',
                        'points_allowed': 0,
                        'sacks': 0,
                        'defensive_interceptions': 0,
                        'fumble_recoveries': 0,
                        'safeties': 0,
                        'blocked_kicks': 0,
                        'return_tds': 0
                    }
            elif roster_pos == 'K':
                # Handle kicker - look up in kicker stats
                player_stats = self.find_kicker(player_name, all_kickers)
                player_stats['name'] = player_name
                player_stats['team'] = team_abbr
                player_stats['position'] = 'K'
            else:
                player_stats = self.find_player(player_name, team_abbr, all_players)
            
            fantasy_points = self.calculate_fantasy_points(player_stats)
            
            # Debug output for D/ST
            if roster_pos == 'D/ST':
                print(f"\n[DEBUG] {player_name} stats being calculated:")
                print(f"  Points Allowed: {player_stats.get('points_allowed', 'N/A')}")
                print(f"  Sacks: {player_stats.get('sacks', 'N/A')}")
                print(f"  INTs: {player_stats.get('defensive_interceptions', 'N/A')}")
                print(f"  Fumbles: {player_stats.get('fumble_recoveries', 'N/A')}")
                print(f"  Blocked Kicks: {player_stats.get('blocked_kicks', 'N/A')}")
                print(f"  Return TDs: {player_stats.get('return_tds', 'N/A')}")
                print(f"  Calculated Points: {fantasy_points}\n")
            
            team1_results.append({
                'name': player_name,
                'roster_pos': roster_pos,
                'team': team_abbr,
                'points': fantasy_points,
                'stats': player_stats
            })
        
        # Calculate Team 2 results
        team2_results = []
        for player_name, roster_pos, team_abbr in self.team2['roster']:
            if 'D/ST' in player_name or 'DST' in player_name:
                # Handle defense - look up actual stats
                if team_abbr in all_defenses:
                    player_stats = all_defenses[team_abbr].copy()
                    player_stats['name'] = player_name
                    player_stats['team'] = team_abbr
                    player_stats['position'] = 'D/ST'
                else:
                    player_stats = {
                        'name': player_name,
                        'team': team_abbr,
                        'position': 'D/ST',
                        'points_allowed': 0,
                        'sacks': 0,
                        'defensive_interceptions': 0,
                        'fumble_recoveries': 0,
                        'safeties': 0,
                        'blocked_kicks': 0,
                        'return_tds': 0
                    }
            elif roster_pos == 'K':
                # Handle kicker - look up in kicker stats
                player_stats = self.find_kicker(player_name, all_kickers)
                player_stats['name'] = player_name
                player_stats['team'] = team_abbr
                player_stats['position'] = 'K'
            else:
                player_stats = self.find_player(player_name, team_abbr, all_players)
            
            fantasy_points = self.calculate_fantasy_points(player_stats)
            
            # Debug output for D/ST
            if roster_pos == 'D/ST':
                print(f"\n[DEBUG] {player_name} stats being calculated:")
                print(f"  Points Allowed: {player_stats.get('points_allowed', 'N/A')}")
                print(f"  Sacks: {player_stats.get('sacks', 'N/A')}")
                print(f"  INTs: {player_stats.get('defensive_interceptions', 'N/A')}")
                print(f"  Fumbles: {player_stats.get('fumble_recoveries', 'N/A')}")
                print(f"  Blocked Kicks: {player_stats.get('blocked_kicks', 'N/A')}")
                print(f"  Return TDs: {player_stats.get('return_tds', 'N/A')}")
                print(f"  Calculated Points: {fantasy_points}\n")
            
            team2_results.append({
                'name': player_name,
                'roster_pos': roster_pos,
                'team': team_abbr,
                'points': fantasy_points,
                'stats': player_stats
            })
        
        # Display results
        team1_total = self.display_team_results(self.team1, team1_results)
        team2_total = self.display_team_results(self.team2, team2_results)
        
        # Show winner
        print("\n" + "="*80)
        print("FINAL SCORE")
        print("="*80)
        print(f"{self.team1['name']}: {team1_total:.2f} points")
        print(f"{self.team2['name']}: {team2_total:.2f} points")
        print("="*80)
        
        if team1_total > team2_total:
            print(f"\n🏆 {self.team1['name']} WINS by {team1_total - team2_total:.2f} points!")
        elif team2_total > team1_total:
            print(f"\n🏆 {self.team2['name']} WINS by {team2_total - team1_total:.2f} points!")
        else:
            print(f"\n🤝 TIE GAME!")
        print()


def main():
    matchup = ChampionshipMatchup()
    matchup.run_matchup()


if __name__ == '__main__':
    main()
