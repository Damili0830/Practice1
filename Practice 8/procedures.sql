-- =========================================================
-- PROCEDURE 1: Insert or update single contact (UPSERT)
-- =========================================================
-- If the contact (same name + surname) already exists:
--      → update phone
-- If not:
--      → insert new row
CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,        -- input name
    p_surname VARCHAR,     -- input surname
    p_phone VARCHAR        -- input phone
)
LANGUAGE plpgsql AS $$
BEGIN
    -- EXISTS → checks if ANY row matches the condition
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE name = p_name AND surname = p_surname
    ) THEN

        -- If found → update phone number
        UPDATE contacts
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;

    ELSE
        -- If not found → insert new record
        INSERT INTO contacts(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;



-- =========================================================
-- PROCEDURE 2: Insert many contacts with validation
-- =========================================================
-- Accepts 3 arrays (same size): names, surnames, phones
-- Loops through all items one-by-one
-- Valid phone must contain ONLY digits and be at least 6 chars
-- invalid_data collects lines describing invalid inputs
CREATE OR REPLACE PROCEDURE insert_many_contacts(
    IN p_names TEXT[],          -- array of names
    IN p_surnames TEXT[],       -- array of surnames
    IN p_phones TEXT[],         -- array of phone numbers
    INOUT invalid_data TEXT DEFAULT ''   -- output error string
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;  -- index for looping through arrays
BEGIN
    -- Loop from 1 to length of the array
    FOR i IN 1..array_length(p_names, 1) LOOP

        -- Regex: ^[0-9]{6,}$ → only digits, at least 6 digits
        IF p_phones[i] !~ '^[0-9]{6,}$' THEN

            -- Add info about invalid input into the output variable
            invalid_data := invalid_data ||
                format(
                    'Invalid phone: %s %s %s\n',
                    p_names[i], p_surnames[i], p_phones[i]
                );

            -- Skip to next iteration (do not insert this row)
            CONTINUE;
        END IF;

        -- If the contact exists → update
        IF EXISTS (
            SELECT 1
            FROM contacts
            WHERE name = p_names[i] AND surname = p_surnames[i]
        ) THEN

            UPDATE contacts
            SET phone = p_phones[i]
            WHERE name = p_names[i] AND surname = p_surnames[i];

        ELSE
            -- Insert new contact
            INSERT INTO contacts(name, surname, phone)
            VALUES (p_names[i], p_surnames[i], p_phones[i]);
        END IF;

    END LOOP; -- loop ends
END;
$$;



-- =========================================================
-- PROCEDURE 3: Delete contact by name OR phone
-- =========================================================
-- User must provide either name or phone.
-- If both are NULL → error.
CREATE OR REPLACE PROCEDURE delete_contact(
    p_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    -- Case 1: delete by name
    IF p_name IS NOT NULL THEN
        DELETE FROM contacts WHERE name = p_name;

    -- Case 2: delete by phone
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;

    -- Case 3: nothing provided → error
    ELSE
        RAISE EXCEPTION 'Provide either name or phone';
    END IF;
END;
$$;