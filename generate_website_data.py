#!/usr/bin/env python3
"""
Generate JSON data file for the NFL Playoff Fantasy Tracker website
This script outputs championship_results.json that the website reads
"""

import json
from datetime import datetime
from championship_matchup import ChampionshipMatchup

def format_player_stats(player_stats):
    """Format player stats into a readable string"""
    stats_parts = []
    pos = player_stats.get('position', 'N/A')
    
    if pos == 'QB':
        if player_stats.get('passing_yards', 0) > 0:
            stats_parts.append(f"{player_stats['passing_yards']} pass yds")
        if player_stats.get('passing_tds', 0) > 0:
            stats_parts.append(f"{player_stats['passing_tds']} pass TD")
        if player_stats.get('interceptions', 0) > 0:
            stats_parts.append(f"{player_stats['interceptions']} INT")
        if player_stats.get('rushing_yards', 0) > 0:
            stats_parts.append(f"{player_stats['rushing_yards']} rush yds")
        if player_stats.get('rushing_tds', 0) > 0:
            stats_parts.append(f"{player_stats['rushing_tds']} rush TD")
    
    elif pos in ['RB', 'WR', 'TE', 'FLEX']:
        if player_stats.get('rushing_yards', 0) > 0:
            stats_parts.append(f"{player_stats['rushing_yards']} rush yds")
        if player_stats.get('rushing_tds', 0) > 0:
            stats_parts.append(f"{player_stats['rushing_tds']} rush TD")
        if player_stats.get('receptions', 0) > 0:
            stats_parts.append(f"{player_stats['receptions']} rec")
        if player_stats.get('receiving_yards', 0) > 0:
            stats_parts.append(f"{player_stats['receiving_yards']} rec yds")
        if player_stats.get('receiving_tds', 0) > 0:
            stats_parts.append(f"{player_stats['receiving_tds']} rec TD")
    
    elif pos == 'K':
        fg_made = player_stats.get('fg_0_39', 0) + player_stats.get('fg_40_49', 0) + player_stats.get('fg_50_plus', 0)
        fg_miss = player_stats.get('fg_miss_0_39', 0) + player_stats.get('fg_miss_40_49', 0) + player_stats.get('fg_miss_50_plus', 0)
        pat_made = player_stats.get('pat_made', 0)
        pat_miss = player_stats.get('pat_missed', 0)
        stats_parts.append(f"{fg_made}/{fg_made + fg_miss} FG")
        stats_parts.append(f"{pat_made}/{pat_made + pat_miss} XP")
    
    elif pos == 'D/ST':
        pa = player_stats.get('points_allowed', 0)
        sacks = player_stats.get('sacks', 0)
        ints = player_stats.get('defensive_interceptions', 0)
        fum = player_stats.get('fumble_recoveries', 0)
        blk = player_stats.get('blocked_kicks', 0)
        
        stats_parts.append(f"{pa} PA")
        if sacks > 0:
            stats_parts.append(f"{int(sacks)} sack{'s' if sacks > 1 else ''}")
        if ints > 0:
            stats_parts.append(f"{ints} INT")
        if fum > 0:
            stats_parts.append(f"{fum} FR")
        if blk > 0:
            stats_parts.append(f"{blk} BLK")
    
    return ", ".join(stats_parts) if stats_parts else "No stats"


