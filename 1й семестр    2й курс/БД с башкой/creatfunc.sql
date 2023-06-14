CREATE FUNCTION masterInfo(name varchar(64))
RETURNS TABLE(f1 varchar(64), f2 INT) AS $$
BEGIN 
RETURN QUERY SELECT m.lastname, m.qualification
FROM master m
where m.lastname = name;
END;
$$ LANGUAGE plpgsql;