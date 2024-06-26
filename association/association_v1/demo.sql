-- Use the database
USE association_db;

-- Insert users
INSERT INTO user (username, password, email, name, address, postal_address, date_of_birth, marital_status, phone, is_admin)
VALUES 
('john_doe', 'password123', 'john@example.com', 'John Doe', '123 Elm Street', 'P.O. Box 456', '1985-05-15', 'Single', '555-1234', FALSE),
('jane_smith', 'password456', 'jane@example.com', 'Jane Smith', '456 Oak Avenue', 'P.O. Box 789', '1990-08-25', 'Married', '555-5678', FALSE),
('michael_brown', 'password789', 'michael@example.com', 'Michael Brown', '789 Pine Road', 'P.O. Box 123', '1980-12-10', 'Married', '555-7890', FALSE),
('lisa_white', 'password012', 'lisa@example.com', 'Lisa White', '321 Cedar Lane', 'P.O. Box 321', '1975-03-22', 'Single', '555-9012', FALSE),
('alex_green', 'password789', 'alex@example.com', 'Alex Green', '567 Maple Avenue', 'P.O. Box 567', '1995-07-20', 'Single', '555-2345', FALSE),
('emily_harris', 'password345', 'emily@example.com', 'Emily Harris', '890 Pine Street', 'P.O. Box 890', '1988-09-18', 'Married', '555-6789', FALSE),
('david_jones', 'password678', 'david@example.com', 'David Jones', '432 Birch Lane', 'P.O. Box 432', '1972-01-05', 'Divorced', '555-3456', FALSE),
('sarah_miller', 'password901', 'sarah@example.com', 'Sarah Miller', '654 Cedar Road', 'P.O. Box 654', '1992-03-30', 'Single', '555-7890', FALSE),
('ryan_thomas', 'password234', 'ryan@example.com', 'Ryan Thomas', '876 Oak Street', 'P.O. Box 876', '1983-11-12', 'Married', '555-4567', FALSE),
('olivia_clark', 'password567', 'olivia@example.com', 'Olivia Clark', '987 Pine Avenue', 'P.O. Box 987', '1990-02-28', 'Single', '555-8901', FALSE);

-- Insert events
INSERT INTO event (name, date)
VALUES 
('Annual General Meeting', '2025-07-15 10:00:00'),
('Summer Picnic', '2025-08-20 12:00:00'),
('Spring Festival', '2025-05-10 14:00:00'),
('Charity Run', '2025-09-25 09:00:00'),
('Holiday Gala', '2025-12-15 19:00:00'),
('Volunteer Orientation', '2025-03-05 11:00:00'),
('Community Workshop', '2025-06-08 15:00:00'),
('Fundraising Dinner', '2025-10-20 18:30:00'),
('Health Fair', '2025-04-22 09:30:00'),
('Art Exhibition', '2025-11-08 10:00:00');

-- Insert news
INSERT INTO news (title, content, image_url, date)
VALUES 
('New Board Elected', 'We are pleased to announce the election of our new board.', 'board_election.jpg', '2023-06-01 09:00:00'),
('Summer Picnic Announcement', 'Join us for our annual summer picnic at the park.', 'summer_picnic.jpg', '2023-07-01 10:00:00'),
('Spring Festival Success', 'Our spring festival was a huge success with over 500 attendees.', 'spring_festival.jpg', '2023-05-12 11:00:00'),
('Charity Run Recap', 'Recap of the charity run event that raised funds for local schools.', 'charity_run_recap.jpg', '2023-09-26 08:00:00'),
('Holiday Gala Highlights', 'Highlights from our annual holiday gala event.', 'holiday_gala_highlights.jpg', '2023-12-16 10:00:00'),
('Volunteer Orientation Update', 'Update on the recent volunteer orientation session.', 'volunteer_orientation_update.jpg', '2023-03-06 14:00:00'),
('Community Workshop Summary', 'Summary of key takeaways from our community workshop.', 'community_workshop_summary.jpg', '2023-06-09 12:00:00'),
('Fundraising Dinner Success', 'Successful fundraising dinner with generous contributions from attendees.', 'fundraising_dinner_success.jpg', '2023-10-21 09:00:00'),
('Health Fair Report', 'Report on health fair activities and participant feedback.', 'health_fair_report.jpg', '2023-04-23 15:00:00'),
('Art Exhibition Opening', 'Opening day of our art exhibition showcasing local artists.', 'art_exhibition_opening.jpg', '2023-11-09 11:00:00');

