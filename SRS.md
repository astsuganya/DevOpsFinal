# Software Requirements Specification (SRS)
## Project Name: Lost and Found

### 1. Introduction
"Lost and Found" is a web application designed to help people find their lost items or report items they have found. Users can post pictures of the items, specify the location where it was lost or found, and communicate via a comment section.

### 2. General Description
The application will be built using the Django framework and deployed on Render.com using a CI/CD pipeline from GitHub. It will use PostgreSQL as the database.

### 3. Functional Requirements
- **FR1:** Users can create a post detailing a lost (หาย) or found (เจอ) item.
- **FR2:** A post must include the title, description, location (text), status (Lost/Found), and an image.
- **FR3:** Users can view a feed of all posted items.
- **FR4:** Users can add comments to any existing post to communicate with the poster.
- **FR5:** User authentication (Register/Login) is required. Users must be logged in to post items or comment.

### 4. Non-Functional Requirements
- **NFR1:** The application must be deployed on Render.com.
- **NFR2:** The system will use PostgreSQL for data storage.
- **NFR3:** Source code will be managed via GitHub with CI/CD deployment configured.
- **NFR4:** The application should be mobile-responsive for easy access on the go.
