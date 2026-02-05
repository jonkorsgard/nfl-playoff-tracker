// Function to load data with cache-busting
async function loadData() {
    try {
        // Add timestamp to prevent CDN caching
        const cacheBuster = new Date().getTime();
        const response = await fetch(`championship_results.json?v=${cacheBuster}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Update scores and populate tables
        updateScoreboard(data);
        populateRoster('team1', data.team1);
        populateRoster('team2', data.team2);
        populateTopPerformers(data.top_performers);
        updateLastUpdated(data.generated_at);
        
        // Determine winner
        showWinner(data.team1, data.team2);
        
    } catch (error) {
        console.error('Error loading data:', error);
        // Show error message to user
        document.querySelector('.main').innerHTML = `
            <div style="text-align: center; padding: 60px 20px; color: #FF6B35;">
                <h2 style="font-size: 32px; margin-bottom: 20px;">⚠️ Data Not Available</h2>
                <p style="font-size: 18px; color: #8B92B8;">
                    Run <code style="background: #151B3B; padding: 4px 8px; border-radius: 4px;">python generate_website_data.py</code> to generate the data file.
                </p>
            </div>
        `;
    }
}

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
