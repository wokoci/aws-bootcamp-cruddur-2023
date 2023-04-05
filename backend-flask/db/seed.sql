-- this file was manually created
INSERT INTO public.users (display_name, handle, email, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown', 'andrewbrown@exam.co' ,'MOCK'),
  ('Andrew Bayko', 'bayko','bayko@exam.co' ,'MOCK'),
   ('Jeffrey Wokocha', 'jeffrey','wokoci@gmail.com' ,'MOCK'),;


INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )