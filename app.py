from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('data/prod-database.sqlite')
    db.row_factory = sqlite3.Row
    return db

@app.context_processor
def inject_current_year():
    return {
        "current_year": datetime.now().year,
        "current_date": datetime.now().strftime('%Y-%m-%d')
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teams')
def teams():
    db = get_db()
    query = """
        SELECT id as team_id, full_name, nickname, city, state, abbreviation
        FROM team
    """
    params = []
    
    search = request.args.get('search', '').strip()
    
    if search:
        query += " WHERE (city LIKE ? OR nickname LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    query += " ORDER BY city, nickname"
    
    teams = db.execute(query, params).fetchall()
    
    db.close()
    return render_template('teams.html', teams=teams, divisions=[])

@app.route('/teams/<team_id>')
def team_detail(team_id):
    db = get_db()
    
    # Get team info
    team = db.execute("""
        SELECT *
        FROM team_info_common
        WHERE team_id = ?
        AND season_year = (SELECT MAX(season_year) FROM team_info_common)
    """, [team_id]).fetchone()
    
    if not team:
        return "Team not found", 404
    
    # Get recent games
    recent_games = db.execute("""
        SELECT *
        FROM game
        WHERE (team_id_home = ? OR team_id_away = ?)
        ORDER BY game_date DESC
        LIMIT 10
    """, [team_id, team_id]).fetchall()
    
    # Get current roster
    roster = db.execute("""
        SELECT p.*
        FROM player p
        JOIN common_player_info cpi ON p.id = cpi.player_id
        WHERE cpi.team_id = ?
        AND p.is_active = 1
        ORDER BY p.full_name
    """, [team_id]).fetchall()
    
    db.close()
    return render_template('team_detail.html', team=team, recent_games=recent_games, roster=roster)

@app.route('/players')
def players():
    db = get_db()
    query = """
        SELECT p.id, p.full_name, p.is_active,
               cpi.team_id, cpi.team_name, cpi.position,
               cpi.height, cpi.weight, cpi.season_exp
        FROM player p
        LEFT JOIN common_player_info cpi ON p.id = cpi.person_id
    """
    params = []
    
    search = request.args.get('search', '').strip()
    team = request.args.get('team', '').strip()
    is_active = request.args.get('is_active', '').strip()
    
    where_clauses = []
    
    if search:
        where_clauses.append("(p.full_name LIKE ?)")
        params.append(f"%{search}%")
    
    if team:
        where_clauses.append("cpi.team_id = ?")
        params.append(team)
        
    if is_active:
        where_clauses.append("p.is_active = ?")
        params.append(int(is_active))
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY p.full_name"
    
    players = db.execute(query, params).fetchall()
    
    # Get teams for filter dropdown
    teams = db.execute("""
        SELECT id as team_id, city as team_city, nickname as team_name
        FROM team
        ORDER BY city, nickname
    """).fetchall()
    
    db.close()
    return render_template('players.html', players=players, teams=teams)

@app.route('/players/<player_id>')
def player_detail(player_id):
    db = get_db()
    
    # Get player info
    player = db.execute("""
        SELECT p.*, cpi.*,
               dh.draft_year, dh.draft_round, dh.draft_number
        FROM player p
        LEFT JOIN common_player_info cpi ON p.id = cpi.player_id
        LEFT JOIN draft_history dh ON p.id = dh.player_id
        WHERE p.id = ?
    """, [player_id]).fetchone()
    
    if not player:
        return "Player not found", 404
    
    # Get recent games
    recent_games = db.execute("""
        SELECT g.*, ls.*
        FROM game g
        JOIN line_score ls ON g.game_id = ls.game_id
        WHERE ls.player_id = ?
        ORDER BY g.game_date DESC
        LIMIT 10
    """, [player_id]).fetchall()
    
    db.close()
    return render_template('player_detail.html', player=player, recent_games=recent_games)

@app.route('/games')
def games():
    db = get_db()
    query = """
        SELECT DISTINCT game_id, 
               strftime('%Y-%m-%d', game_date) as game_date,
               season_type,
               team_id_home, team_name_home, pts_home,
               team_id_away, team_name_away, pts_away
        FROM game
    """
    params = []
    where_clauses = []
    
    date = request.args.get('date', '').strip()
    team = request.args.get('team', '').strip()
    season_type = request.args.get('season_type', '').strip()
    
    if date:
        where_clauses.append("DATE(game_date) = DATE(?)")
        params.append(date)
    
    if team:
        where_clauses.append("(team_id_home = ? OR team_id_away = ?)")
        params.extend([team, team])
        
    if season_type:
        where_clauses.append("season_type = ?")
        params.append(season_type)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY game_date DESC LIMIT 100"
    
    games = db.execute(query, params).fetchall()
    
    # Get teams for filter dropdown
    teams = db.execute("""
        SELECT id as team_id, city as team_city, nickname as team_name 
        FROM team
        ORDER BY city, nickname
    """).fetchall()
    
    db.close()
    return render_template('games.html', games=games, teams=teams)

@app.route('/games/<game_id>')
def game_detail(game_id):
    db = get_db()
    
    # Get game info
    game = db.execute("""
        SELECT *
        FROM game
        WHERE game_id = ?
    """, [game_id]).fetchone()
    
    if not game:
        return "Game not found", 404
    
    # Get player statistics
    player_stats = db.execute("""
        SELECT ls.*, p.full_name as player_name, p.id as player_id
        FROM line_score ls
        JOIN player p ON ls.player_id = p.id
        WHERE ls.game_id = ?
        ORDER BY ls.team_id, ls.min DESC
    """, [game_id]).fetchall()
    
    db.close()
    return render_template('game_detail.html', game=game, player_stats=player_stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)