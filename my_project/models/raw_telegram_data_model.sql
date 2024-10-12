-- models/cleaned_telegram_data_model.sql

{{ config(
    materialized='view'  -- or 'table' based on your requirements
) }}

WITH raw_data AS (
    SELECT
        id,
        created_at,
        text,
        user_id,
        user_name,
        CASE 
            WHEN lower(text) LIKE '%urgent%' THEN 'High Priority'
            WHEN lower(text) LIKE '%important%' THEN 'Medium Priority'
            ELSE 'Low Priority'
        END AS priority,
        -- Additional transformations can be added here
        -- Example: Extracting date part from created_at
        DATE_TRUNC('day', created_at) AS created_date
    FROM 
        public.telegram_data
    WHERE 
        created_at IS NOT NULL  -- Filter out records without a timestamp
)

SELECT 
    id,
    created_date,
    text,
    user_id,
    user_name,
    priority
FROM 
    raw_data
ORDER BY 
    created_date DESC;  -- Optional: order the result
