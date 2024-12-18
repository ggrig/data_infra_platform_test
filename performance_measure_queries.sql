SELECT AVG(length) AS average_length
FROM osm_data;


SELECT highway, COUNT(highway) AS count, SUM(length) AS total_length
FROM osm_data
WHERE highway IS NOT NULL
GROUP BY highway;