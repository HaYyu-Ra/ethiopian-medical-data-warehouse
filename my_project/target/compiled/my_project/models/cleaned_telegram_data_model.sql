-- models/cleaned_telegram_data_model.sql

SELECT
    message_id,
    date,
    sender_id,
    message,
    media
FROM public.cleaned_telegram_data