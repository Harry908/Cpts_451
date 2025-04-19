DROP TABLE IF EXISTS business_updates;

CREATE TABLE business_updates AS
SELECT 
    b.business_id,
    CASE 
        WHEN chk.total_checkins IS NULL THEN 0 
        ELSE chk.total_checkins 
    END AS numCheckins,
    CASE 
        WHEN rev.reviewcount IS NULL THEN 0 
        ELSE rev.reviewcount 
    END AS reviewcount,
    CASE 
        WHEN rev.reviewrating IS NULL THEN 0 
        ELSE rev.reviewrating 
    END AS reviewrating
FROM business b
LEFT JOIN (
    SELECT business_id, SUM(count) AS total_checkins
    FROM business_check_in
    GROUP BY business_id
) AS chk ON b.business_id = chk.business_id
LEFT JOIN (
    SELECT business_id, COUNT(*) AS reviewcount, AVG(stars) AS reviewrating
    FROM review
    GROUP BY business_id
) AS rev ON b.business_id = rev.business_id;

UPDATE business
SET 
    numCheckins = (
        SELECT bu.numCheckins
        FROM business_updates bu
        WHERE bu.business_id = business.business_id
    ),
    reviewcount = (
        SELECT bu.reviewcount
        FROM business_updates bu
        WHERE bu.business_id = business.business_id
    ),
    reviewrating = (
        SELECT bu.reviewrating
        FROM business_updates bu
        WHERE bu.business_id = business.business_id
    )
WHERE business_id IN (SELECT business_id FROM business_updates);