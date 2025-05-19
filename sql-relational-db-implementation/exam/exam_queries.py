import csv
import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


QUERIES = {
    "query1_count_by_type": """
        SELECT t.name_type AS type, COUNT(*) AS count
        FROM pokemontype pt
        JOIN types t ON pt.type_id = t.type_id
        GROUP BY t.name_type
        ORDER BY count DESC;
    """,
    "query2_base_total_gt_600": """
        SELECT p.name AS name, p.base_total AS base_total
        FROM pokemon p
        WHERE p.base_total > 600
        ORDER BY p.base_total DESC;
    """,
    "query3_avg_base_by_type": """
        SELECT t.name_type AS type, AVG(p.base_total) AS average_base_total 
        FROM pokemontype pt
        JOIN types t ON pt.type_id = t.type_id
        JOIN pokemon p ON pt.pokedex_number = p.pokedex_number
        GROUP BY t.name_type
        ORDER BY AVG(p.base_total) ASC;
    """,
    "query4_overgrow_ability": """
        SELECT p.name AS name, p.base_total AS base_total
        FROM pokemon p
        JOIN pokemonability pa ON p.pokedex_number = pa.pokedex_number
        JOIN abilities a ON pa.ability_id = a.ability_id
        WHERE a.name_ability = 'Overgrow'
        ORDER BY p.base_total DESC;
    """,
    "query5_primary_and_secondary": """
        SELECT p.name AS name,
        ( 
            SELECT t2.name_type
            FROM pokemontype pt2
            JOIN types t2 ON pt2.type_id = t2.type_id
            WHERE pt2.pokedex_number = p.pokedex_number
            ORDER BY t2.name_type
            LIMIT 1 
        ) AS primary_type,
        ( 
            SELECT t2.name_type
            FROM pokemontype pt2
            JOIN types t2 ON pt2.type_id = t2.type_id
            WHERE pt2.pokedex_number = p.pokedex_number
            ORDER BY t2.name_type
            OFFSET 1
            LIMIT 1
        ) AS secondary_type
        FROM pokemon p
        ORDER BY p.name;
    """,
    "query6_above_avg_stats": """
        WITH gen_avg AS (
            SELECT p.generation, 
                AVG(p.base_total + s.hp + s.attack + s.defense + s.speed + s.sp_attack + s.sp_defense) AS avg_stats
            FROM Pokemon p
            JOIN Stats s ON p.pokedex_number = s.pokedex_number
            GROUP BY p.generation
        )
        SELECT p.name AS name, 
            p.generation, 
            (p.base_total + s.hp + s.attack + s.defense + s.speed + s.sp_attack + s.sp_defense) AS total_stats
        FROM Pokemon p
        JOIN Stats s ON p.pokedex_number = s.pokedex_number
        JOIN gen_avg g ON p.generation = g.generation
        WHERE (p.base_total + s.hp + s.attack + s.defense + s.speed + s.sp_attack + s.sp_defense) > g.avg_stats
        ORDER BY p.generation, total_stats DESC;
    """,
    "query7_fire_attack_gt_100": """
        SELECT p.name AS name, s.attack AS attack
        FROM pokemon p
        JOIN stats s ON p.pokedex_number = s.pokedex_number
        JOIN pokemontype pt ON p.pokedex_number = pt.pokedex_number
        JOIN types t ON pt.type_id = t.type_id
        WHERE t.name_type = 'fire' AND s.attack > 100
        ORDER BY s.attack DESC;
    """,
    "query8_stats_vs_generation_avg": """
        WITH gen_avg AS (
            SELECT p.generation, 
                AVG(p.base_total + s.hp + s.attack + s.defense + s.speed + s.sp_attack + s.sp_defense) AS avg_stats 
            FROM pokemon p 
            JOIN stats s ON p.pokedex_number = s.pokedex_number 
            GROUP BY p.generation
        )
        SELECT p.name AS pokemon_name, 
            p.generation AS pokemon_generation, 
            (p.base_total + s.hp + s.attack + s.defense + s.speed + s.sp_attack + s.sp_defense) AS total_stats, 
            CASE WHEN (p.base_total + s.hp + s.attack + s.defense + s.speed + s.sp_attack + s.sp_defense) >= g.avg_stats
                THEN 'Supérieur ou égal à la moyenne'
                ELSE 'Inférieur ou égal à la moyenne'
            END AS total_stats_comparison
        FROM pokemon p
        JOIN stats s ON p.pokedex_number = s.pokedex_number
        JOIN gen_avg g ON p.generation = g.generation
        ORDER BY p.pokedex_number;
    """
}

# load secrets from .env file
load_dotenv()
SQL_USERNAME = os.getenv("SQL_USERNAME")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

# validate
if not (SQL_USERNAME and SQL_PASSWORD):
    raise RuntimeError("Ensure SQL_USERNAME and SQL_PASSWORD are set in .env")

def run_queries_and_export_csv():
    conn = psycopg2.connect(
        database="exam_sql_SIOBHAN",
        host="localhost",
        user=SQL_USERNAME,
        password=SQL_PASSWORD,
        port="5432"
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    for name, sql in QUERIES.items():
        print(f"Running {name} -")
        cursor.execute(sql)
        rows = cursor.fetchall()

        if not rows:
            print("No results found")
            continue

        csv_file = f"{name}.csv"
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        print(f"{len(rows)} rows written to {csv_file}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    run_queries_and_export_csv()