-- Insert achievements
INSERT INTO achievement (name, start_date, end_date, site, objectives, beneficiaries_kind, beneficiaries_number, results_obtained)
VALUES 
('Community Clean-Up', '2023-04-01', '2023-04-07', 'City Park', 'Clean up the park and surrounding areas.', 'Volunteers', 50, 'Park cleaned and waste collected.'),
('Youth Leadership Program', '2023-05-01', '2023-05-30', 'Community Center', 'Empower young leaders in the community.', 'Youth', 30, 'Successful workshops and leadership activities.'),
('Environmental Awareness Campaign', '2023-06-01', '2023-06-30', 'Various locations', 'Raise awareness about environmental issues.', 'Community', 100, 'Increased awareness and participation in eco-friendly practices.'),
('Tech Workshops for Seniors', '2023-07-01', '2023-07-15', 'Senior Center', 'Provide basic tech skills to seniors.', 'Seniors', 25, 'Successful workshops with positive feedback.'),
('Food Drive Initiative', '2023-08-01', '2023-08-15', 'Local Food Bank', 'Collect and distribute food donations to families in need.', 'Families', 200, 'Significant amount of food collected and distributed.'),
('Educational Scholarship Program', '2023-09-01', '2023-09-30', 'Local Schools', 'Award scholarships to deserving students for higher education.', 'Students', 10, 'Ten scholarships awarded to talented students.'),
('Healthcare Awareness Campaign', '2023-10-01', '2023-10-31', 'Health Clinics', 'Promote health awareness and screenings in the community.', 'Patients', 150, 'Increased health screenings and awareness among residents.'),
('Cultural Diversity Festival', '2023-11-01', '2023-11-15', 'Community Center', 'Celebrate cultural diversity through performances and exhibits.', 'Community', 300, 'Successful event with diverse cultural participation.'),
('Literacy Program Expansion', '2023-12-01', '2023-12-31', 'Local Libraries', 'Expand literacy programs for children and adults.', 'Participants', 50, 'Increased literacy skills and engagement in reading.'),
('Artisan Market Launch', '2024-01-01', '2024-01-15', 'City Square', 'Launch a market to promote local artisans and craftsmen.', 'Artisans', 40, 'Successful market launch with positive feedback from vendors and attendees.');

-- Insert associations
INSERT INTO association (name)
VALUES 
('Community Helpers Association'),
('Youth Empowerment Network'),
('Environmental Advocates'),
('Senior Support Group'),
('Women Empowerment Initiative'),
('Sports Enthusiasts Club'),
('Tech Innovation Forum'),
('Cultural Exchange Society'),
('Healthcare Professionals Network'),
('Business Leaders Alliance');

-- Insert reports
INSERT INTO report (title, date, content)
VALUES 
('Quarterly Financial Report Q1 2023', '2023-04-15 10:00:00', 'Details of financial performance in Q1 2023.'),
('Annual Activities Report 2023', '2023-12-31 17:00:00', 'Summary of all activities and events in 2023.'),
('Mid-Year Financial Report 2023', '2023-07-15 10:00:00', 'Details of financial performance in the first half of 2023.'),
('Community Outreach Report 2023', '2023-11-30 17:00:00', 'Summary of community outreach activities in 2023.'),
('Environmental Impact Assessment', '2023-08-31 15:00:00', 'Assessment of environmental initiatives and their impact.'),
('Healthcare Access Report', '2023-09-30 12:00:00', 'Analysis of healthcare access and initiatives in the community.'),
('Educational Program Evaluation', '2023-10-31 09:00:00', 'Evaluation of educational programs and their effectiveness.'),
('Cultural Event Feedback', '2023-11-30 14:00:00', 'Feedback received from participants of our recent cultural event.'),
('Volunteer Impact Assessment', '2023-12-31 11:00:00', 'Assessment of volunteer contributions and their impact on community programs.');

-- Insert contact messages
INSERT INTO contact_message (sender_name, sender_email, subject, content)
VALUES 
('Alice Brown', 'alice@example.com', 'Inquiry about membership', 'I would like to know more about becoming a member.'),
('Bob White', 'bob@example.com', 'Volunteer opportunities', 'Are there any upcoming volunteer opportunities I can join?'),
('Emma Davis', 'emma@example.com', 'Donation query', 'I have some items I would like to donate. Can you please provide information on drop-off locations?'),
('James Wilson', 'james@example.com', 'Event registration', 'I would like to register for the upcoming charity run event.'),
('Sophia Lee', 'sophia@example.com', 'Feedback on recent workshop', 'I attended the recent community workshop and wanted to provide feedback.'),
('William Garcia', 'william@example.com', 'Partnership proposal', 'I represent a local business interested in partnering with your association.'),
('Olivia Martinez', 'olivia@example.com', 'Question about upcoming event', 'Could you provide more details about the Spring Festival event?'),
('Noah Rodriguez', 'noah@example.com', 'Request for sponsorship', 'I am organizing a local charity event and would like to inquire about sponsorship opportunities.'),
('Ava Hernandez', 'ava@example.com', 'Interest in volunteering', 'I am interested in volunteering with your organization. How can I get involved?'),
('Ethan Moore', 'ethan@example.com', 'Issue with membership login', 'I am having trouble logging into my membership account. Can you assist me?');

-- Insert attendance
INSERT INTO attendance (event_id, user_id, name, email, phone)
VALUES 
(1, 1, 'John Doe', 'john@example.com', '555-1234'),
(2, 2, 'Jane Smith', 'jane@example.com', '555-5678'),
(3, 3, 'Michael Brown', 'michael@example.com', '555-7890'),
(4, 4, 'Lisa White', 'lisa@example.com', '555-9012'),
(5, 5, 'Alex Green', 'alex@example.com', '555-2345'),
(6, 6, 'Emily Harris', 'emily@example.com', '555-6789'),
(7, 7, 'David Jones', 'david@example.com', '555-3456'),
(8, 8, 'Sarah Miller', 'sarah@example.com', '555-7890'),
(9, 9, 'Ryan Thomas', 'ryan@example.com', '555-4567'),
(10, 10, 'Olivia Clark', 'olivia@example.com', '555-8901');

-- Insert user_event
INSERT INTO user_event (user_id, event_id)
VALUES 
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);
