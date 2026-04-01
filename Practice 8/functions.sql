-- =====================================
-- functions.sql for PhoneBook Practice 8
-- =====================================

-- 1️⃣ Function: get contacts by pattern (search by name, surname, phone)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern text)
RETURNS TABLE(contact_id integer, contact_name varchar, contact_surname varchar, contact_phone varchar) AS $$
BEGIN
    -- Return all contacts matching the pattern (case-insensitive)
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts c
    WHERE c.name ILIKE '%' || p_pattern || '%'
       OR c.surname ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- 2️⃣ Function: get contacts with pagination
CREATE OR REPLACE FUNCTION get_contacts_paged(p_limit integer, p_offset integer)
RETURNS TABLE(contact_id integer, contact_name varchar, contact_surname varchar, contact_phone varchar) AS $$
BEGIN
    -- Return contacts using LIMIT and OFFSET for pagination
    RETURN QUERY
    SELECT c.id, c.name, c.surname, c.phone
    FROM contacts c
    ORDER BY c.id  -- order by ID to ensure stable pagination
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
