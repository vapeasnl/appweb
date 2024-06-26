-- Use the database
USE association_db;

-- Insert users
INSERT INTO user (username, password, email, name, address, postal_address, date_of_birth, marital_status, phone, is_admin)
VALUES 
('john_doe', 'password123', 'john@example.com', 'John Doe', '123 Elm Street', 'P.O. Box 456', '1985-05-15', 'Single', '555-1234', FALSE),
('jane_smith', 'password456', 'jane@example.com', 'Jane Smith', '456 Oak Avenue', 'P.O. Box 789', '1990-08-25', 'Married', '555-5678', FALSE);

-- Insert events
INSERT INTO event (name, date)
VALUES 
('Annual General Meeting', '2023-07-15 10:00:00'),
('Summer Picnic', '2023-08-20 12:00:00');

-- Insert news
INSERT INTO news (title, content, image_url, date)
VALUES 
('New Board Elected', 'We are pleased to announce the election of our new board.', 'board_election.jpg', '2023-06-01 09:00:00'),
('Summer Picnic Announcement', 'Join us for our annual summer picnic at the park.', 'summer_picnic.jpg', '2023-07-01 10:00:00');

-- Insert media
INSERT INTO media (title, description, file_url)
VALUES 
('Annual Report 2023', 'The annual report for the year 2023.', 'reports/annual_report_2023.pdf'),
('Summer Picnic Photos', 'Photos from the summer picnic event.', 'photos/summer_picnic_2023.zip');

-- Insert achievements
INSERT INTO achievement (name, start_date, end_date, site, objectives, beneficiaries_kind, beneficiaries_number, results_obtained)
VALUES 
('Community Clean-Up', '2023-04-01', '2023-04-07', 'City Park', 'Clean up the park and surrounding areas.', 'Volunteers', 50, 'Park cleaned and waste collected.'),
('Youth Leadership Program', '2023-05-01', '2023-05-30', 'Community Center', 'Empower young leaders in the community.', 'Youth', 30, 'Successful workshops and leadership activities.');

-- Insert associations
INSERT INTO association (name)
VALUES 
('Community Helpers Association'),
('Youth Empowerment Network');

-- Insert reports
INSERT INTO report (title, date, content)
VALUES 
('Quarterly Financial Report Q1 2023', '2023-04-15 10:00:00', 'Details of financial performance in Q1 2023.'),
('Annual Activities Report 2023', '2023-12-31 17:00:00', 'Summary of all activities and events in 2023.');

-- Insert contact messages
INSERT INTO contact_message (sender_name, sender_email, subject, content)
VALUES 
('Alice Brown', 'alice@example.com', 'Inquiry about membership', 'I would like to know more about becoming a member.'),
('Bob White', 'bob@example.com', 'Volunteer opportunities', 'Are there any upcoming volunteer opportunities I can join?');

-- Insert attendance
INSERT INTO attendance (event_id, user_id, name, email, phone)
VALUES 
(1, 1, 'John Doe', 'john@example.com', '555-1234'),
(2, 2, 'Jane Smith', 'jane@example.com', '555-5678');

-- Insert user_event
INSERT INTO user_event (user_id, event_id)
VALUES 
(1, 1),
(2, 2);
