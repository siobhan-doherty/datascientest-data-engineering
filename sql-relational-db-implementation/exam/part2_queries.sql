-- Query 1: Count the number of Pokémon by type in descending order.
SELECT t.name_type AS type, COUNT(*) AS count
FROM pokemontype pt
JOIN types t ON pt.type_id = t.type_id
GROUP BY t.name_type
ORDER BY count DESC;

-- Query 2: List Pokémon with a base number of points greater than 600, sorted in descending order.
SELECT p.name AS name, p.base_total AS base_total
FROM pokemon p
WHERE p.base_total > 600
ORDER BY p.base_total DESC;

-- Query 3: Display Pokémon types with average points in ascending order
SELECT t.name_type AS type, AVG(p.base_total) AS average_base_total 
FROM pokemontype pt
JOIN types t ON pt.type_id = t.type_id
JOIN pokemon p ON pt.pokedex_number = p.pokedex_number
GROUP BY t.name_type
ORDER BY AVG(p.base_total) ASC;

-- Query 4: Find Pokémon with the special ability 'Overgrow' and sort by the points base in descending order.
SELECT p.name AS name, p.base_total AS base_total
FROM pokemon p
JOIN pokemonability pa ON p.pokedex_number = pa.pokedex_number
JOIN abilities a ON pa.ability_id = a.ability_id
WHERE a.name_ability = 'Overgrow'
ORDER BY p.base_total DESC;

-- Query 5: List the names of the Pokémon, their main type and their secondary type (if they have one). Sort by name.
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

-- Request 6: Display Pokémon with above-average total stats per generation.
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

-- Query 7: Find fire-type Pokémon with an attack greater than 100.
SELECT p.name AS name, s.attack AS attack
FROM pokemon p
JOIN stats s ON p.pokedex_number = s.pokedex_number
JOIN pokemontype pt ON p.pokedex_number = pt.pokedex_number
JOIN types t ON pt.type_id = t.type_id
WHERE t.name_type = 'fire' AND s.attack > 100
ORDER BY s.attack DESC;

-- Query 8: Indicate whether a Pokémon's total stats are above or below the generation average. ?
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