def generate_website_json():
    """Generate JSON file for website"""
    print("Generating website data...")
    
    # Create matchup instance
    matchup = ChampionshipMatchup()
    
    # Fetch games
    games = matchup.fetch_playoff_games()
    if not games:
        print("✗ No games found")
        return
    
    # Collect all stats
    all_players = {}
    all_kickers = {}
    all_defenses = {}
    
    for event in games:
        game_id = event.get('id')
        game_data = matchup.fetch_game_stats(game_id)
        if game_data:
            players = matchup.parse_all_players(game_data)
            all_players.update(players)
            
            kickers = matchup.parse_kicker_stats(game_data)
            all_kickers.update(kickers)
            
            defenses = matchup.parse_defense_stats(game_data)
            all_defenses.update(defenses)
    
    # Process Team 1
    team1_roster = []
    for player_name, roster_pos, team_abbr in matchup.team1['roster']:
        if 'D/ST' in player_name or 'DST' in player_name:
            if team_abbr in all_defenses:
                player_stats = all_defenses[team_abbr].copy()
                player_stats['name'] = player_name
                player_stats['team'] = team_abbr
                player_stats['position'] = 'D/ST'
            else:
                player_stats = {'name': player_name, 'team': team_abbr, 'position': 'D/ST'}
        elif roster_pos == 'K':
            player_stats = matchup.find_kicker(player_name, all_kickers)
            player_stats['name'] = player_name
            player_stats['team'] = team_abbr
            player_stats['position'] = 'K'
        else:
            player_stats = matchup.find_player(player_name, team_abbr, all_players)
        
        fantasy_points = matchup.calculate_fantasy_points(player_stats)
        
        team1_roster.append({
            "position": roster_pos,
            "name": player_name,
            "team": team_abbr,
            "stats": format_player_stats(player_stats),
            "points": round(fantasy_points, 2)
        })
    
    # Process Team 2
    team2_roster = []
    for player_name, roster_pos, team_abbr in matchup.team2['roster']:
        if 'D/ST' in player_name or 'DST' in player_name:
            if team_abbr in all_defenses:
                player_stats = all_defenses[team_abbr].copy()
                player_stats['name'] = player_name
                player_stats['team'] = team_abbr
                player_stats['position'] = 'D/ST'
            else:
                player_stats = {'name': player_name, 'team': team_abbr, 'position': 'D/ST'}
        elif roster_pos == 'K':
            player_stats = matchup.find_kicker(player_name, all_kickers)
            player_stats['name'] = player_name
            player_stats['team'] = team_abbr
            player_stats['position'] = 'K'
        else:
            player_stats = matchup.find_player(player_name, team_abbr, all_players)
        
        fantasy_points = matchup.calculate_fantasy_points(player_stats)
        
        team2_roster.append({
            "position": roster_pos,
            "name": player_name,
            "team": team_abbr,
            "stats": format_player_stats(player_stats),
            "points": round(fantasy_points, 2)
        })
    
    # Calculate totals
    team1_total = sum(p['points'] for p in team1_roster)
    team2_total = sum(p['points'] for p in team2_roster)
    
    # Get top performers (combine both rosters and sort)
    all_roster = team1_roster + team2_roster
    top_performers = sorted(all_roster, key=lambda x: x['points'], reverse=True)[:5]
    
    for i, performer in enumerate(top_performers, 1):
        performer['rank'] = i
    
    # Build final JSON structure
    data = {
        "generated_at": datetime.now().isoformat(),
        "weekend": "Conference Championships - Jan 25-26, 2026",
        "team1": {
            "name": matchup.team1['name'],
            "total_points": round(team1_total, 2),
            "roster": team1_roster
        },
        "team2": {
            "name": matchup.team2['name'],
            "total_points": round(team2_total, 2),
            "roster": team2_roster
        },
        "top_performers": top_performers
    }
    
    # Write to file
    output_file = 'championship_results.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Generated {output_file}")
    print(f"  {matchup.team1['name']}: {team1_total:.2f} points")
    print(f"  {matchup.team2['name']}: {team2_total:.2f} points")
    
    if team1_total > team2_total:
        print(f"\n🏆 {matchup.team1['name']} WINS by {team1_total - team2_total:.2f} points!")
    elif team2_total > team1_total:
        print(f"\n🏆 {matchup.team2['name']} WINS by {team2_total - team1_total:.2f} points!")
    else:
        print("\n🤝 TIE GAME!")


if __name__ == '__main__':
    generate_website_json()
