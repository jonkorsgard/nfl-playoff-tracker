// Sample data structure - this will be replaced by data from your Python script
// The Python script should output a JSON file with this structure

const sampleData = {
    "generated_at": "2026-01-26T15:30:00",
    "weekend": "Conference Championships - Jan 25-26, 2026",
    "team1": {
        "name": "TEAM 1",
        "total_points": 150.54,
        "roster": [
            {
                "position": "QB",
                "name": "Drake Maye",
                "team": "NE",
                "stats": "65 rush yds, 1 TD",
                "points": 12.5
            },
            {
                "position": "RB",
                "name": "RJ Harvey",
                "team": "DEN",
                "stats": "37 rush yds, 4 rec, 22 rec yds",
                "points": 9.9
            },
            {
                "position": "RB",
                "name": "Kyren Williams",
                "team": "LAR",
                "stats": "2 rec, 22 rec yds, 1 TD",
                "points": 10.2
            },
            {
                "position": "WR",
                "name": "Puka Nacua",
                "team": "LAR",
                "stats": "11 rec, 153 rec yds, 1 TD",
                "points": 36.3
            },
            {
                "position": "WR",
                "name": "Davante Adams",
                "team": "LAR",
                "stats": "4 rec, 89 rec yds, 1 TD",
                "points": 18.9
            },
            {
                "position": "TE",
                "name": "Hunter Henry",
                "team": "NE",
                "stats": "6 rec, 54 rec yds",
                "points": 11.4
            },
            {
                "position": "FLEX",
                "name": "Kayshon Boutte",
                "team": "NE",
                "stats": "3 rec, 31 rec yds",
                "points": 6.1
            },
            {
                "position": "D/ST",
                "name": "Patriots D/ST",
                "team": "NE",
                "stats": "7 PA, 3 sacks, 1 INT, 1 FR, 1 BLK",
                "points": 27.0
            },
            {
                "position": "K",
                "name": "Jason Myers",
                "team": "SEA",
                "stats": "1/1 FG, 4/4 XP",
                "points": 7.0
            }
        ]
    },
    "team2": {
        "name": "TEAM 2",
        "total_points": 153.66,
        "roster": [
            {
                "position": "QB",
                "name": "Matthew Stafford",
                "team": "LAR",
                "stats": "374 pass yds, 3 TD, 16 rush yds",
                "points": 45.56
            },
            {
                "position": "RB",
                "name": "Kenneth Walker",
                "team": "SEA",
                "stats": "62 rush yds, 1 TD, 4 rec, 49 rec yds",
                "points": 25.1
            },
            {
                "position": "RB",
                "name": "Rhamondre Stevenson",
                "team": "NE",
                "stats": "71 rush yds",
                "points": 7.1
            },
            {
                "position": "WR",
                "name": "Jaxon Smith-Njigba",
                "team": "SEA",
                "stats": "10 rec, 153 rec yds, 1 TD",
                "points": 40.3
            },
            {
                "position": "WR",
                "name": "Courtland Sutton",
                "team": "DEN",
                "stats": "3 rec, 17 rec yds, 1 TD",
                "points": 14.7
            },
            {
                "position": "TE",
                "name": "Colby Parkinson",
                "team": "LAR",
                "stats": "3 rec, 62 rec yds",
                "points": 9.2
            },
            {
                "position": "FLEX",
                "name": "Stefon Diggs",
                "team": "NE",
                "stats": "5 rec, 17 rec yds",
                "points": 6.7
            },
            {
                "position": "D/ST",
                "name": "Seahawks D/ST",
                "team": "SEA",
                "stats": "27 PA, 1 sack, 1 FR",
                "points": 6.0
            },
            {
                "position": "K",
                "name": "Will Lutz",
                "team": "DEN",
                "stats": "0/2 FG, 1/1 XP",
                "points": -1.0
            }
        ]
    },
    "top_performers": [
        { "rank": 1, "name": "Matthew Stafford", "position": "QB", "team": "LAR", "stats": "374 pass yds, 3 TD", "points": 45.56 },
        { "rank": 2, "name": "Jaxon Smith-Njigba", "position": "WR", "team": "SEA", "stats": "10 rec, 153 yds, 1 TD", "points": 40.3 },
        { "rank": 3, "name": "Puka Nacua", "position": "WR", "team": "LAR", "stats": "11 rec, 153 yds, 1 TD", "points": 36.3 },
        { "rank": 4, "name": "Patriots D/ST", "position": "D/ST", "team": "NE", "stats": "7 PA, 3 sacks, 1 INT", "points": 27.0 },
        { "rank": 5, "name": "Kenneth Walker", "position": "RB", "team": "SEA", "stats": "62 rush yds, 1 TD, 4 rec", "points": 25.1 }
    ]
};



