CREATE TABLE contact_messages (
    id SERIAL PRIMARY KEY,
    sender_name VARCHAR(100) NOT NULL,
    sender_email VARCHAR(100) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    sent_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO contact_messages (sender_name, sender_email, subject, content, sent_at, is_read) VALUES
('John Doe', 'john.doe@example.com', 'Question about membership', 'Hi, I have a question about membership. Can you help?', '2024-06-01 10:15:00', FALSE),
('Jane Smith', 'jane.smith@example.com', 'Feedback on event', 'Hello, I attended the recent event and wanted to share my feedback.', '2024-06-02 12:30:00', FALSE),
('Alice Brown', 'alice.brown@example.com', 'Volunteer Inquiry', 'I am interested in volunteering. Please provide more information.', '2024-06-03 09:45:00', FALSE),
('Bob Johnson', 'bob.johnson@example.com', 'Partnership Proposal', 'We are interested in a partnership. Let’s discuss further.', '2024-06-04 14:20:00', FALSE),
('Charlie Davis', 'charlie.davis@example.com', 'Technical Issue', 'I am experiencing a technical issue with the website.', '2024-06-05 16:10:00', FALSE);
