# NBA Explorer Copilot Instructions

## Project Overview
This is a Python-based web application that provides a frontend for browsing NBA data stored in a SQLite database. The application should follow the NBA website's design aesthetic while providing easy access to teams, players, and games data.

## Technical Requirements
- Backend: Python with vanilla Flask
- Database: SQLite (local file)
- Frontend: HTML and CSS only (no JavaScript frameworks)
- Deployment: Containerized application

## Core Features
1. Homepage with navigation to teams, players, and games sections
2. Listing pages with search and filtering capabilities
3. Detail pages for individual items
4. NBA-inspired visual design
5. Containerized deployment ready for VPS hosting

## Implementation Guidelines

### Directory Structure
```
/
├── templates/          # HTML templates
├── static/            # CSS and static assets
├── data/             # SQLite database
├── app.py            # Main Flask application
└── Dockerfile        # Container configuration
```

### Flow Implementation
1. Homepage serves as the central hub with clear navigation
2. Listing pages (teams, players, games) display tabulated data with search/filter
3. Detail pages show comprehensive information for selected items
4. All pages maintain consistent NBA-inspired styling

### Technical Implementation Steps
1. Set up Flask application with SQLite database connection
2. Create HTML templates for all required pages
3. Implement search and filtering functionality
4. Style pages to match NBA website aesthetic
5. Package application in container

### Search and Filter Requirements
- Implement on all listing pages
- Support filtering by multiple criteria
- Ensure efficient database queries
- Provide clear UI for search/filter options

### Design Guidelines
- Follow NBA website color scheme and layout
- Ensure responsive design
- Maintain consistent navigation patterns
- Focus on readability and usability

### Security Considerations
- Implement input sanitization
- Follow Flask security best practices
- Ensure secure database access

### Performance Requirements
- Fast page load times
- Efficient database queries
- Responsive UI
- Containerized deployment optimization

## Out of Scope
- User authentication
- Real-time data updates
- Third-party API integrations
- Advanced frontend frameworks
- External database management

## Development Workflow
1. Use VS Code as primary IDE
2. Follow Python and Flask best practices
3. Test locally before containerization
4. Validate container deployment
5. Ensure error handling is in place