// Update scoreboard
function updateScoreboard(data) {
    const team1Score = document.getElementById('team1-score');
    const team2Score = document.getElementById('team2-score');
    
    animateNumber(team1Score, 0, data.team1.total_points, 2000);
    animateNumber(team2Score, 0, data.team2.total_points, 2000);
}

// Animate number counting up
function animateNumber(element, start, end, duration) {
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuad = progress => 1 - (1 - progress) * (1 - progress);
        const current = start + (end - start) * easeOutQuad(progress);
        
        element.textContent = current.toFixed(2);
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Populate roster table
function populateRoster(teamId, teamData) {
    const tbody = document.getElementById(`${teamId}-tbody`);
    const totalElement = document.getElementById(`${teamId}-total`);
    
    tbody.innerHTML = '';
    
    teamData.roster.forEach((player, index) => {
        const row = document.createElement('tr');
        row.style.animationDelay = `${index * 0.05}s`;
        row.classList.add('fade-in-row');
        
        row.innerHTML = `
            <td><span class="pos-badge">${player.position}</span></td>
            <td class="player-name">${player.name}</td>
            <td class="team-abbr">${player.team}</td>
            <td class="stat-col">${player.stats}</td>
            <td class="pts-col">${player.points.toFixed(2)}</td>
        `;
        
        tbody.appendChild(row);
    });
    
    totalElement.textContent = `${teamData.total_points.toFixed(2)} PTS`;
}

// Populate top performers
function populateTopPerformers(performers) {
    const grid = document.getElementById('performers-grid');
    grid.innerHTML = '';
    
    performers.forEach(performer => {
        const card = document.createElement('div');
        card.className = 'performer-card';
        
        card.innerHTML = `
            <div class="performer-rank">#${performer.rank}</div>
            <div class="performer-name">${performer.name}</div>
            <div class="performer-pos">${performer.position} • ${performer.team}</div>
            <div class="performer-stats">${performer.stats}</div>
            <div class="performer-points">${performer.points.toFixed(2)}</div>
        `;
        
        grid.appendChild(card);
    });
}

// Show winner banner
function showWinner(team1, team2) {
    const banner = document.getElementById('winner-banner');
    const winnerText = document.getElementById('winner-text');
    
    if (team1.total_points > team2.total_points) {
        const margin = (team1.total_points - team2.total_points).toFixed(2);
        winnerText.textContent = `${team1.name} WINS by ${margin} points!`;
        banner.classList.remove('hidden');
    } else if (team2.total_points > team1.total_points) {
        const margin = (team2.total_points - team1.total_points).toFixed(2);
        winnerText.textContent = `${team2.name} WINS by ${margin} points!`;
        banner.classList.remove('hidden');
    } else {
        winnerText.textContent = 'TIE GAME!';
        banner.classList.remove('hidden');
    }
}

// Update last updated time
function updateLastUpdated(timestamp) {
    const element = document.getElementById('last-update');
    const date = new Date(timestamp);
    element.textContent = date.toLocaleString();
}

// Load data when page loads
document.addEventListener('DOMContentLoaded', loadData);

// Add CSS animation for table rows
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInRow {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .fade-in-row {
        animation: fadeInRow 0.5s ease-out backwards;
    }
`;
document.head.appendChild(style);
