DROP TABLE IF EXISTS tmp_checkins;

CREATE TEMPORARY TABLE tmp_checkins AS
SELECT business_id, SUM(count) AS numCheckins
FROM business_check_in
GROUP BY business_id;

DROP TABLE IF EXISTS tmp_reviews;

CREATE TEMPORARY TABLE tmp_reviews AS
SELECT
  business_id,
  COUNT(*)         AS reviewCount,
  AVG(stars) AS reviewRating
FROM review
GROUP BY business_id;

UPDATE business
SET numCheckins = tc.numCheckins
FROM tmp_checkins tc
WHERE business.business_id = tc.business_id;

UPDATE business
SET
  reviewcount  = tr.reviewCount,
  reviewrating = tr.reviewRating
FROM tmp_reviews AS tr
WHERE business.business_id = tr.business_id;

DROP TABLE IF EXISTS tmp_checkins;
DROP TABLE IF EXISTS tmp_reviews;